from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers

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
        # send_confirmation_email.delay(code, user.email)
        send_confirmation_email(user.activation_code, user.email)
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