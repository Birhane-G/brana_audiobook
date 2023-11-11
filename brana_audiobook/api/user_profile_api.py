import frappe
from frappe import _

@frappe.whitelist(allow_guest=True)
def retrieve_profile():
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    
    user_profile = frappe.get_doc("User", frappe.session.user)
        
    return user_profile