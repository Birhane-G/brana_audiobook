import frappe
import json
from frappe.utils import now_datetime
import mimetypes
from frappe.utils.file_manager import get_file_url
from flask import Flask, Response, send_file, request, make_response, current_app, stream_with_context
from werkzeug.utils import secure_filename

app = Flask(__name__)

@frappe.whitelist(allow_guest=True)
def retrieve_audiobooks(search=None, page=1, limit=20):
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
                "subscription_level",
                "audio_file",
                "thumbnail",
                "chapter",
                "total_listening_time",
                ],
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )

    total_count = frappe.get_value(
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
        audio_file_url = get_file_url(audiobook.audio_file) if audiobook.audio_file else None
        chapters = frappe.get_all("Audiobook Chapter", filters={ "audiobook": audiobook.name }, fields=["title",])
        response_data.append({
            "id": audiobook.name,
            "title": audiobook.title,
            "description": audiobook.description,
            "author": author.full_name,
            "narrator": narrator.full_name,
            "publisher": audiobook.publisher,
            "total_listening_time": str(audiobook.total_listening_time),
            "thumbnail": audiobook.thumbnail,
            "audio_file_url": audio_file_url,
            "chapter" : chapters,
        })

    return json.dumps({"success": True, "data": {"audiobooks": response_data, "total_count": total_count}}, ensure_ascii=False)

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
    audio_file_url = get_file_url(audiobook.audio_file) if audiobook.audio_file else None
    total_listening_time = str(audiobook.total_listening_time) if audiobook.total_listening_time else None
    response = {
        "id": audiobook.name,
        "title": audiobook.title,
        "author": author.full_name,
        "narrator": narrator.full_name,
        "duration": total_listening_time,
        "description": audiobook.description,
        "audio_file_url": audio_file_url,
        # "release_date": audiobook.release_date,
        # "average_rating": audiobook.average_rating,
        # "num_ratings": audiobook.num_ratings,
        # Is bookmarked ?
        "is_favorite": is_favorite
    }

    return json.dumps({"success": True, "data": response}, ensure_ascii=False)
import os
@frappe.whitelist(allow_guest=False)
def retrieve_audiobook_sample(audiobook_id):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)

    # Perform user role and permission checks here
    # ...
    # Ensure the authenticated user has the necessary roles and permissions to access the API method

    audiobook_doc = frappe.get_doc("Audiobook", audiobook_id)
    audio_file_doc = frappe.get_doc("File", audiobook_doc.audio_file)

    file_path = frappe.get_site_path("public", audio_file_doc.file_url[1:])
    filename = secure_filename(audio_file_doc.file_name)
    mimetype = mimetypes.guess_type(filename)[0]

    abso_file_path = os.path.abspath(file_path)
    with app.test_request_context():
        return Response(stream_with_context(send_file(abso_file_path, mimetype=mimetype, as_attachment=True)), content_type=mimetype)
    # with app.test_request_context():
    #     return send_file(abso_file_path, mimetype=mimetype, as_attachment=True, conditional=True, download_name=filename)
import subprocess
@frappe.whitelist(allow_guest=False)
def test_audiobook_sample(audiobook_id):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    
    audiobook_doc = frappe.get_doc("Audiobook", audiobook_id)
    audio_file_doc = frappe.get_doc("File", audiobook_doc.audio_file)

    file_path = frappe.get_site_path("public", audio_file_doc.file_url[1:])
    filename = secure_filename(audio_file_doc.file_name)
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
# def test_audiobook_sample(audiobook_id):
#     if not frappe.session.user:
#         frappe.throw("User not authenticated", frappe.AuthenticationError)
#     audiobook_doc = frappe.get_doc("Audiobook", audiobook_id)
#     audio_file_doc = frappe.get_doc("File", audiobook_doc.audio_file)

#     file_path = frappe.get_site_path("public", audio_file_doc.file_url[1:])
#     filename = secure_filename(audio_file_doc.file_name)
#     mimetype = mimetypes.guess_type(filename)[0]
#     abso_file_path = os.path.abspath(file_path)

#     if not os.path.exists(os.path.dirname(abso_file_path)+"/hls"):
#         os.makedirs(os.path.dirname(abso_file_path)+"/hls")
#     os.chmod(os.path.dirname(abso_file_path)+"/hls", 0o777)

#     # Used TO Test
#     # return os.path.exists(os.path.dirname(abso_file_path)+"/hls")

    # ffmpeg -y -i Abdu.mp3 -hls_time 5 -c:v libx264 -b:v 1M -c:a aac -b:a 128k 
    # -f segment -segment_time 10 -segment_list playlist.m3u8 segment_%03dbook.ts -vn -c:a copy output.mp3
#     try:
#         hls_cmd = [
#             "ffmpeg","-y" ,"-i", abso_file_path, "-hls_time", "5", "-c:v", "libx264", "-b:v", "1M",
#             "-c:a", "aac", "-b:a", "128k", "-f", "segment", "-segment_time", "10", "-segment_list",
#             os.path.dirname(abso_file_path)+"/hls/playlist.m3u8", os.path.dirname(abso_file_path)+"/hls/segment_%03dbook.ts"
#         ]
#         # hls_cmd = [
#         #     "ffmpeg","-y", "-i", abso_file_path, "-c:a", "acc", "-b:a", "128k",
#         #     "-f", "-segment_time", "10", os.path.dirname(abso_file_path)+"/hls/playlist.m3u8", 
#         #     os.path.dirname(abso_file_path)+"/hls/segment%dbook.ts"
#         # ]
#         subprocess_result = subprocess.run(hls_cmd)
#         if subprocess_result.returncode != 0:
#             raise Exception(f"FFmpeg command failed: {subprocess_result.stderr}")
#          # with open(os.path.dirname(abso_file_path)+"/hls/playlist.m3u8", "r", encoding="utf-8") as f:
#         #     file_content = f.read()
#         #     segments = json.loads(file_content)
#         with open(os.path.dirname(abso_file_path)+"/hls/playlist.m3u8", "r", encoding="utf-8") as f:
#             file_content = f.readlines()
#             segments = []
#             for line in file_content:
#                 if line.startswith("#EXTINF"):
#                     duration_str = line.split(",")[1]
#                     try:
#                         duration = float(duration_str)
#                         segments.append({"duration": duration})
#                     except ValueError:
#                         continue  # Skip lines with invalid duration
#                 elif line.startswith("#EXT-X-ENDLIST"):
#                     break
#                 else:
#                     segments.append({"url": line})

#                      # if(vall):
#         #     return os.path.dirname(abso_file_path)+"/hls/playlist.m3u8"
#         # return "not work"
#     except (FileNotFoundError, json.decoder.JSONDecodeError) as e:
#         message = f"Failed to generate new HLS manifest file: {e}"
#         frappe.throw(message, frappe.ValidationError)

#     # with current_app.test_request_context():
#     site = frappe.local.site
#     with frappe.get_site_context(site):
#         return send_file(os.path.dirname(abso_file_path)+"/hls/playlist.m3u8", mimetype="application/vnd.apple.mpegurl")

if __name__ == '__main__':
    app.run()

# 51ae2b8175
# @frappe.whitelist(allow_guest=False)
# def retrieve_audiobook_chapters(audiobook_id):
#     if not frappe.session.user:
#         frappe.throw("User not authenticated", frappe.AuthenticationError)

#     # Verify that the user is subscribed to a subscription level equal or higher than that of the audiobook's subscription level
#     subscription_plan = frappe.get_all("Subscription Plan",
#         filters={"user_profile": frappe.session.user, "end_date": (">=", frappe.utils.nowdate())},
#         fields=["subscription_level"])

#     audiobook_subscription_level = frappe.get_value("Audiobook", audiobook_id, "subscription_level")

#     if not any(plan.subscription_level == audiobook_subscription_level for plan in subscription_plan):
#         frappe.throw("You are not subscribed to a subscription level that allows access to this audiobook")

#     # Check if the user has the necessary roles and permissions to access the API method
#     if not frappe.has_permission("Audiobook", "read"):
#         frappe.throw("You do not have the necessary permissions to access this API method", frappe.PermissionError)

#     # Perform additional user role and permission checks here
#     # ...
#     # Ensure the authenticated user has the necessary roles and permissions to access the API method

#     audiobook_chapters = frappe.get_all("Audiobook Chapter",
#         filters={"audiobook": audiobook_id, "docstatus": 1, "disabled": 0},
#         fields=["name", "chapter_number", "title", "description", "audio_file", "start_time", "end_time", "total_duration"],
#         order_by="chapter_number ASC")

#     response_data = []
#     for chapter in audiobook_chapters:
#         chapter_doc = frappe.get_doc("Audiobook Chapter", chapter.name)
#         response_data.append({
#             "id": chapter_doc.name,
#             "chapter_number": chapter_doc.chapter_number,
#             "title": chapter_doc.title,
#             "description": chapter_doc.description,
#             "audio_file_url": get_file_url(chapter_doc.audio_file),
#             "start_time": chapter_doc.start_time,
#             "end_time": chapter_doc.end_time,
#             "total_duration": chapter_doc.total_duration
#         })
#     return json.dumps({"success": True, "data": response_data})

# @frappe.whitelist(allow_guest=False)
# def retrieve_audiobook_chapter_audio(audiobook_id, chapter_id):
#     if not frappe.session.user:
#         frappe.throw("User not authenticated", frappe.AuthenticationError)

#     # Verify that the user is subscribed to a subscription level equal or higher than that of the audiobook's subscription level
#     subscription_plan = frappe.get_all("Subscription Plan",
#         filters={"user_profile": frappe.session.user, "end_date": (">=", frappe.utils.nowdate())},
#         fields=["subscription_level"])

#     audiobook_subscription_level = frappe.get_value("Audiobook", audiobook_id, "subscription_level")

#     if not any(plan.subscription_level == audiobook_subscription_level for plan in subscription_plan):
#         frappe.throw("You are not subscribed to a subscription level that allows access to this audiobook")

#     # Check if the user has the necessary roles and permissions to access the API method
#     if not frappe.has_permission("Audiobook Chapter", "read"):
#         frappe.throw("You do not have the necessary permissions to access this API method", frappe.PermissionError)

#     # Perform additional user role and permission checks here
#     # ...
#     # Ensure the authenticated user has the necessary roles and permissions to access the API method

#     chapter_doc = frappe.get_doc("Audiobook Chapter", chapter_id)
#     audio_file_doc = frappe.get_doc("File", chapter_doc.audio_file)

#     file_path = frappe.get_site_path("public", audio_file_doc.file_url[1:])
#     filename = secure_filename(audio_file_doc.file_name)
#     mimetype = mimetypes.guess_type(filename)[0]

#     # Create a new User Listening History record for the current user and audiobook
#     listening_history = frappe.new_doc("User Listening History")
#     listening_history.user = frappe.session.user
#     listening_history.audio_content_type = "Audiobook"
#     listening_history.audio_content_id = audiobook_id
#     listening_history.start_time = now_datetime()
#     listening_history.end_time = now_datetime()
#     listening_history.total_listening_time = 0
#     listening_history.access_frequency = 1
#     listening_history.save()



#     return Response(stream_with_context(send_file(file_path, mimetype=mimetype, as_attachment=True, attachment_filename=filename, streaming=True)), content_type=mimetype)



# @frappe.whitelist(allow_guest=False)
# def update_audiobook_chapter_listening_time():
#     if not frappe.session.user:
#         frappe.throw("User not authenticated", frappe.AuthenticationError)

#     audiobook_id = request.form.get("audiobook_id")
#     chapter_id = request.form.get("chapter_id")
#     listening_time = request.form.get("listening_time")

#     chapter_doc = frappe.get_doc("Audiobook Chapter", chapter_id)
#     chapter_doc.total_listening_time += float(listening_time)
#     chapter_doc.save()

#     audiobook_doc = frappe.get_doc("Audiobook", audiobook_id)
#     audiobook_doc.total_listening_time += float(listening_time)
#     audiobook_doc.save()

#     # Retrieve the User Listening History record for the current user and audiobook
#     listening_history = frappe.get_all("User Listening History",
#         filters={"user": frappe.session.user, "audio_content_type": "Audiobook", "audio_content_id": audiobook_id},
#         fields=["name", "total_listening_time"])

#     if listening_history:
#         # Update the total_listening_time field in the User Listening History record
#         listening_history_doc = frappe.get_doc("User Listening History", listening_history[0].name)
#         listening_history_doc.total_listening_time += float(listening_time)
#         listening_history_doc.save()

#     return "OK"


# def get_file_url(file_name):
#     if file_name:
#         file_doc = frappe.get_doc("File", file_name)
#         return file_doc.file_url
#     else:
#         return None


# @frappe.whitelist()
# def retrieve_user_listening_history(user_id):
#     # Check if the authenticated user has permission to retrieve the listening history for the specified user
#     if not frappe.has_permission("User Profile", "read", user_id=user_id):
#         frappe.throw("You do not have the necessary permissions to access this API method", frappe.PermissionError)

#     # Retrieve the User Listening History records
#     listening_history = frappe.get_all("User Listening History",
#         filters={"user": user_id},
#         fields=["audio_content_type", "audio_content_id", "total_listening_time", "access_frequency"])

#     # Format the retrieved data into a JSON response
#     response = []
#     for lh in listening_history:
#         if lh.audio_content_type == "Audiobook":
#             audiobook = frappe.get_doc("Audiobook", lh.audio_content_id)
#             response.append({
#                 "audiobook_id": audiobook.name,
#                 "total_time": lh.total_listening_time,
#                 "access_frequency": lh.access_frequency
#             })
#         elif lh.audio_content_type == "Podcast":
#             podcast = frappe.get_doc("Podcast", lh.audio_content_id)
#             response.append({
#                 "podcast_id": podcast.name,
#                 "total_time": lh.total_listening_time,
#                 "access_frequency": lh.access_frequency
#             })

#     return {"listening_history": response}