import frappe
import json
from frappe.utils import now_datetime
import mimetypes
import subprocess
import os
from frappe.utils.file_manager import get_file_url
from flask import Flask, Response, send_file, request, make_response, current_app, stream_with_context
from werkzeug.utils import secure_filename
from flask import send_file
from frappe.utils.file_manager import get_file_path
app = Flask(__name__)

"""
# This Api Used To Retrieve All Audiobooks 
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
                #  "docstatus": 1,
                #  "disabled": 0,
                #  "subscription_level": ("!=", "")
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
                ],
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )
    total_audiobook_count = frappe.get_value(
        "Audiobook",
        filters={
                #  "docstatus": 1,
                #  "disabled": 0,
                #  "subscription_level": ("!=", "")
                 },
        fieldname="COUNT(title)"
    )
    response_data = []
    for audiobook in audiobooks:
        author = frappe.get_doc("User", audiobook.author)
        narrator = frappe.get_doc("User", audiobook.narrator)
        # audio_file_url = get_file_url(audiobook.audio_file) if audiobook.audio_file else None
        # audio_file_url = frappe.get_site_path('public', 'files', audiobook.audio_file)
        chapters = frappe.get_all("Audiobook Chapter", filters={ "audiobook": audiobook.name }, fields=["title","duration"])
        total_chapters_duration = 0
        for chapter in chapters:
            total_chapters_duration = total_chapters_duration + chapter.duration
        audio_file_doc = frappe.get_doc("File", audiobook.thumbnail)
        site_name = frappe.local.site
        thumbnail_url = f"https://{site_name}{audio_file_doc.file_url}"
        total_chapter_count = frappe.get_value(
        "Audiobook Chapter",
        filters={
            "audiobook": audiobook.name
                 },
        fieldname="COUNT(title)"
    )
        response_data.append({
            "title": audiobook.title,
            "description": audiobook.description,
            "author": author.full_name,
            "narrator": narrator.full_name,
            "thumbnail": thumbnail_url,
            "Sample Audio Title": audiobook.sample_audio_title,
            "duration": audiobook.duration,
            "chapter" : chapters,
            "Total chapter": total_chapter_count,
            "Total chapter Duration": total_chapters_duration
        })
    response_data.append({
        "Total Audiobook": total_audiobook_count
    })
    return response_data

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
    is_favorite = False
    if user_favorite:
        is_favorite = True
    author = frappe.get_doc("User", audiobook.author)
    narrator = frappe.get_doc("User", audiobook.narrator)
    total_listening_time = str(audiobook.total_listening_time) if audiobook.total_listening_time else None
    response = {
        "id": audiobook.name,
        "title": audiobook.title,
        "author": author.full_name,
        "narrator": narrator.full_name,
        "duration": total_listening_time,
        "description": audiobook.description,
        # Is bookmarked ?
        "is_favorite": is_favorite
    }

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
                "recommendation" : 1
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
                ],
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )
    response_data = []
    for audiobook in audiobooks:
        author = frappe.get_doc("User", audiobook.author)
        narrator = frappe.get_doc("User", audiobook.narrator)
        chapters = frappe.get_all("Audiobook Chapter", filters={ "audiobook": audiobook.name }, fields=["title","duration"])
        # file_path = frappe.get_site_path('public', 'files', "photo1695894679.jpeg")
        # abso_file_path = os.path.abspath(file_path)
        total_chapter_count = frappe.get_value(
        "Audiobook Chapter",
        filters={"audiobook": audiobook.name},
        fieldname="COUNT(title)")
        response_data.append({
            "title": audiobook.title,
            "description": audiobook.description,
            "author": author.full_name,
            "narrator": narrator.full_name,
            "thumbnail": audiobook.thumbnail,
            "chapter" : chapters,
            "Total_chapter": total_chapter_count
        })
        
    return response_data

@frappe.whitelist(allow_guest=True)
def retrieve_editors_picks(search=None, page=1, limit=20):
    """it return 1 if editors pic true else return 0"""
    # editors_picks = frappe.get_value(
    #     "Audiobook",
    #     filters={
    #         "title": audiobook_id, 
    #         },
    #     fieldname="editors_pick"
    # )
    filters = []
    if search:
        filters.append(f"(ab.title LIKE '%{search}%' OR aut.name LIKE '%{search}%' OR nar.name LIKE '%{search}%')")
    filters_str = " AND ".join(filters)
    offset = (page - 1) * limit
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
                "description",
                "thumbnail",
                "chapter",
                "total_listening_time",
                ],
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )
    response_data = []
    for editors_picks_audiobook in editors_picks_audiobooks:
        chapters = frappe.get_all("Audiobook Chapter", filters={ "audiobook": editors_picks_audiobook.name }, fields=["title","duration"])
        author = frappe.get_doc("User", editors_picks_audiobook.author)
        response_data.append({
            "title": editors_picks_audiobook.name,
            "Author": author.full_name,
            "description": editors_picks_audiobook.description,
            "chapters": chapters,
            "thumbnail": editors_picks_audiobook.thumbnail,
        })

    return response_data
@frappe.whitelist(allow_guest=False)
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
        number_of_audiobooks = frappe.get_value(
        "Audiobook",
        filters={
                "genre": Genre.genre_name
                 },
        fieldname="COUNT(title)"
    )
        response_data.append({
            "Genre Name": Genre.genre_name,
            "Audiobooks": number_of_audiobooks
        })
   
    return response_data

@frappe.whitelist(allow_guest=False)
def retreive_audiobook_genre(audiobook_genre):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)

    audiobooks = frappe.get_all(
        "Audiobook",
        filters={
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
                "genre"
        ]
    )
    response_data = []
    for audiobook in audiobooks:
        author = frappe.get_doc("User", audiobook.author)
        narrator = frappe.get_doc("User", audiobook.narrator)
        chapters = frappe.get_all("Audiobook Chapter", filters={ "audiobook": audiobook.name }, fields=["title","duration"])
        file_path = frappe.get_site_path('public', 'files', "photo1695894679.jpeg")
        abso_file_path = os.path.abspath(file_path)
        total_chapter_count = frappe.get_value(
        "Audiobook Chapter",
        filters={"audiobook": audiobook.name},
        fieldname="COUNT(title)")
        response_data.append({
            "title": audiobook.title,
            "description": audiobook.description,
            "author": author.full_name,
            "narrator": narrator.full_name,
            "thumbnail": audiobook.thumbnail,
            "chapter" : chapters,
            "Total Duration" : audiobook.total_chapters_duration,
            "Total_chapter": total_chapter_count
        })
   
    return response_data

@frappe.whitelist(allow_guest=False)
def retrieve_audiobook_thumbnail(audiobook_id):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    audiobook_doc = frappe.get_doc("Audiobook", audiobook_id)
    audio_file_doc = frappe.get_doc("File", audiobook_doc.thumbnail)
    file_path = get_file_path(audio_file_doc.file_url[7:])
    filename = secure_filename(audio_file_doc.file_name)
    mimetype = mimetypes.guess_type(filename)[0]
    abso_file_path = os.path.abspath(file_path)
    site_name = frappe.local.site
    thumbnail_url = f"https://{site_name}{audio_file_doc.file_url}"
    
    return thumbnail_url
    
    # with open(abso_file_path, 'rb') as file:
    #     file_data = file.read()

    # with app.test_request_context():
    #     return send_file(abso_file_path, mimetype=mimetype, as_attachment=True, conditional=True, download_name=filename)

@frappe.whitelist(allow_guest=False)
def audiobook_sample(audiobook_id):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    audiobook_doc = frappe.get_doc("Audiobook", audiobook_id)
    audio_file_doc = frappe.get_doc("Audiobook File", audiobook_doc.audio_file)
    # file_path = frappe.get_site_path("public", audio_file_doc.file_url[1:])
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
        # return frappe.utils.get_url() + os.path.dirname(abso_file_path) + "/hls/output.mp3"
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
