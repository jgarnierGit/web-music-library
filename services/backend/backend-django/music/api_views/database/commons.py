from rest_framework.response import Response
from rest_framework import status


def extract_get_params_cards(request):
    limit = request.query_params.get("limit", 10)
    if limit:
        try:
            limit = int(limit)
        except ValueError:
            return Response(
                {"error": "Invalid limit value"}, status=status.HTTP_400_BAD_REQUEST
            )
    offset = request.query_params.get("offset", 0)
    if offset:
        try:
            offset = int(offset)
        except ValueError:
            return Response(
                {"error": "Invalid offset value"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    return limit, offset


def extract_post_params_cards(request):
    param = request.data
    offset = 0
    limit = 10
    filters = []
    if param:
        offset = param.get("offset", 0)
        limit = param.get("limit", 10)
        filters = param.get("filters", [])
    return limit, offset, filters
