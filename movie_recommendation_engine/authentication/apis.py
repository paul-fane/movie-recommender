from django.contrib.auth import authenticate, login, logout
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from movie_recommendation_engine.api.mixins import ApiAuthMixin
from movie_recommendation_engine.users.selectors import user_get_login_data


class UserSessionLoginApi(APIView):
    """
    Following https://docs.djangoproject.com/en/3.1/topics/auth/default/#how-to-log-a-user-in
    """

    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        password = serializers.CharField()

    def post(self, request):
        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(request, **serializer.validated_data)

        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        login(request, user)

        data = user_get_login_data(user=user)
        session_key = request.session.session_key

        return Response({"session": session_key, "data": data})


class UserSessionLogoutApi(APIView):
    def get(self, request):
        logout(request)

        return Response()

    def post(self, request):
        logout(request)

        return Response()



class UserMeApi(ApiAuthMixin, APIView):
    def get(self, request):
        data = user_get_login_data(user=request.user)

        return Response(data)