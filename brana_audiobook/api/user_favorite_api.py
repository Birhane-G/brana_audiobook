import frappe

@frappe.whitelist(allow_guest=True)
def favorite(title):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    
    user = frappe.get_doc("User", frappe.session.user)
    favorite = frappe.new_doc("Brana User Profile")
    favorite.user = user.email
    # user.insert()
    user.save()
    
    return {
        "message": favorite
    }