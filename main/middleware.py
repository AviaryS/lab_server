from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None and response.status_code == 422 or response.status_code == 403 or \
            response.status_code == 401:
        if context.get('request') and not context['request'].user.is_authenticated:
            response.data = {
                "error": {
                    'code': 403,
                    'message': 'Login failed'
                }
            }
            response.status_code = 403
        else:
            response.data = {
                "error": {
                    "code": 403,
                    "message": "Forbidden for you"
                }
            }
            response.status_code = 403
        return response
