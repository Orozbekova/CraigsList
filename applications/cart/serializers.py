from rest_framework import serializers

from applications.cart.models import CartItem, Cart


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ('post', 'quantity', 'total_cost')


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, write_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'items', 'status')

    def create(self, validated_data):
        request = self.context.get('request')
        items = validated_data.pop('items')
        print(items)
        user = request.user
        cart, _ = Cart.objects.get_or_create(user=user)
        for item in items:
            try:
                cart_item = CartItem.objects.get(cart=cart,
                                                 post=item['post'])
                cart_item.quantity = quantity=item['quantity']
            except CartItem.DoesNotExist:
                cart_item = CartItem(cart=cart, post=item['post'], quantity=item['quantity'])
            cart_item.save()
        return cart


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['post'] = CartItemSerializer(instance.cart_item.all(), many=True).data
        return representation