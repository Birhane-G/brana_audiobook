import frappe
import json
from frappe.utils import format_duration
"""
Brana Audiobook
This File Containe All Api's For Users basically for Authors 
"""
@frappe.whitelist(allow_guest=True)
def retrieve_authors(search=None, page=1, limit=20):
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
            "enabled": 1,
            "type" : "author",
                 },
        fields=[
                "full_name",
                "user_image",
                "email"
                ],
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )
    response_data = []
    for author in authors:
        author_image = f"https://{frappe.local.site}{author.user_image}"
        total_book_count = frappe.get_value(
            "Audiobook",
        filters={
            "author": author.email,
        },
        fieldname="COUNT(*)"
        )
        response_data.append({
            "full name": author.full_name,
            "author image": author_image,
            "total Book": total_book_count
        })
    # total_count = frappe.get_value(
    #     "User",
    # filters={
    #     "type": "author",
    # },
    # fieldname="COUNT(*)"
    # )
    # response_data.append({
    #     "Total Authors" : total_count
    # })
    return response_data
"""
It must check the argument if it is email or full name 
"""
@frappe.whitelist(allow_guest=True)
def retrieve_author(author_id):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    authors = frappe.get_all(
        "User",
        filters={
                "full_name" : author_id,
                 },
        fields=[
                "full_name",
                "user_image",
                'email',
                ],
    )
    response_data = []
    for author in authors:
        total_book_count = frappe.get_value(
            "Audiobook",
        filters={
            "disabled": 0,
            "author": author.email,
        },
        fieldname = "COUNT(*)"
        )
        books = frappe.get_all(
            "Audiobook",
        filters={
            "disabled": 0,
            "author": author.email,
        },
        fields=[
            "title",
            "description",
            "author",
            "narrator",
            "publisher",
            "thumbnail",
            "chapter",
            "sample_audio_title",
            "duration",
            "total_chapters_duration",
            ],
        )
        author_image = f"https://{frappe.local.site}{author.user_image}"
        author_image = f"https://{frappe.local.site}{author.user_image}"
        response_data.append({
            "name": author.full_name,
            "author image": author_image,
            "number of books" : total_book_count,
            "books": []
        })
        
        for book in books:
            narrator = frappe.get_doc("User", book.narrator)
            thumbnail_urls = f"https://{frappe.local.site}{book.thumbnail}"
            chapters = frappe.get_all("Audiobook Chapter", filters={ "audiobook": book.name }, fields=["title","duration"])
            total_chapter_count = frappe.get_value(
                "Audiobook Chapter",
                filters={"audiobook": book.name},
                fieldname="COUNT(title)")
            response_data[-1]["books"].append({
                "title": book.title,
                "description": book.description,
                "narrator": narrator.full_name,
                "thumbnail" : thumbnail_urls,
                "sample audiobook title": book.sample_audio_title,
                "duration": format_duration(book.duration),
                "total chapter": total_chapter_count,
                "total chapter duration": format_duration(book.total_chapters_duration),
                "chapters" : []
            })
            for chapter in chapters:
                response_data[-1]["chapters"].append({
                "title": chapter.title,
                "duration" : format_duration(chapter.duration)
            })

        return response_data