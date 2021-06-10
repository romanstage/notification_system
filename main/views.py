from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add user id to response
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['groups'] = list(user.groups.all().values('id', 'name'))
        # ...
        print(list(user.groups.all().values('id', 'name')))

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer





class TokenObtainPairPatchedSerializer(TokenObtainPairSerializer):
    def to_representation(self, instance):
        r = super(TokenObtainPairPatchedSerializer, self).to_representation(instance)
        r.update({'user': self.user.username})
        return r


class TokenObtainPairPatchedView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = TokenObtainPairPatchedSerializer

    token_obtain_pair = TokenObtainPairView.as_view()



class UserInfo(APIView):

    def get(self, request):
        user = request.user
        group = Group.objects.filter(user=user)
        data = {'last_name': user.last_name, 'first_name': user.first_name, 'group': group}
        return Response(data)
