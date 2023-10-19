import frappe
import json
"""
 * Brana Audiobook
 * This File Containe All Api's For Editors picks basically Authors 
"""

@frappe.whitelist(allow_guest=False)
def retrieve_editors_picks():
    """it return 1 if editors pic true else return 0"""
    # editors_picks = frappe.get_value(
    #     "Audiobook",
    #     filters={
    #         "title": audiobook_id, 
    #         },
    #     fieldname="editors_pick"
    # )
    editors_picks_audiobooks = frappe.get_all(
        "Audiobook",
        filters={
               "editors_pick": 1
                 },
        fields=[
                "name",
                "title",
                "author",
                "narrator",
                "publisher",
                "subscription_level",
                "audio_file",
                "thumbnail",
                "chapter",
                "total_listening_time",
                ],
        order_by="creation DESC"
    )
    response_data = []
    for editors_picks_audiobook in editors_picks_audiobooks:
        author = frappe.get_doc("User", editors_picks_audiobook.author)
        response_data.append({
            "thumbnail" : editors_picks_audiobook.thumbnail,
            "title": editors_picks_audiobook.name,
            "description": editors_picks_audiobook.description,
            "Author": author.full_name,
        })

    return response_data