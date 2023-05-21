from rest_framework.authentication import TokenAuthentication


class CustomTokAuth(TokenAuthentication):
    keyword = 'Bearer'