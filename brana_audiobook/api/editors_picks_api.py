import frappe
import json
"""
 * Brana Audiobook
 * This File Containe All Api's For Editors picks basically Authors 
"""

@frappe.whitelist(allow_guest=False)
def retrieve_editors_picks(search=None, page=1,limit=20):
    return "Work"