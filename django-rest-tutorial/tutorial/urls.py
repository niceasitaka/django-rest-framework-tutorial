from django.contrib import admin
from django.urls import path, include

from rest_framework import routers

from .quickstart import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', include(router.urls)),
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

'''
routers 는 logic과 어플리케이션을 위한 URL을 어떻게 매핑할지를 자동으로 결정하는 기능 제공

register() 메소드는 2개의 필수 arg가 있음
- prefix : route의 집합들을 사용하기 위한 URL prefix
- viewset : views의 viewset 클래스(rest_framework의 viewsets을 부모로 함)
'''