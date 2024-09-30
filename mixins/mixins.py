from rest_framework.response import Response
from rest_framework import status


class RequiredParamsMixin:
    required_params = []

    def check_required_params(self, data):
        missing_params = [param for param in self.required_params if param not in data]
        if missing_params:
            return Response({
                "detail": f"Missing parameter(s): {', '.join(missing_params)}"
            }, status=status.HTTP_400_BAD_REQUEST)
        return None
