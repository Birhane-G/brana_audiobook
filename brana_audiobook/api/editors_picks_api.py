import frappe
import json
"""
 * Brana Audiobook
 * This File Containe All Api's For Editors picks basically Authors 
"""

@frappe.whitelist(allow_guest=False)
def retrieve_editors_picks(audiobook_id):
    editors_pick = frappe.get_value(
        "Audiobook",
        filters={
            "title": audiobook_id, 
            },
        fieldname="editors_pick"
    )
    return editors_pick