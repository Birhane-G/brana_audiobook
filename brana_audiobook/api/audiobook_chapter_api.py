import frappe

def get_audiobook_chapter_list(audiobook):
    # Custom function to retrieve a list of Audiobook Chapters for a given Audiobook
    chapters = frappe.get_all(
        "Audiobook Chapter",
        filters={"audiobook": audiobook},
        fields=["name", "title", "description", "audiobook", "audio_file", "total_listening_time"]
    )
    return chapters
