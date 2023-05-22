import datetime

from rest_framework.serializers import ModelSerializer
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import SlugRelatedField

from ads.models import Ad, Category, Selection
from users.models import User
from users.serializers import UserListSerializer, LocationSerializer


class UserAdSerializer(ModelSerializer):
    locations = LocationSerializer(many=True)
    age_of_born = SerializerMethodField()

    def get_age_of_born(self, obj):
        return datetime.date.today().year - obj.age


    class Meta:
        model = User
        fields = ["locations", "username", "age_of_born"]


class AdSerializer(ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"


class AdListSerializer(ModelSerializer):
    category = SlugRelatedField(slug_field="name", queryset=Category.objects.all())
    user_locations = SerializerMethodField()

    def get_user_locations(self, obj):
        return [loc.name for loc in obj.author.locations.all()]

    class Meta:
        model = Ad
        fields = ["name", "price", "category", "user_locations"]


class AdDetailSerializer(ModelSerializer):
    author = UserAdSerializer()
    category = SlugRelatedField(slug_field="name", queryset=Category.objects.all())


    class Meta:
        model = Ad
        fields = "__all__"

class SelectionSerializer(ModelSerializer):
    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(ModelSerializer):
    owner = SlugRelatedField(slug_field="username", read_only=True)

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["owner"] = request.user
        return super().create(validated_data)
    class Meta:
        model = Selection
        fields = '__all__'
