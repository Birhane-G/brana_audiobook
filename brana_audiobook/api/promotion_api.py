import frappe

@frappe.whitelist(allow_guest=True)
def promotion(search=None, page=1, limit=20):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    filters = []
    if search:
        filters.append(f"(ab.title LIKE '%{search}%' OR aut.name LIKE '%{search}%' OR nar.name LIKE '%{search}%')")
    filters_str = " AND ". join(filters)
    offset = (page - 1) * limit
    promotions = frappe.get_all(
        "Promotion",
        filters={
            "disabled": 0,
                 },
        fields=[
                "image",
                "header",
                "description",
                ],
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )
    response_data=[]
    for promotion in promotions:
        thumbnail_url = f"https://{frappe.local.site}{promotion.image}"
        response_data.append({
            "image" : thumbnail_url,
            "header": promotion.header,
            "description": promotion.description
        })
        
    return response_data