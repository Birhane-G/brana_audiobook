import frappe
import json
import mimetypes
import subprocess
import os
from flask import Flask, send_file, request
from werkzeug.utils import secure_filename
from flask import send_file
from frappe.utils import format_duration

app = Flask(__name__)
"""
This function retrieve all audiobook available in the 
Brana Audiobook collection That is not disabled
"""
@frappe.whitelist(allow_guest=True)
def retrieve_audiobooks(search=None, page=1, limit=20):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    filters = []
    if search:
        filters.append(f"(ab.title LIKE '%{search}%' OR aut.name LIKE '%{search}%' OR nar.name LIKE '%{search}%')")
    filters_str = " AND ". join(filters)
    offset = (page - 1) * limit
    audiobooks = frappe.get_all(
        "Audiobook",
        filters={
            "disabled": 0,
                 },
        fields=[
                "name",
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
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )
    if audiobooks:
        total_audiobook_count = frappe.get_value(
        "Audiobook",
        filters={
                 "disabled": 0,
                 },
        fieldname="COUNT(title)"
    )
        response_data = []
        for audiobook in audiobooks:
            author = frappe.get_doc("User", audiobook.author)
            narrator = frappe.get_doc("User", audiobook.narrator)
            chapters = frappe.get_all("Audiobook Chapter", filters={ "audiobook": audiobook.name }, fields=["title","duration"])
            thumbnail_url = f"https://{frappe.local.site}{audiobook.thumbnail}"
            total_chapter_count = frappe.get_value(
                "Audiobook Chapter",
                filters={
                    "audiobook": audiobook.name
                },
                fieldname="COUNT(title)")
            response_data.append({
                "title": audiobook.title,
                "description": audiobook.description,
                "author": author.full_name,
                "narrator": narrator.full_name,
                "thumbnail": thumbnail_url,
                "Sample Audiobook Title": audiobook.sample_audio_title,
                "duration": format_duration(audiobook.duration),
                "Total chapter": total_chapter_count,
                "Total chapter Duration": format_duration(audiobook.total_chapters_duration),
                "chapters" : []
        })
            for chapter in chapters:
                response_data[-1]["chapters"].append({
                "title": chapter.title,
                "duration" : format_duration(chapter.duration)
            })
        response_data.append({
            "Total Audiobook": total_audiobook_count
            })
        return response_data
    else:
        return "No Audiobook found."

@frappe.whitelist(allow_guest=True)
def retrieve_audiobook(audiobook_id):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    # Perform user role and permission checks here
    # ...
    # Ensure the authenticated user has the necessary roles and permissions to access the API method
    audiobook = frappe.get_doc("Audiobook", audiobook_id)
    # Retrieve User Favorite
    user_favorite = frappe.get_value(
        "User Favorite",
        filters={"user": frappe.session.user, "audio_content": audiobook_id},
        fieldname="name"
    )
    # is_favorite = False
    # if user_favorite:
    #     is_favorite = True
    author = frappe.get_doc("User", audiobook.author)
    narrator = frappe.get_doc("User", audiobook.narrator)
    thumbnail_url = f"https://{frappe.local.site}{audiobook.thumbnail}"
    chapters = frappe.get_all("Audiobook Chapter", filters={ "audiobook": audiobook.name }, fields=["title","duration"])
    total_chapter_count = frappe.get_value(
                "Audiobook Chapter",
                filters={
                    "audiobook": audiobook.name
                },
                fieldname="COUNT(title)")
    response = {
        "title": audiobook.title,
        "description": audiobook.description,
        "author": author.full_name,
        "narrator": narrator.full_name,
        "thumbnail": thumbnail_url,
        "Sample Audiobook Title": audiobook.sample_audio_title,
        "duration": format_duration(audiobook.duration),
        "total chapter": total_chapter_count,
        "total chapter duration": format_duration(audiobook.total_chapters_duration),
        "chapters" : []
        # Is bookmarked ?
        # "is_favorite": is_favorite
    }
    for chapter in chapters:
        response["chapters"].append({
            "title": chapter.title,
            "duration" : format_duration(chapter.duration)
        })
    return response

"""
#
"""
@frappe.whitelist(allow_guest=True)
def retrieve_recommended_audiobooks(search=None, page=1, limit=20):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    filters = []
    if search:
        filters.append(f"(ab.title LIKE '%{search}%' OR aut.name LIKE '%{search}%' OR nar.name LIKE '%{search}%')")
    filters_str = " AND ".join(filters)
    offset = (page - 1) * limit
    audiobooks = frappe.get_all(
        "Audiobook",
        filters={
                "recommendation" : 1,
                 "disabled": 0,
                 },
        fields=[
                "name",
                "title",
                "description",
                "author",
                "narrator",
                "publisher",
                "thumbnail",
                "chapter",
                "sample_audio_title",
                "duration",
                "total_chapters_duration"
                ],
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )
    response_data = []
    if audiobooks:
        for audiobook in audiobooks:
            author = frappe.get_doc("User", audiobook.author)
            narrator = frappe.get_doc("User", audiobook.narrator)
            chapters = frappe.get_all("Audiobook Chapter", filters={ "audiobook": audiobook.name }, fields=["title","duration"])
            thumbnail_url = f"https://{frappe.local.site}{audiobook.thumbnail}"
            total_chapter_count = frappe.get_value(
                "Audiobook Chapter",
                filters={"audiobook": audiobook.name},
                fieldname="COUNT(title)")
            response_data.append({
                "title": audiobook.title,
                "description": audiobook.description,
                "author": author.full_name,
                "narrator":narrator.full_name,
                "thumbnail": thumbnail_url,
                "sample audiobook title": audiobook.sample_audio_title,
                "duration": format_duration(audiobook.duration),
                "total chapter": total_chapter_count,
                "total chapter duration": format_duration(audiobook.total_chapters_duration),
                "chapters" : []
        })
        for chapter in chapters:
                response_data[-1]["chapters"].append({
                "title": chapter.title,
                "duration" : format_duration(chapter.duration)
            })
        return response_data
    else:
        return "No Audiobook found."

@frappe.whitelist(allow_guest=True)
def retrieve_editors_picks(search=None, page=1, limit=20):
    filters = []
    if search:
        filters.append(f"(ab.title LIKE '%{search}%' OR aut.name LIKE '%{search}%' OR nar.name LIKE '%{search}%')")
    filters_str = " AND ".join(filters)
    offset = (page - 1) * limit
    editors_picks_audiobooks = frappe.get_all(
        "Audiobook",
        filters={
               "editors_pick": 1,
               "disabled": 0
                 },
        fields=[
                "name",
                "title",
                "author",
                "narrator",
                "publisher",
                "description",
                "thumbnail",
                "chapter",
                "sample_audio_title",
                "duration",
                "total_chapters_duration"
                ],
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )
    response_data = []
    if editors_picks_audiobooks:
        for editors_picks_audiobook in editors_picks_audiobooks:
            chapters = frappe.get_all("Audiobook Chapter", filters={ "audiobook": editors_picks_audiobook.name }, fields=["title","duration"])
            author = frappe.get_doc("User", editors_picks_audiobook.author)
            narrator = frappe.get_doc("User", editors_picks_audiobook.narrator)
            thumbnail_url = f"https://{frappe.local.site}{editors_picks_audiobook.thumbnail}"
            total_chapter_count = frappe.get_value(
                "Audiobook Chapter",
                filters={"audiobook": editors_picks_audiobook.name},
                fieldname="COUNT(title)")
            response_data.append({
                "title": editors_picks_audiobook.name,
                "description": editors_picks_audiobook.description,
                "Author": author.full_name,
                "narrator":narrator.full_name,
                "thumbnail": thumbnail_url,
                "sample audiobook title": editors_picks_audiobook.sample_audio_title,
                "duration": format_duration(editors_picks_audiobook.duration),
                "Total chapter": total_chapter_count,
                "Total chapter Duration": format_duration(editors_picks_audiobook.total_chapters_duration),
                "chapters" : []
        })
            for chapter in chapters:
                response_data[-1]["chapters"].append({
                "title": chapter.title,
                "duration" : format_duration(chapter.duration)
            })
        return response_data
    else:
        return "No Audiobook found."

@frappe.whitelist(allow_guest=True)
def retreive_audiobook_genres(search=None, page=1, limit=20):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    filters = []
    if search:
        filters.append(f"(ab.title LIKE '%{search}%' OR aut.name LIKE '%{search}%' OR nar.name LIKE '%{search}%')")
    filters_str = " AND ".join(filters)
    offset = (page - 1) * limit
    Genres = frappe.get_all(
        "Genre",
        filters={
        },
        fields=[
            "genre_name"
        ],
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )
    response_data = []
    for Genre in Genres:
        genre_images = frappe.get_all(
            "Audiobook",
            filters={"genre": Genre.genre_name},
            fields=["thumbnail"],
            limit=5,
            order_by="creation DESC"
        )
        number_of_audiobooks = frappe.get_value(
        "Audiobook",
        filters={
                "genre": Genre.genre_name
            },
        fieldname="COUNT(title)"
    )
        if genre_images:
            thumbnail_urls = [f"https://{frappe.local.site}{image.thumbnail}" for image in genre_images]
        else:
            thumbnail_urls = []
        response_data.append({
            "Genre Name": Genre.genre_name,
            "Audiobooks": number_of_audiobooks,
            "thumbnail": thumbnail_urls
        })
   
    return response_data

@frappe.whitelist(allow_guest=True)
def retreive_audiobook_genre(audiobook_genre):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    audiobooks = frappe.get_all(
        "Audiobook",
       
        filters={
            "disabled": 0,
            "genre": audiobook_genre
        },
        fields=[
            "name",
            "title",
            "description",
            "author",
            "narrator",
            "publisher",
            "thumbnail",
            "chapter",
            "genre",
            "sample_audio_title",
            "duration",
            "total_chapters_duration"
        ]
    )
    response_data = []
    if audiobooks:
        for audiobook in audiobooks:
            author = frappe.get_doc("User", audiobook.author)
            narrator = frappe.get_doc("User", audiobook.narrator)
            chapters = frappe.get_all("Audiobook Chapter", filters={ "audiobook": audiobook.name }, fields=["title","duration"])
            thumbnail_url = f"https://{frappe.local.site}{audiobook.thumbnail}"
            total_chapter_count = frappe.get_value(
                "Audiobook Chapter",
                filters={"audiobook": audiobook.name},
                fieldname="COUNT(title)")
            response_data.append({
                "title": audiobook.title,
                "description": audiobook.description,
                "author": author.full_name,
                "narrator": narrator.full_name,
                "thumbnail": thumbnail_url,
                "sample audiobook title": audiobook.sample_audio_title,
                "duration": format_duration(audiobook.duration),
                "Total chapter": total_chapter_count,
                "Total chapter Duration": format_duration(audiobook.total_chapters_duration),
                "chapters" : []
        })
            for chapter in chapters:
                response_data[-1]["chapters"].append({
                "title": chapter.title,
                "duration" : format_duration(chapter.duration)
            })
        return response_data
    else:
        return "No Audiobook found."

@frappe.whitelist(allow_guest=True)
def retreive_latest_audiobook(search=None, page=1, limit=20):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    filters = []
    if search:
        filters.append(f"(ab.title LIKE '%{search}%' OR aut.name LIKE '%{search}%' OR nar.name LIKE '%{search}%')")
    filters_str = " AND ".join(filters)
    offset = (page - 1) * limit
    from_date = frappe.utils.add_days(frappe.utils.today(), -5)
    # to_date = frappe.utils.today()
    audiobooks = frappe.get_all(
        'Audiobook',
        filters={
             "disabled": 0,
             "If we add a fild on the ui we will use this"
             "creation field created by default when we create doctype to store document created date on the database"
            # field: ['>=', from_date],
            # field: ['<=', to_date]
            'creation': ['>=', from_date]
        },
        fields=[
            "name",
            "title",
            "description",
            "author",
            "narrator",
            "publisher",
            "thumbnail",
            "chapter",
            "sample_audio_title",
            "duration",
            "total_chapters_duration"
        ]
    )
    if audiobooks:
        response_data = []
        for audiobook in audiobooks:
            author = frappe.get_doc("User", audiobook.author)
            narrator = frappe.get_doc("User", audiobook.narrator)
            chapters = frappe.get_all("Audiobook Chapter", filters={ "audiobook": audiobook.name }, fields=["title","duration"])
            thumbnail_url = f"https://{frappe.local.site}{audiobook.thumbnail}"
            total_chapter_count = frappe.get_value(
                "Audiobook Chapter",
                filters={
                    "audiobook": audiobook.name
                 },
                 fieldname="COUNT(title)")
            response_data.append({
                "title": audiobook.title,
                "description": audiobook.description,
                "author": author.full_name,
                "narrator": narrator.full_name,
                "thumbnail": thumbnail_url,
                "Sample Audiobook": audiobook.sample_audio_title,
                "duration": format_duration(audiobook.duration),
                "Total chapter": total_chapter_count,
                "Total chapter Duration": format_duration(audiobook.total_chapters_duration),
                "chapters" : chapters
        })
        return response_data
    else:
        return "No Audiobook found."

@frappe.whitelist(allow_guest=False)
def audiobook_sample(audiobook_id):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    audiobook_doc = frappe.get_doc("Audiobook", audiobook_id)
    audio_file_doc = frappe.get_doc("Audiobook File", audiobook_doc.audio_file)
    file_url = audio_file_doc.file_url
    file_path = frappe.utils.get_files_path(file_url)

    filename = secure_filename(audio_file_doc.audio_base_name)
    mimetype = mimetypes.guess_type(filename)[0]
    abso_file_path = os.path.abspath(file_path)

    if not os.path.exists(os.path.dirname(abso_file_path) + "/hls"):
        os.makedirs(os.path.dirname(abso_file_path) + "/hls")
    os.chmod(os.path.dirname(abso_file_path) + "/hls", 0o777)
    try:
        hls_cmd = [
            "ffmpeg", "-y", "-i", abso_file_path, "-hls_time", "5", "-c:v", "libx264", "-b:v", "1M",
            "-c:a", "aac", "-b:a", "128k", "-f", "hls", "-hls_segment_filename",
            os.path.dirname(abso_file_path) + "/hls/segment_%03d.ts",
            os.path.dirname(abso_file_path) + "/hls/playlist.m3u8", "-vn", "-c:a", "copy", os.path.dirname(abso_file_path) + "/hls/output.mp3"
        ]
        subprocess_result = subprocess.run(hls_cmd)
        if subprocess_result.returncode != 0:
            raise Exception(f"FFmpeg command failed: {subprocess_result.stderr}")
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        message = f"Failed to generate new HLS manifest file: {e}"
        frappe.throw(message, frappe.ValidationError)
    try:
        with app.test_request_context():
            return send_file(os.path.dirname(abso_file_path) + "/hls/output.mp3", mimetype="application/vnd.apple.mpegurl")
    finally:
        cleanup_hls_files(abso_file_path)
def cleanup_hls_files(abso_file_path):
    hls_dir = os.path.dirname(abso_file_path) + "/hls"
    if os.path.exists(hls_dir):
        for file in os.listdir(hls_dir):
            os.remove(os.path.join(hls_dir, file))
        os.rmdir(hls_dir)

@frappe.whitelist(allow_guest=False)
def play_audiobook_chapter(audiobook_chapter):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    audiobook_doc = frappe.get_doc("Audiobook Chapter", audiobook_chapter)
    audio_file_doc = frappe.get_doc("Audiobook File", audiobook_doc.audio_file)
    file_url = audio_file_doc.file_url
    file_path = frappe.utils.get_files_path(file_url)

    filename = secure_filename(audio_file_doc.audio_base_name)
    mimetype = mimetypes.guess_type(filename)[0]
    abso_file_path = os.path.abspath(file_path)

    if not os.path.exists(os.path.dirname(abso_file_path) + "/hls"):
        os.makedirs(os.path.dirname(abso_file_path) + "/hls")
    os.chmod(os.path.dirname(abso_file_path) + "/hls", 0o777)
    try:
        hls_cmd = [
            "ffmpeg", "-y", "-i", abso_file_path, "-hls_time", "5", "-c:v", "libx264", "-b:v", "1M",
            "-c:a", "aac", "-b:a", "128k", "-f", "hls", "-hls_segment_filename",
            os.path.dirname(abso_file_path) + "/hls/segment_%03d.ts",
            os.path.dirname(abso_file_path) + "/hls/playlist.m3u8", "-vn", "-c:a", "copy", os.path.dirname(abso_file_path) + "/hls/output.mp3"
        ]
        subprocess_result = subprocess.run(hls_cmd)
        if subprocess_result.returncode != 0:
            raise Exception(f"FFmpeg command failed: {subprocess_result.stderr}")
    except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
        message = f"Failed to generate new HLS manifest file: {e}"
        frappe.throw(message, frappe.ValidationError)
    try:
        with app.test_request_context():
            return send_file(os.path.dirname(abso_file_path) + "/hls/output.mp3", mimetype="application/vnd.apple.mpegurl")
    finally:
        cleanup_hls_files(abso_file_path)
def cleanup_hls_files(abso_file_path):
    hls_dir = os.path.dirname(abso_file_path) + "/hls"
    if os.path.exists(hls_dir):
        for file in os.listdir(hls_dir):
            os.remove(os.path.join(hls_dir, file))
        os.rmdir(hls_dir)

if __name__ == '__main__':
    app.run()
