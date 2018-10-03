from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    path('snippets/', views.snippet_list),
	path('snippets/<int:pk>/', views.snippet_detail),
]

# 포맷의 다양한 접미어를 URL 형태로 전달받으려면 아래 함수 제공
# ex) http://example.com/api/items/4.json
urlpatterns = format_suffix_patterns(urlpatterns)