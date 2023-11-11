import frappe

@frappe.whitelist(allow_guest=True)
def favorite(title):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    
    user = frappe.get_doc("User", frappe.session.user)
    favorite = frappe.new_doc("Brana User Profile")
    favorite.user = user.email
    favorite.user_name = user.full_name
    
    favorite_item = favorite.append("wish_list", {})
    favorite_item.title = title
    favorite_item.favourite = 1
    
    favorite.save()
    
    return {
        "message": "sucess"
    }