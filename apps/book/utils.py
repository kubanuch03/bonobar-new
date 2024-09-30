from rest_framework import status
from django.http import JsonResponse


def validate_date(date_param):
    if date_param is None:
        return None
    try:
        from datetime import datetime
        datetime.strptime(date_param, '%Y-%m-%d')
        return None
    except ValueError:
        return "Invalid date format. Expected format is YYYY-MM-DD."


def validate_int(value, name):
    try:
        return int(value), None
    except ValueError:
        return None, f"Invalid {name}. {name.capitalize()} should be an integer."


def validate_status(param, param_name):
    if param is not None:
        if param == '0':
            return False, None
        elif param == '1':
            return True, None
        else:
            return None, f'“{param}” value for {param_name} must be either 0 or 1.'
    return None, None


def validate_params(request):
    date_param = request.query_params.get('date')
    status_param = request.query_params.get('status')
    floor_param = request.query_params.get('floor')
    search_form = request.query_params.get('search_form')
    table_param = request.query_params.get('table')

    date_error = validate_date(date_param)
    if date_error:
        return None, JsonResponse({'error': date_error}, status=status.HTTP_400_BAD_REQUEST)

    status_param, status_error = validate_status(status_param, "status")
    if status_error:
        return None, JsonResponse({'error': status_error}, status=status.HTTP_400_BAD_REQUEST)

    floor_param, floor_error = validate_int(floor_param, "floor") if floor_param else (None, None)
    if floor_error:
        return None, JsonResponse({'error': floor_error}, status=status.HTTP_400_BAD_REQUEST)

    table_param, table_error = validate_status(table_param, "table")
    if table_error:
        return None, JsonResponse({'error': table_error}, status=status.HTTP_400_BAD_REQUEST)

    return {
        'date_param': date_param,
        'status_param': status_param,
        'floor_param': floor_param,
        'search_form': search_form,
        'table_param': table_param
    }, None