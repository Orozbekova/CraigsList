from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

from applications.normal_account.models import CustomUser
from main.tasks import send_confirmation_email

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(max_length=100,write_only=True,required=True)

    class Meta:
        model = User
        fields = ('email','password','confirm_password')

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.create_user(email, password)
        code = user.activation_code
        send_confirmation_email.delay(code, user.email)
        # send_confirmation_email(user.activation_code, user.email)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError('Password did not match!')
        return attrs

    # def validate_email(self,email):
    #     if not email.endswith('gmail.com'):
    #         raise serializers.ValidationError("Your email must end with 'gmail.com'")
    #     return email

    def validate(self,attrs):
        email=attrs.get('email')
        password=attrs.get('password')

        if email and password:
            user = authenticate(username=email,password=password)

        if not user:
            raise serializers.ValidationError('Неверный email или password')
        attrs['user']=user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    password = serializers.CharField(required=True,min_length=6)
    password_confirm = serializers.CharField(required=True,min_length=6)

    def validate_old_password(self,old_pass):
        user = self.context.get('request').user
        if not user.check_password(old_pass):
            raise serializers.ValidationError('неверный пароль!')
        return old_pass


    def validate(self,attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.get('password_confirm')


        if pass1 != pass2:
            raise  serializers.ValidationError('Пароли не совпадают')
        return attrs

    def set_user_password(self):
        user = self.context.get('request').user
        password = self.validated_data.get('password')
        user.set_password(password)
        user.save()


#################

class CreateNewPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField(max_length=40,
                                            required=True)
    password = serializers.CharField(min_length=8,
                                     required=True)
    password_confirmation = serializers.CharField(min_length=8,
                                     required=True)

    def validate_email(self, email):
        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Пользователь не найден')
        return email

    def validate_activation_code(self, act_code):
        if not CustomUser.objects.filter(activation_code=act_code,
                                         is_active=False).exists():
            raise serializers.ValidationError('Неверный код активации')
        return act_code

    def validate(self, attrs):
        password = attrs.get('password')
        password_conf = attrs.pop('password_confirmation')
        if password != password_conf:
            raise serializers.ValidationError(
                'Passwords do not match'
            )
        return attrs

    def save(self, **kwargs):
        data = self.validated_data
        email = data.get('email')
        activation_code = data.get('activation_code')
        password = data.get('password')
        try:
            user = CustomUser.objects.get(email=email,
                                          activation_code=activation_code,
                                          is_active=False)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден')

        user.is_active = True
        user.activation_code = ''
        user.set_password(password)
        user.save()
        return user
