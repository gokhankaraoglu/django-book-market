from rest_framework import permissions

class IsAdminUserReadOnly(permissions.IsAdminUser):
  def has_permission(self,request, view):
    is_admin = super().has_permission(request, view)
    return request.method in permissions.SAFE_METHODS or is_admin

class IsCommentByOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request in permissions.SAFE_METHODS:
            return True

        return request.user == obj.comment_by