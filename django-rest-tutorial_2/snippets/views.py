from django.http import HttpResponse
#from django.views.decorators.csrf import csrf_exempt

#from rest_framework.renderers import JSONRenderer
#from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

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
		
# request.data 는 json 요청 뿐만 아니라 yaml과 같은 다른 포맷도 다룰 수 있습니다