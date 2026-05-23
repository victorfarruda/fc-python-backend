def get_params(request):
    order_by = request.query_params.get("order_by", "name")
    current_page = int(request.query_params.get("current_page", 1))
    per_page = int(request.query_params.get("per_page", 2))
    return order_by, current_page, per_page
