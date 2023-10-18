import frappe
import json


@frappe.whitelist(allow_guest=False)
def retrive_authors(search=None, page=1, limit=20):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    filters = []
    if search:
        filters.append(f"(ab.title LIKE '%{search}%' OR aut.name LIKE '%{search}%' OR nar.name LIKE '%{search}%')")
    filters_str = " AND ".join(filters)
    offset = (page - 1) * limit

    authors = frappe.get_all(
        "User",
        filters={
                #  "docstatus": 1,
                #  "disabled": 0,
                #  "subscription_level": ("!=", "")
                 },
        fields=[
                "full_name",
                "user_image",
                "type"
                ],
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )
    total_count = frappe.get_value(
        "User",
        fieldname="COUNT(first_name)"
        )

    return authors