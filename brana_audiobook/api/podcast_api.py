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
@frappe.whitelist(allow_guest=True)
def retrieve_podcasts(search=None, page=1, limit=20):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    filters = []
    if search:
        filters.append(f"(ab.title LIKE '%{search}%' OR aut.name LIKE '%{search}%' OR nar.name LIKE '%{search}%')")
    filters_str = " AND ". join(filters)
    offset = (page - 1) * limit
    user = frappe.get_doc("User", frappe.session.user)
    favorite = frappe.get_all("Brana User Profile",filters={"user": user.email})
    podcasts = frappe.get_all(
        "Podcast",
        filters={
            "disabled": 0,
                 },
        fields=[
                "title",
                "description",
                "host",
                "publisher",
                "cover_image_url",
                "episodes",
                ],
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )
    if podcasts:
        total_podcast_count = frappe.get_value(
        "Podcast",
        filters={
                 "disabled": 0,
                 },
        fieldname="COUNT(title)"
    )
        response_data = []
        for podcast in podcasts:
            host = frappe.get_doc("User", podcast.host)
            episodes = frappe.get_all("Podcast Episode", filters={ "podcast": podcast.title }, fields=["title","duration", "episode_number"])
            cover_image_url = f"https://{frappe.local.site}{podcast.cover_image_url}"
            is_favorite = 0
            if favorite:
                favorite = frappe.get_doc("Brana User Profile", user.email)
                if not favorite.wish_list:
                    is_favorite = 0
                else:
                    for item in favorite.wish_list:
                        if item.title == podcast.name:
                            is_favorite = 1
            response_data.append({
                "title": podcast.title,
                "description": podcast.description,
                "Host": host.full_name,
                "cover image": cover_image_url,
                "is_favorite": is_favorite,
                "episodes" : []
        })
            for episode in episodes:
                is_favorite = 0
                if favorite:
                    favorite = frappe.get_doc("Brana User Profile", user.email)
                    if not favorite.wish_list:
                        is_favorite = 0
                    else:
                        for item in favorite.wish_list:
                            if item.title == episode.title:
                                is_favorite = 1
                response_data[-1]["episodes"].append({
                "title": episode.title,
                "duration" : format_duration(episode.duration),
                "podcast Number" : episode.episode_number,
                "is_favorite": is_favorite,
            })
        # response_data.append({
        #     "Total Podcast": total_bodcast_count
        #     })
        return response_data
    else:
        return "No Podcast found."

@frappe.whitelist(allow_guest=True)
def retrieve_podcast(podcast_id):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    # Perform user role and permission checks here
    # ...
    # Ensure the authenticated user has the necessary roles and permissions to access the API method
    podcast = frappe.get_doc("Podcast", podcast_id)
    user = frappe.get_doc("User", frappe.session.user)
    favorite = frappe.get_all("Brana User Profile",filters={"user": user.email})
    host = frappe.get_doc("User", podcast.host)
    is_favorite = 0
    if favorite:
        favorite = frappe.get_doc("Brana User Profile", user.email)
        if not favorite.wish_list:
            is_favorite = 0
        else:
            for item in favorite.wish_list:
                if item.title == podcast.name:
                    is_favorite = 1
    cover_image_url = f"https://{frappe.local.site}{podcast.cover_image_url}"
    episodes = frappe.get_all("Podcast Episode", filters={ "podcast": podcast.title }, fields=["title","duration", "episode_number"])
    total_episode_count = frappe.get_value(
                "Podcast Episode",
                filters={
                    "podcast": podcast.title
                },
                fieldname="COUNT(title)")
    response = {
        "title": podcast.title,
        "description": podcast.description,
        "Host": host.full_name,
        "cover image": cover_image_url,
        "episodes" : [],
        "total episodes" : total_episode_count,
        "is_favorite": is_favorite,
    }
    for episode in episodes:
        is_favorite = 0
        if favorite:
            favorite = frappe.get_doc("Brana User Profile", user.email)
            if not favorite.wish_list:
                is_favorite = 0
            else:
                for item in favorite.wish_list:
                    if item.title == episode.title:
                        is_favorite = 1
        response["episodes"].append({
                "title": episode.title,
                "duration" : format_duration(episode.duration),
                "podcast Number" : episode.episode_number,
                "is_favorite": is_favorite,
            })
    return response

@frappe.whitelist(allow_guest=True)
def retrieve_recommended_podcasts(search=None, page=1, limit=20):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    filters = []
    if search:
        filters.append(f"(ab.title LIKE '%{search}%' OR aut.name LIKE '%{search}%' OR nar.name LIKE '%{search}%')")
    filters_str = " AND ". join(filters)
    offset = (page - 1) * limit
    user = frappe.get_doc("User", frappe.session.user)
    favorite = frappe.get_all("Brana User Profile",filters={"user": user.email})
    podcasts = frappe.get_all(
        "Podcast",
        filters={
            "disabled": 0,
            "recommendation" : 1,
                 },
        fields=[
                "title",
                "description",
                "host",
                "publisher",
                "cover_image_url",
                "episodes",
                ],
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )
    if podcasts:
        response_data = []
        for podcast in podcasts:
            host = frappe.get_doc("User", podcast.host)
            episodes = frappe.get_all("Podcast Episode", filters={ "podcast": podcast.title }, fields=["title","duration", "episode_number"])
            cover_image_url = f"https://{frappe.local.site}{podcast.cover_image_url}"
            total_episode_count = frappe.get_value(
                "Podcast Episode",
                filters={
                    "podcast": podcast.title
                },
                fieldname="COUNT(title)")
            is_favorite = 0
            if favorite:
                favorite = frappe.get_doc("Brana User Profile", user.email)
                if not favorite.wish_list:
                    is_favorite = 0
                else:
                    for item in favorite.wish_list:
                        if item.title == podcast.name:
                            is_favorite = 1
            response_data.append({
                "title": podcast.title,
                "description": podcast.description,
                "Host": host.full_name,
                "cover image": cover_image_url,
                "is_favorite": is_favorite,
                "episodes" : [],
                "total episodes" : total_episode_count
        })
            for episode in episodes:
                is_favorite = 0
            if favorite:
                favorite = frappe.get_doc("Brana User Profile", user.email)
                if not favorite.wish_list:
                    is_favorite = 0
                else:
                    for item in favorite.wish_list:
                        if item.title == episode.title:
                            is_favorite = 1
                response_data[-1]["episodes"].append({
                "title": episode.title,
                "duration" : format_duration(episode.duration),
                "podcast Number" : episode.episode_number,
                "is_favorite": is_favorite,
            })
        return response_data
    else:
        return "No Recommended Podcast found."
    
@frappe.whitelist(allow_guest=True)
def retrieve_editor_podcasts(search=None, page=1, limit=20):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    filters = []
    if search:
        filters.append(f"(ab.title LIKE '%{search}%' OR aut.name LIKE '%{search}%' OR nar.name LIKE '%{search}%')")
    filters_str = " AND ". join(filters)
    offset = (page - 1) * limit
    user = frappe.get_doc("User", frappe.session.user)
    favorite = frappe.get_all("Brana User Profile",filters={"user": user.email})
    podcasts = frappe.get_all(
        "Podcast",
        filters={
            "disabled": 0,
            "editors_pick": 1,
                 },
        fields=[
                "title",
                "description",
                "host",
                "publisher",
                "cover_image_url",
                "episodes",
                ],
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )
    if podcasts:
        response_data = []
        for podcast in podcasts:
            host = frappe.get_doc("User", podcast.host)
            episodes = frappe.get_all("Podcast Episode", filters={ "podcast": podcast.title }, fields=["title","duration", "episode_number"])
            cover_image_url = f"https://{frappe.local.site}{podcast.cover_image_url}"
            is_favorite = 0
            if favorite:
                favorite = frappe.get_doc("Brana User Profile", user.email)
                if not favorite.wish_list:
                    is_favorite = 0
                else:
                    for item in favorite.wish_list:
                        if item.title == editors_picks_audiobook.name:
                            is_favorite = 1
            total_episode_count = frappe.get_value(
                "Podcast Episode",
                filters={
                    "podcast": podcast.title
                },
                fieldname="COUNT(title)")
            response_data.append({
                "title": podcast.title,
                "description": podcast.description,
                "Host": host.full_name,
                "cover image": cover_image_url,
                "is_favorite": is_favorite,
                "episodes" : [],
                "total episodes" : total_episode_count
        })
            for episode in episodes:
                is_favorite = 0
                if favorite:
                    favorite = frappe.get_doc("Brana User Profile", user.email)
                    if not favorite.wish_list:
                        is_favorite = 0
                    else:
                        for item in favorite.wish_list:
                            if item.title == episode.title:
                                is_favorite = 1
                response_data[-1]["episodes"].append({
                "title": episode.title,
                "duration" : format_duration(episode.duration),
                "podcast Number" : episode.episode_number,
                "is_favorite": is_favorite,
            })
        return response_data
    else:
        return "No Editor picks Podcast found."

@frappe.whitelist(allow_guest=False)
def play_podcast_episode(podcast_episode):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    audiobook_doc = frappe.get_doc("Podcast Episode", podcast_episode)
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