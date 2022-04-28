from rest_framework import serializers
from rest_framework.utils import representation
from rest_framework.utils.field_mapping import get_nested_relation_kwargs

from applications.board.models import *



class PostImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    images = PostImageSerializers(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'owner','name','description','category','price','images','sub_category','number_phone')

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES
        # pl=request.user_id
        post = Post.objects.create(**validated_data, owner=request.user)
        print(request.data)

        for image in images_data.getlist('images'):
            Image.objects.create(post=post, image=image)
        return post


    def to_representation(self, instance):
        representation = super().to_representation(instance)

# like_representation
        total_likes = 0
        for i in instance.likes.all():
            total_likes += 1
        representation['likes'] = total_likes
        # representation['likes'] = instance.like.filter(like=True)

# rating_representation
        rating_result = 0
        for i in instance.rating.all():
            print(i)
            rating_result += int(i.rating)

        if instance.rating.all().count() == 0:
            representation['rating'] = rating_result
        else:
            representation[
                'rating'] = rating_result / instance.rating.all().count()
        return representation




class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("review",)

class LikeSerializers(serializers.ModelSerializer):
    class Meta:
        model = Likes
        fields = "__all__"


class FavoriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = "__all__"




class RatingSerializers(serializers.ModelSerializer):
    # owner = serializers.EmailField(required=False)

    class Meta:
        model = Rating
        fields = ('rating',)



# class OrderSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields = "__all__"