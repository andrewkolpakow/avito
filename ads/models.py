from django.db import models
from django.db.models import UniqueConstraint
from django.core.validators import MinLengthValidator

from users.models import User

class Ad(models.Model):
    name = models.CharField(max_length=200, validators=[MinLengthValidator(10)])
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey("ads.Category", on_delete=models.CASCADE)
    is_published = models.BooleanField(default=False)
    image = models.ImageField(upload_to="ad_image", blank=True, null=True)

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"

    def __str__(self):
        return self.name
    # def serialize(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "author": self.author.username,
    #         "price": self.price,
    #         "description": self.description,
    #         "category": self.category.name,
    #         "is_published": self.is_published,
    #         "image": self.image.url if self.image else None
    #     }


class Selection(models.Model):
    name = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Ad)


    class Meta:
        verbose_name = "Подборка"
        verbose_name_plural = "Подборки"
        constraints = [UniqueConstraint(fields=["name", "owner"], name="my_constraint")]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=10, validators=[MinLengthValidator(5)]) #unique=True


    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }