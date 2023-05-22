import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from users.models import User
from django.core.paginator import Paginator
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from ads.models import Category, Ad
from ads.serializers import AdSerializer, AdDetailSerializer, AdListSerializer



# class AdListCreateView(View):
#
#     def get(self, request):
#         all_ads = Ad.objects.all()
#         return JsonResponse([ad.serialize() for ad in all_ads], safe=False)
#
#     def post(self, request):
#         data = json.loads(request.body)
#         new_ad = Ad.objects.create(**data)
#         return JsonResponse(new_ad.serialize(), safe = False)

# TOTAL_ON_PAGE = 5
# @method_decorator(csrf_exempt, name="dispatch")
# class AdListView(ListView):
#     queryset = Ad.objects.order_by("-price")
#     def get(self, request, *args, **kwargs):
#         super().get(request, *args, **kwargs)
#         paginator = Paginator(self.object_list, TOTAL_ON_PAGE)
#         page_number = request.GET.get("page")
#         ads_on_page = paginator.get_page(page_number)
#
#
#         return JsonResponse({
#             "total": paginator.count,
#             "num_pages": paginator.num_pages,
#             "items": [ad.serialize() for ad in ads_on_page]
#         }, safe=False)
#
# @method_decorator(csrf_exempt, name="dispatch")
# class AdCreateView(CreateView):
#     model = Ad
#
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#
#         author = get_object_or_404(User, pk=data.pop("author"))
#         category = get_object_or_404(Category, pk=data.pop("category"))
#
#         new_ad = Ad.objects.create(author=author, category=category, **data)
#         return JsonResponse(new_ad.serialize())
#
#
# class AdDetailView(DetailView):
#     model = Ad
#
#     def get(self, request, *args, **kwargs):
#         return JsonResponse(self.get_object().serialize())
#
#
#     def post(self, request, *args, **kwargs):
#         data = json.loads(request.body)
#         new_category = Category.objects.create(**data)
#         return JsonResponse(new_category.serialize())
#
#
#
# @method_decorator(csrf_exempt, name="dispatch")
# class AdUpdateView (UpdateView):
#     model = Ad
#     fields = "__all__"
#     def patch(self, request, *args, **kwargs):
#         super().post(request, *args, **kwargs)
#         data = json.loads(request.body)
#
#         if "name" in data:
#             self.object.name = data.get("name")
#         if "price" in data:
#             self.object.price = data.get("price")
#         if "author_id" in data:
#             author = get_object_or_404(User, pk=data.get("author_id"))
#             self.object.author = author
#         if "category" in data:
#             category = get_object_or_404(Category, name=data.get("category"))
#             self.object.category = category
#
#         return JsonResponse(self.object.serialize())
#
# @method_decorator(csrf_exempt, name="dispatch")
#
# class AdDeleteView(DeleteView):
#     model = Ad
#     success_url = "/"
#
#     def delete(self, request, *args, **kwargs):
#
#         super().delete(request, *args, **kwargs)
#         return JsonResponse({"status": "ok"})

class AdViewSet(ModelViewSet):
    queryset = Ad.objects.all().order_by("-price")
    serializers = {"list": AdListSerializer, "retrieve": AdDetailSerializer}
    default_serializer = AdSerializer

    permissions = {"retrieve": [IsAuthenticated]}
    default_permission = [AllowAny]

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.default_permission)
        return super().get_permissions()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        cat_list = request.GET.get("cat")
        if cat_list:
            self.queryset = self.queryset.filter(category_id__in=cat_list)

        text = request.GET.get("text")
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get("location")
        if location:
            self.queryset = self.queryset.filter(author__locations__name__icontains=location)

        price_from = request.GET.get("price_from")
        if price_from and not price_from.isdigit():
            return Response(data={"message": "price must be int"},status=status.HTTP_400_BAD_REQUEST)
        elif price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)

        price_to = request.GET.get("pirce_to")
        if price_to and not price_to.isdigit():
            return Response(data={"message": "price must be int"}, status=status.HTTP_400_BAD_REQUEST)
        elif price_to:
            self.queryset = self.queryset.filter(price_lte=price_to)

        return super().list(request, *args, **kwargs)

@method_decorator(csrf_exempt, name="dispatch")
class AdUploadImageView (UpdateView):
    model = Ad
    fields = "__all__"
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        self.object.image = request.FILES.get("image")
        self.object.save()

        return JsonResponse(self.object.serialize())
