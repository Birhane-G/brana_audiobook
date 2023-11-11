import frappe


@frappe.whitelist(allow_guest=True)
def retrieve_profile():
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    
    profile = frappe.get_doc("User", frappe.session.user)
        
    email = profile.email
    first_name = profile.first_name
    last_name = profile.last_name
    username = profile.username
    profile_image = f"https://{frappe.local.site}{profile.user_image}"
    
    return {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "username": username,
        "profile_url": profile_image
    }