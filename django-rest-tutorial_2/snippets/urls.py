from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
	path('', views.api_root),
    path('snippets/', views.SnippetList.as_view(), name='snippet-list'),
	path('snippets/<int:pk>/', views.SnippetDetail.as_view(), name='snippet-detail'),
	path('snippets/<int:pk>/highlight/', views.SnippetHighlight.as_view(), name='snippet-highlight'),
	path('users/', views.UserList.as_view(), name='user-list'),
	path('users/<int:pk>/', views.UserDetail.as_view(), name='user-detail'),
]

# 포맷의 다양한 접미어를 URL 형태로 전달받으려면 아래 함수 제공
# ex) http://example.com/api/items/4.json
urlpatterns = format_suffix_patterns(urlpatterns)