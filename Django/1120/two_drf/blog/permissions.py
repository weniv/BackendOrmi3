from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    # R은 모두 허용
    # C로그인 사용자 허용
    # UD는 작성자만 허용
    def has_permission(self, request, view):
        '''
        GET, HEAD, OPTIONS 요청은 인증 여부와 상관없이 항상 True를 리턴합니다.
        '''
        if request.method in permissions.SAFE_METHODS:
            return True
        
    def has_object_permission(self, request, view, obj):
        '''
        GET, HEAD, OPTIONS 요청은 인증 여부와 상관없이 항상 True를 리턴합니다. 그 외 요청(PUT, DELETE)에 대해서는 작성자에 한해서만 True를 리턴합니다.
        '''
        if request.method in permissions.SAFE_METHODS:
            return True