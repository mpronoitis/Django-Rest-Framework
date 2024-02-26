from .permissions import IsStaffEditorPermission
from rest_framework import permissions
from products.models import Product
class StaffEditorPermissionMixin():
    permission_classes = [permissions.IsAdminUser,IsStaffEditorPermission]


class UserQuerysetMixin():
    user_field = 'user' 
    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            user = self.request.user
            lookup_data = {}
            lookup_data[self.user_field] = user
            qs = super().get_queryset(*args, **kwargs)
            return qs.filter(**lookup_data)
        else:
           return Product.objects.none()
