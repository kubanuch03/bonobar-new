from django.db.models import Q


def build_filters(params):
    filters = Q()
    if params['date_param']:
        filters &= Q(will_come=params['date_param'])
    if params['status_param'] is not None:
        filters &= Q(is_come=params['status_param'])
    if params['search_form']:
        filters &= (Q(user_name__icontains=params['search_form']) | Q(phone_number__icontains=params['search_form']))
    return filters
