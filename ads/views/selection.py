from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.viewsets import ModelViewSet

from ads.serializers import SelectionSerializer, SelectionCreateSerializer
from ads.models import Selection

class SelectionViewSet(ModelViewSet):
    queryset = Selection.objects.all()
    serializers = {
        "create": SelectionCreateSerializer
    }
    default_serializer = SelectionSerializer

    permissions = {"retrieve": [IsAuthenticated], "create": [IsAuthenticated]}
    default_permission = [AllowAny]

    def get_permissions(self):
        self.permission_classes = self.permissions.get(self.action, self.default_permission)
        return super().get_permissions()

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.default_serializer)