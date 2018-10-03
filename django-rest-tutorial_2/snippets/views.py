#from django.http import HttpResponse
#from django.http import Http404
#from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

#from rest_framework.renderers import JSONRenderer
#from rest_framework.parsers import JSONParser
#from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework import renderers
#from rest_framework.views import APIView
#from rest_framework import mixins
from rest_framework import generics
from rest_framework import permissions

from .models import Snippet
from .serializers import SnippetSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly

# request.data 는 json 요청 뿐만 아니라 yaml과 같은 다른 포맷도 다룰 수 있습니다.

'''
# HttpResponse의 하위 클래스를 만들고, 받은 데이터를 모두 json 형태로 반환
# 해당 클래스는 rest_framework.response 클래스의 Response 메소드를 통해서 json으로 변환 가능
class JSONResponse(HttpResponse):
	"""
	콘텐츠를 JSON으로 변환한 후 HttpResponse 형태로 반환합니다.
	"""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)
'''
'''		
# @csrf_exempt # 인증되지 않은 사용자도 이 뷰에 POST를 할 수 있도록
# 아래 장식자는 뷰에서 받은 Request에 몇몇 기능을 더하거나, 콘텐츠가 잘 변환되도록  Response에 특정 context를 추가하는 기능 제공
@api_view(['GET', 'POST'])
def snippet_list(request, format=None):
	"""
	코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
	"""
	# 모델 인스턴스 직렬화 (모델 불러오기 > 직렬화(파이썬 데이터형 변환)> JSON 변환)
	if request.method == 'GET':
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many=True)
		#return JSONResponse(serializer.data)
		return Response(serializer.data)
	
	# 반직렬화 (JSON 파싱 > 데이터형 변환 > 모델 인스턴스 화)
	elif request.method == 'POST':
		#data = JSONParser().parse(request)
		serializer = SnippetSerializer(data=request.data)
		# 위의 request.data는 request.POST와 비슷하나, 폼 데이터 뿐만이 아닌 아무 데이터나 다룰 수 있고, 'POST'뿐만 아니라 'PUT'과 'PATCH' 메서드에서도 사용 가
		if serializer.is_valid():
			serializer.save()
			#return JSONResponse(serializer.data, status=201)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		#return JSONResponse(serializer.errors, status=400)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
'''
# 위의 snippet_list 함수의 클래스 기반 뷰로 전환
class SnippetList(APIView):
	"""
	코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
	"""
	# 직렬화
	def get(self, request, format=None):
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many=True)
		return Response(serializer.data)
	
	# 반직렬화
	def post(self, request, format=None):
		serializer = SnippetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''
'''
# 위의 SnippetList 클래스를 mixin 을 통해 더욱 코드 간소화
"""
기본 뷰(GenericAPIView)는 핵심 기능을 제공하며,
믹스인 클래스들은 .list()나  .create() 기능을 제공
이 기능들을 get과 post 메서드에 적절히 연결
"""
class SnippetList(mixins.ListModelMixin,
					mixins.CreateModelMixin,
					generics.GenericAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	# 직렬화
	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	# 반직렬화
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)
'''

# 위의 SnippetList 클래스를 ListCreateAPIView 을 통해 또다시 더욱 코드 간소화
class SnippetList(generics.ListCreateAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer
	# IsAuthenticatedOrReadOnly는 인증 받은 요청에 읽기와 쓰기 권한을 부여하고, 인증 받지 않은 요청에 대해서는 읽기 권한만 부여
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	
	# 코드 조각을 만든 사용자를 연관시키기 위해 perform_create() 메소드를 오버라이딩
	# 해당 코드 조각을 작성한 사용자와 연결
	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)
		

################################################################################
		
'''		
# @csrf_exempt
@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail(request, pk, format=None):
	"""
	코드 조각 조회, 업데이트, 삭제
	"""
	try:
		snippet = Snippet.objects.get(pk=pk)
	except Snippet.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)

	# 직렬화
	if request.method == 'GET':
		serializer = SnippetSerializer(snippet)
		return Response(serializer.data)

	# 반직렬화
	# PUT 은 HTTP 업데이트 메소드
	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = SnippetSerializer(snippet, data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 폼 검증 에러

	# DELETE 는 HTTP 삭제 메소드
	elif request.method == 'DELETE':
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT) # 204 는 성공적으로 삭제된 요청의 응답 상태 코드
'''
'''
# 위의 snippet_detail 함수의 클래스 기반 뷰로 전환
class SnippetDetail(APIView):
    """
    코드 조각 조회, 업데이트, 삭제
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

	# 직렬화
    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

	# 반직렬화
    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	# DELETE 는 HTTP 삭제 메소드
    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
'''		
'''
# 위의 SnippetDetail 클래스를 mixin 을 통해 더욱 코드 간소화	
class SnippetDetail(mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer

	# 직렬화
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

	# 반직렬화
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

	# DELETE 는 HTTP 삭제 메소드
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
'''

# 위의 SnippetDetail 클래스를 RetrieveUpdateDestroyAPIView 을 통해 또다시 더욱 코드 간소화
class SnippetDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
							IsOwnerOrReadOnly,)
							# IsOwnerOrReadOnly 는 permissions 에서 커스텀으로 설정한 권한 부여함
	
################################################################################

# 사용자와 관련된 뷰
'''
- 코드 조각은 만든 사람과 연관이 있다.
- 인증받은 사용자만 코드 조각을 만들 수 있다.
- 해당 코드 조각을 만든 사람만, 이를 편집하거나 삭제할 수 있다.
- 인증받지 않은 사용자는 '읽기 전용'으로만 사용 가능하다.
'''
# 읽기 전용 뷰만 있으면 되니까, 제네릭 클래스 기반 뷰 중에서 ListAPIView와 RetrieveAPIView를 사용
class UserList(generics.ListAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	
################################################################################

# API의 최상단에 대한 엔드 포인트 만들기
# 지금까지 '코드 조각'과 '사용자'에 대한 엔드 포인트를 만들었지만, 아직까지 이렇다 할 API의 시작점은 없었기 때문에 이를 위한 함수 기반 뷰 구현
@api_view(['GET',])
def api_root(request, format=None):
	return Response({
		# urls.py 의 user-list 와 snippet-list (name) 으로 하이퍼링크
		'users': reverse('user-list', request=request, format=format),
		'snippets': reverse('snippet-list', request=request, format=format)
	})
	
################################################################################

# 코드 조각의 하이라이트 버전 보기
class SnippetHighlight(generics.GenericAPIView):
	queryset = Snippet.objects.all()
	renderer_classes = (renderers.StaticHTMLRenderer,)

	def get(self, request, *args, **kwargs):
		snippet = self.get_object()
		return Response(snippet.highlighted)
