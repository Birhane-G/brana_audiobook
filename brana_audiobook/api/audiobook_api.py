import frappe
import json
# from flask import send_file, Response, stream_with_context, abort, request
from werkzeug.utils import secure_filename
from frappe.utils import now_datetime
import mimetypes

@frappe.whitelist(allow_guest=False)
def retrieve_audiobooks(search=None, page=1, limit=20):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)

    # Perform user role and permission checks here
    # ...
    # Ensure the authenticated user has the necessary roles and permissions to access the API method

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
                # "name",
                "title",
                "description",
                "author",
                "narrator",
                "publisher",
                "subscription_level",
                "audio_file",
                "total_listening_time",
                "licensing_cost",
                "production_cost",
                "royalty_percentage",
                "listening_history",
                # "chapters"
                ],
        limit=limit,
        start=offset,
        order_by="creation DESC"
    )

    total_count = frappe.get_value(
        "Audiobook",
        filters={
                #   docstatus": 1,
                #  "disabled": 0,
                #  "subscription_level": ("!=", "")
                 },
        fieldname="COUNT(title)"
    )

    response_data = []
    for audiobook in audiobooks:
        # audio_file = frappe.get_doc("File", audiobook.audio_file)
        # author = frappe.get_doc("Author", audiobook.author)
        # narrator = frappe.get_doc("Narrator", audiobook.narrator)
        # publisher = frappe.get_doc("Publisher", audiobook.publisher)
        # subscription_level = frappe.get_doc("Subscription Level", audiobook.subscription_level)
        response_data.append({
            "id": audiobook.name,
            "title": audiobook.title,
            # "description": audiobook.description,
            # "author": audiobook.author,
            # "narrator": audiobook.narrator,
            # "publisher": audiobook.publisher,
            # "total_listening_time": str(audiobook.total_listening_time),
            # "licensing_cost": str(audiobook.licensing_cost),
            # "production_cost": str(audiobook.production_cost),
            # "royalty_percentage": str(audiobook.royalty_percentage),
            # "thumbnail": audio_file.thumbnail,
            # "audio_file_url": audio_file.file_url,
            # "author": {
            #     "name": author.name,
            #     "bio": author.bio,
            #     "first_name": author.first_name,
            #     "last_name": author.last_name
            # },
            # "narrator": {
            #     "name": narrator.name,
            #     "bio": narrator.bio,
            #     "first_name": narrator.first_name,
            #     "last_name": narrator.last_name
            # },
            # "publisher": {
            #     "name": publisher.name,
            #     "website": publisher.website,
            #     "address": publisher.address
                # "address_line1": publisher.address_line1,
                # "city": publisher.city,
                # "state": publisher.state,
                # "country": publisher.country
            # },
            # "subscription_level": {
                # "name": subscription_level.name1,
                # "monthly_price": subscription_level.monthly_price,
                # "annual_price": subscription_level.annual_price,
                # "access_frequency": subscription_level.access_frequency
            # }
        })

    return json.dumps({"success": True, "data": {"audiobooks": response_data, "total_count": total_count}})


@frappe.whitelist(allow_guest=False)
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
    response = {
        "id": audiobook.name,
        "title": audiobook.title,
        "author": audiobook.author,
        "narrator": audiobook.narrator,
        "duration": audiobook.total_listening_time,
        "description": audiobook.description,
        "cover_image_url": audiobook.cover_image_url,
        "audio_file_url": audiobook.audio_file_url,
        "release_date": audiobook.release_date,
        "average_rating": audiobook.average_rating,
        "num_ratings": audiobook.num_ratings,
        "is_favorite": is_favorite
    }

    return json.dumps({"success": True, "data": response})


@frappe.whitelist(allow_guest=False)
def retrieve_audiobook_sample(audiobook_id):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)

    # Perform user role and permission checks here
    # ...
    # Ensure the authenticated user has the necessary roles and permissions to access the API method

    audiobook_doc = frappe.get_doc("Audiobook", audiobook_id)
    audio_file_doc = frappe.get_doc("File", audiobook_doc.sample_audio_file)

    file_path = frappe.get_site_path("public", audio_file_doc.file_url[1:])
    filename = secure_filename(audio_file_doc.file_name)
    mimetype = mimetypes.guess_type(filename)[0]

    return Response(stream_with_context(send_file(file_path, mimetype=mimetype, as_attachment=True, attachment_filename=filename, streaming=True)), content_type=mimetype)



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