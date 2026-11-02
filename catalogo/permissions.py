from rest_framework import permissions


class EsAutorOSoloLectura(permissions.BasePermission):
    """Leer: cualquiera. Editar o borrar: solo el autor (o el staff, para moderar)."""

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.usuario_id == request.user.id or request.user.is_staff


class EsStaffOSoloLectura(permissions.BasePermission):
    """Leer: cualquiera. Crear, editar o borrar: solo el staff."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff