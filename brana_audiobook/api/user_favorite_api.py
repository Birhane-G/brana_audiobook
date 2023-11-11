import frappe
from frappe import _
@frappe.whitelist(allow_guest=True)
def favorite(title):
    # check the title is available on audiobook or podcast list before save
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    user = frappe.get_doc("User", frappe.session.user)
    try:
        favorite = frappe.get_doc("Brana User Profile", user.email)
        if favorite:
            favorite = frappe.get_doc("Brana User Profile", user.email)
            if not favorite.wish_list:
                favorite_item = favorite.append("wish_list", {})
                favorite_item.title = title
                favorite_item.favourite = 1
                favorite.save()
                return "Favourite"
            else:
                for item in favorite.wish_list:
                    if item.title == title:
                        favorite.remove(item)
                        favorite.save()
                        # item.favourite = 0
                        return "Remove Favourite"
        else:
            favorite = frappe.new_doc("Brana User Profile")
            favorite.user = user.email
            favorite.user_name = user.full_name
            favorite_item = favorite.append("wish_list", {})
            favorite_item.title = title
            favorite_item.favourite = 1
            favorite.save()
            return "Favourite"
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error")
        return {"message": _("Favourite Error")}