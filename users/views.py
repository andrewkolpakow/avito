import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from users.models import User, Location
from django.core.paginator import Paginator
from django.db.models import Count, Q
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from users.serializers import UserSerializer, UserListSerializer, UserCreateUpdateSerializer, LocationSerializer



# TOTAL_ON_PAGE = 5
# @method_decorator(csrf_exempt, name="dispatch")
# class UserListView(ListView):
#     queryset = User.objects.prefetch_related("locations").annotate(
#         total_ads=Count("ad", filter=Q(ad__is_published=True)))
#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#         paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
#         page_number = request.GET.get("page")
#         users_on_page = paginator.get_page(page_number)
#
#
#         return JsonResponse({
#             "total": paginator.count,
#             "num_pages": paginator.num_pages,
#             "items": [{**user.serialize(), "total_ads":user.total_ads} for user in users_on_page]
#         }, safe=False)

class UserPaginator(PageNumberPagination):
    page_size = 4

class UserListView(ListAPIView):
    queryset = User.objects.prefetch_related("locations").annotate(
        total_ads=Count("ad", filter=Q(ad__is_published=True))).order_by('username')
    serializer_class = UserListSerializer
    pagination_class = UserPaginator
# @method_decorator(csrf_exempt, name="dispatch")
# class UserCreateView(CreateView):
#     model = User
#
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#
#         locations = data.pop("locations")
#         new_user = User.objects.create(**data)
#         for loc_name in locations:
#             loc, _ = Location.objects.get_or_create(name=loc_name)
#             new_user.locations.add(loc)
#
#         return JsonResponse(new_user.serialize())


# class UserDetailView(DetailView):
#     model = User
#
#     def get(self, request, *args, **kwargs):
#         return JsonResponse(self.get_object().serialize())

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer

class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# @method_decorator(csrf_exempt, name="dispatch")
# class UserUpdateView (UpdateView):
#     model = User
#     fields = "__all__"
#     def patch(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#         data = json.loads(request.body)
#
#         if "locations" in data:
#             locations = data.get("locations")
#             self.object.locations.clear()
#             for loc_name in locations:
#                 loc, _ = Location.objects.get_or_create(name=loc_name)
#                 self.object.locations.add(loc)
#         if "username" in data:
#             self.object.username = data["username"]
#
#
#         return JsonResponse(self.object.serialize())

# @method_decorator(csrf_exempt, name="dispatch")

# class UserDeleteView(DeleteView):
#     model = User
#     success_url = "/"
#
#     def delete(self, request, *args, **kwargs):
#
#         super().delete(request, *args, **kwargs)
#         return JsonResponse({"status": "ok"})
class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateSerializer

class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LocationViewSet(ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
