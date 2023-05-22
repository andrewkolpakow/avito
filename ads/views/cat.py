import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView

from ads.models import Category, Ad


def index(request):
    return JsonResponse({"status": "ok"}, status=200)

@method_decorator(csrf_exempt, name="dispatch")
class CategoryListView(ListView):
    queryset = Category.objects.order_by("name")

    def get(self, request, *args, **kwargs):
        all_categories = Category.objects.all()
        return JsonResponse([cat.serialize() for cat in all_categories], safe=False)

@method_decorator(csrf_exempt, name="dispatch")
class CategoryCreateView(CreateView):
    model = Category
    fields = "__all__"

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        new_category = Category.objects.create(**data)
        return JsonResponse(new_category.serialize())

class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        return JsonResponse(self.get_object().serialize())

@method_decorator(csrf_exempt, name="dispatch")
class CategoryUpdateView (UpdateView):
    model = Category
    fields = "__all__"
    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        self.object.name = data.get("name")

        return JsonResponse(self.object.serialize())


class CategoryDeleteView(DeleteView):
    model = Category
    success_url = "/"

    def delete(self, request, *args, **kwargs):

        super().delete(request, *args, **kwargs)
        return JsonResponse({"status": "ok"})