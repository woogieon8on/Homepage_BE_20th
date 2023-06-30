from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

class ApiAuthMixin:
    # authenticated_classes = (CsrfExemptedSessionAuthentication, )
    permission_classes = (IsAuthenticated, )

class ApiAdminAuthMixin:
    permission_classes = (IsAdminUser, )

class ApiAllowAnyMixin:
    permission_classes = (AllowAny, )