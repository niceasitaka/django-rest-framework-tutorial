# Serializer는 queryset과 모델 인스턴스와 같은 복잡한 데이터를 
# JSON, XML 또는 다른 콘텐츠 유형으로 쉽게 변환 가능
# ModelForm 클래스와 유사하게 동작함

from django.contrib.auth.models import User, Group

from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ['url', 'username', 'email', 'groups']
		
class GroupSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Group
		fields = ['url', 'name']