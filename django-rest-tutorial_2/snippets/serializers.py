from django.contrib.auth.models import User


from rest_framework import serializers
from .models import Snippet
# from .models import LANGUAGE_CHOICES, STYLE_CHOICES

'''
# SnippetSerializer 클래스는 Snippet 모델의 정보들을 그대로 베낌
class SnippetSerializer(serializers.Serializer):\
	# 직렬화/반직렬화될 필드를 선언
	# 직렬화 = 모델 인스턴스(DB데이터)를 파이썬의 데이터 타입(사전형)으로 변환 후 JSON으로 변환함
	# 반직렬화 = 직렬화의 반대 과정, JSON -> 파이썬의 데이터 타입 -> 데이터의 모델 인스턴스화
	pk = serializers.IntegerField(read_only=True)
	title = serializers.CharField(required=False, allow_blank=True, max_length=100)
	code = serializers.CharField(style={'base_template': 'textarea.html'})
	linenos = serializers.BooleanField(required=False)
	language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
	style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

	
	# create() 메서드와 update() 메서드에서는 serializer.save()가 호출되었을 때 
	# 인스턴스가 생성 혹은 수정되는 과정을 전부 명시
	def create(self, validated_data):
		"""
		검증한 데이터로 새 `Snippet` 인스턴스를 생성하여 리턴합니다.
		"""
		return Snippet.objects.create(**validated_data)

	def update(self, instance, validated_data):
		"""
		검증한 데이터로 기존 `Snippet` 인스턴스를 업데이트한 후 리턴합니다.
		"""
		instance.title = validated_data.get('title', instance.title)
		instance.code = validated_data.get('code', instance.code)
		instance.linenos = validated_data.get('linenos', instance.linenos)
		instance.language = validated_data.get('language', instance.language)
		instance.style = validated_data.get('style', instance.style)
		instance.save()
		return instance
'''
'''
# ModelForm 클래스와 유사하게 동작함
# Django에서 Form 클래스와 ModelForm 클래스를 제공하듯, 
# REST 프레임워크에서도  Serializer 클래스와 ModelSerializer 클래스를 제공
# 아래 클래스의 내용을 단축적으로 사용 가능
class SnippetSerializer(serializers.ModelSerializer):
	# ReadOnlyField는 직렬화에 사용되었을 땐 언제나 읽기 전용이므로, 모델의 인스턴스를 업데이트할 때는 사용할 수 없음
	owner = serializers.ReadOnlyField(source='owner.username')

	class Meta:
		model = Snippet
		fields = ['id', 'title', 'code', 'linenos', 'language', 'style', 'owner']

# 'snippets'는 사용자 모델과 '반대 방향'으로 이어져 있기 때문에 ModelSerializer에 기본적으로 추가되지 않음. 따라서 명시적으로 필드를 지정 필요.
class UserSerializer(serializers.ModelSerializer):
	snippets = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

	class Meta:
		model = User
		fields = ['id', 'username', 'snippets']
'''		
		
"""
- 위의 코드는 API에서 '관계'는 주 키(primary key)로 나타나고 있었음
- 지금은 하이퍼링크 방식으로 변경할 것임
- ModelSerializer를 HyperlinkedModelSerializer로 변경 필요
"""

"""
yperlinkedModelSerializer는 다음과 같은 점들이 다름

- pk 필드는 기본 요소가 아닙니다.
- HyperlinkedIdentityField를 사용하는 url 필드가 포함되어 있습니다.
- 관계는 PrimaryKeyRelatedField 대신 HyperlinkedRelatedField 를 사용하여 나타냅니다.
"""
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')
	# highlight 필드에 하이퍼링크된 url 표시 > urls.py 의 snippet-highlight (name) 과 매치
	highlight = serializers.HyperlinkedIdentityField(view_name='snippet-highlight', format='html')

	class Meta:
		model = Snippet
		fields = ['url', 'highlight', 'owner',
					'title', 'code', 'linenos', 'language', 'style']
	# 새롭게 'highlight' 필드가 추가
	# 이 필드는 url 필드와 같은 타입이며, 'snippet-detail' url 패턴 대신 'snippet-highlight' url 패턴을 가리킴

class UserSerializer(serializers.HyperlinkedModelSerializer):
	snippets = serializers.HyperlinkedRelatedField(many=True, view_name='snippet-detail', read_only=True)

	class Meta:
		model = User
		fields = ['url', 'username', 'snippets']