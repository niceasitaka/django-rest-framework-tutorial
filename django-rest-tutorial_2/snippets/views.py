from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

# HttpResponse의 하위 클래스를 만들고, 받은 데이터를 모두 json 형태로 반환
class JSONResponse(HttpResponse):
	"""
	콘텐츠를 JSON으로 변환한 후 HttpResponse 형태로 반환합니다.
	"""
	def __init__(self, data, **kwargs):
		content = JSONRenderer().render(data)
		kwargs['content_type'] = 'application/json'
		super(JSONResponse, self).__init__(content, **kwargs)
		
@csrf_exempt # 인증되지 않은 사용자도 이 뷰에 POST를 할 수 있도록
def snippet_list(request):
	"""
	코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
	"""
	# 모델 인스턴스 직렬화 (모델 불러오기 > 직렬화(파이썬 데이터형 변환)> JSON 변환)
	if request.method == 'GET':
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many=True)
		return JSONResponse(serializer.data)
	
	# 반직렬화 (JSON 파싱 > 데이터형 변환 > 모델 인스턴스 화)
	elif request.method == 'POST':
		data = JSONParser().parse(request)
		serializer = SnippetSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data, status=201)
		return JSONResponse(serializer.errors, status=400)
		
		
@csrf_exempt
def snippet_detail(request, pk):
	"""
	코드 조각 조회, 업데이트, 삭제
	"""
	try:
		snippet = Snippet.objects.get(pk=pk)
	except Snippet.DoesNotExist:
		return HttpResponse(status=404)

	# 직렬화
	if request.method == 'GET':
		serializer = SnippetSerializer(snippet)
		return JSONResponse(serializer.data)

	# 반직렬화
	# PUT 은 HTTP 업데이트 메소드
	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = SnippetSerializer(snippet, data=data)
		if serializer.is_valid():
			serializer.save()
			return JSONResponse(serializer.data)
		return JSONResponse(serializer.errors, status=400) # 폼 검증 에러

	# DELETE 는 HTTP 삭제 메소드
	elif request.method == 'DELETE':
		snippet.delete()
		return HttpResponse(status=204) # 204 는 성공적으로 삭제된 요청의 응답 상태 코드
		
		
		
