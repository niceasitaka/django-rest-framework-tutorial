from django.contrib.auth.models import User, Group

from rest_framework import viewsets

from .serializers import UserSerializer, GroupSerializer

# 사용자 보거나 편집하는 API
class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

# 그룹을 보거나 편집하는 API
class GroupViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = GroupSerializer
	
'''
일반적인 경우 ViewSet 클래스에 model 속성만 설정하면 serializer와 queryset은 
자동으로 설정됩니다. queryset이나 serializer_class 속성을 설정하면 API의 행동을 좀더 
명시적으로 표현할 수 있는데 대다수 애플리케이션에서는 이렇게 하기를 권장합니다.
'''

