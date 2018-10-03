from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', include('snippets.urls')),
	# 탐색 가능한 API의 로그인 뷰와 로그아웃 뷰에 사용
	path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
