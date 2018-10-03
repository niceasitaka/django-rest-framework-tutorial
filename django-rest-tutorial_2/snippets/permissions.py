from rest_framework import permissions

# 업데이트와 삭제는 해당 코드를 만든 사용자만 할 수 있도록 커스텀 권한 구현
class IsOwnerOrReadOnly(permissions.BasePermission):
	"""
	객체의 소유자에게만 쓰기를 허용하는 커스텀 권한
	"""
	def has_object_permission(self, request, view, obj):
		# 읽기 권한은 모두에게 허용하므로,
		# GET, HEAD, OPTIONS 요청은 항상 허용함
		if request.method in permissions.SAFE_METHODS:
			return True

		# 쓰기 권한은 코드 조각의 소유자에게만 부여함
		return obj.owner == request.user