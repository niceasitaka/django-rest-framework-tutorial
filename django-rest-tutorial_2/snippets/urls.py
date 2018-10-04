from django.urls import path, include

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from rest_framework.routers import DefaultRouter

from . import views

'''
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
'''

'''
# 뷰셋의 뷰들을 명시적으로 표시
# ViewSet 클래스를 실제 뷰(concrete view)와 연결
# HTTP 메서드에 실제 뷰와 연결
snippet_list = views.SnippetViewSet.as_view({
	'get': 'list',
	'post': 'create'
})
snippet_detail = views.SnippetViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'patch': 'partial_update',
	'delete': 'destroy'
})
snippet_highlight = views.SnippetViewSet.as_view({
	'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])
user_list = views.UserViewSet.as_view({
	'get': 'list'
})
user_detail = views.UserViewSet.as_view({
	'get': 'retrieve'
})

urlpatterns = format_suffix_patterns([
	path('', views.api_root),
	path('snippets/', snippet_list, name='snippet-list'),
	path('snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
	path('snippets/<int:pk>/highlight/', snippet_highlight, name='snippet-highlight'),
	path('users/', user_list, name='user-list'),
	path('users/<int:pk>/', user_detail, name='user-detail')
])
'''

"""
View 클래스 대신 ViewSet 클래스를 사용했기 때문에, 이제는 URL도 설정할 필요가 없다.
Router 클래스를 사용하면 뷰 코드와 뷰, URL이 관례적으로 자동 연결된다.

"""
# 라우터를 생성하고 '뷰셋'을 등록
# DefaultRouter 클래스는 API의 최상단 뷰를 자동으로 생성
router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

# 이제 API URL을 라우터가 자동으로 인식합니다
# 추가로 탐색 가능한 API를 구현하기 위해 로그인에 사용할 URL은 직접 설정을 했습니다
urlpatterns = [
	path('', include(router.urls)),
]
