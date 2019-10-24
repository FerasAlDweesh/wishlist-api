from rest_framework import serializers
from django.contrib.auth.models import User

from items.models import Item, FavoriteItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class FavSerializer(serializers.ModelSerializer):
	class Meta:
		model = FavoriteItem
		fields = ['user']


class ItemListSerializer(serializers.ModelSerializer):
	detail = serializers.HyperlinkedIdentityField(
        view_name = "api-detail",
        lookup_field = "id",
        lookup_url_kwarg = "item_id"
        )
	added_by = UserSerializer()

	favorited_by = serializers.SerializerMethodField()

	class Meta:
		model = Item
		fields = ['name', 'detail', 'id', 'added_by', 'favorited_by']

	def get_favorited_by(self, obj):
		favs = obj.favoriteitem_set.all()
		return len(favs)


class ItemDetailSerializer(serializers.ModelSerializer):

	favuser = serializers.SerializerMethodField()

	class Meta:
		model = Item
		fields = ['image', 'name', 'description', 'favuser', 'id']

	def get_favuser(self, obj):
		favorited_users = obj.favoriteitem_set.all()
		favuser = []
		for fav in favorited_users:
			favuser.append(fav.user)
		return UserSerializer(favuser, many=True).data

