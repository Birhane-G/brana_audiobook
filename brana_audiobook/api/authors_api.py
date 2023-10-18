import frappe
import json
"""
 * Brana Audiobook
 * This File Containe All Api's For Users basically Authors 
"""
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
                "type" : "author",
                 },
        fields=[
                "full_name",
                "user_image",
                'email',
                # "type"
                ],
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )
   
    response_data = []
    for author in authors:
        total_book_count = frappe.get_value(
            "Audiobook",
        filters={
            "author": author.email,
        },
        fieldname="COUNT(*)"
        )
        response_data.append({
            "Name": author.full_name,
            "user Image": author.user_image,
            "Email": author.email,
            "Total Book": total_book_count
        })

    total_count = frappe.get_value(
        "User",
    filters={
        "type": "author",
    },
    fieldname="COUNT(*)"
    )
    response_data.append({
        "Total Authors" : total_count
    })

    return response_data



@frappe.whitelist(allow_guest=False)
def retrieve_author(author_id):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    author = frappe.get_doc("User", author_id)

    return author.full_name