from src.core._shared.entity import ListOutputMeta


def output_entity(input, items):
    if input.order_by:
        items = sorted(
            items,
            key=lambda i: getattr(i, input.order_by),
        )

    page_offset = (input.current_page - 1) * input.per_page
    paginated_items = items[page_offset : page_offset + input.per_page]

    return ListOutputMeta(
        current_page=input.current_page,
        per_page=input.per_page,
        total=len(items),
    ), paginated_items
