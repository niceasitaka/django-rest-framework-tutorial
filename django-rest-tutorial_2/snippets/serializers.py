from django.forms import widgets

from rest_framework import serializers
from .models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES

# Django에서 Form 클래스와 ModelForm 클래스를 제공하듯, 
# REST 프레임워크에서도  Serializer 클래스와 ModelSerializer 클래스를 제공
# 아래 클래스의 내용을 단축적으로 사용 가능
class SnippetSerializer(serializers.ModelSerializer):
	class Meta:
		model = Snippet
		fields = ['id', 'title', 'code', 'linenos', 'language', 'style']

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
		
# ModelForm 클래스와 유사하게 동작함

'''