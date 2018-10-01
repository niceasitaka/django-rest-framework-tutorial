from django.contrib.auth.models import User, Group

from rest_framework import viewsets

from .serializers import UserSerializer, GroupSerializer

# 사용자 보거나 편집하는 API
class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

# 그룹을 보거나 편집하는 API
class GroupViewSet(viewsets.ModelViewSet):
	queryset = Group.objects.all()
	serializer_class = GroupSerializer
	
'''
일반적인 경우 ViewSet 클래스에 model 속성만 설정하면 serializer와 queryset은 
자동으로 설정.
queryset이나 serializer_class 속성을 설정하면 API의 행동을 좀더 
명시적으로 표현할 수 있는데 대다수 애플리케이션에서는 이렇게 하기를 권장.

viewsets 클래스를 사용하면 view 클래스보다 좋은점
- routers를 통해 더이상 사용자 스스로 URL 설정파일을 다룰 필요가 없음

뷰를 여러 번 작성하기보다는 자주 사용되는 기능들을 묶은 ViewSet 클래스를 사용

물론 필요에 따라 뷰를 잘게 나눌 수도 있습니다. 하지만 뷰셋(viewset)을 사용하면 뷰 로직을 아주 간결하고 체계적으로 유지 가능
'''

