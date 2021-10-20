from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN


def auth_decorator(auth=False, admin=False):
    auth_err_messsage = {'message': 'user not allowed'}

    def decorator(request_function):
        def wrapper(self, request, *args, **kwargs):
            if(auth or admin):
                user_data = request.user
                if(not user_data):
                    return Response(data=auth_err_messsage, status=HTTP_401_UNAUTHORIZED)
                if(admin and not user_data.is_staff):
                    return Response(data=auth_err_messsage, status=HTTP_403_FORBIDDEN)
            return request_function(self, request, *args, **kwargs)
        return wrapper
    return decorator
