import frappe
from frappe.utils import format_duration
# @frappe.whitelist()
# def retrieve_podcasts(search=None, page=None, limit=None):
#     filters = {}
#     if search:
#         filters["title"] = ["like", f"%{search}%"]
#     podcasts = get_list(
#         "Podcast",
#         filters=filters,
#         fields=["name", 
#                 "title", 
#                 "host", 
#                 "description",
#                 "host", 
#                 "cover_image_url",
#                 "publisher",
#                 "subscription_level", 
#                 "audio_file", 
#                 "total_listening_time",
#                 "licensing_cost",
#                 # "royality_percentage"
#                 ],
#         or_filters=[],
#         limit_page_length=limit,
#         start=page * limit if page and limit else None
#     )

#     total_count = get_all(
#         "Podcast",
#         filters=filters,
#         fields=["count(*) as total_count"]
#     )[0].total_count

#     # Get the currently logged-in user
#     session = frappe.session.user
#     user_favorite_podcasts = get_list(
#         "User Favorite",
#         filters={"user": session},
#         fields=["audio_content"],
#     )

#     favorite_podcast_ids = [fav.audio_content for fav in user_favorite_podcasts]

#     for podcast in podcasts:
#         podcast["is_favorite"] = podcast["name"] in favorite_podcast_ids

#     response = {
#         "podcasts": podcasts,
#         "total_count": total_count
#     }
#     return response
@frappe.whitelist(allow_guest=True)
def retrieve_podcasts(search=None, page=1, limit=20):
    if not frappe.session.user:
        frappe.throw("User not authenticated", frappe.AuthenticationError)
    filters = []
    if search:
        filters.append(f"(ab.title LIKE '%{search}%' OR aut.name LIKE '%{search}%' OR nar.name LIKE '%{search}%')")
    filters_str = " AND ". join(filters)
    offset = (page - 1) * limit
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
        total_bodcast_count = frappe.get_value(
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
            response_data.append({
                "title": podcast.title,
                "description": podcast.description,
                "Host": host.full_name,
                "cover image": cover_image_url,
                "episodes" : []
        })
            for episode in episodes:
                response_data[-1]["episodes"].append({
                "title": episode.title,
                "duration" : format_duration(episode.duration),
                "podcast Number" : episode.episode_number
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
    # Retrieve User Favorite
    user_favorite = frappe.get_value(
        "User Favorite",
        filters={"user": frappe.session.user, "audio_content": podcast_id},
        fieldname="name"
    )
    host = frappe.get_doc("User", podcast.host)
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
        "total episodes" : total_episode_count
        # Is bookmarked ?
        # "is_favorite": is_favorite
    }
    for episode in episodes:
                response["episodes"].append({
                "title": episode.title,
                "duration" : format_duration(episode.duration),
                "podcast Number" : episode.episode_number
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
            response_data.append({
                "title": podcast.title,
                "description": podcast.description,
                "Host": host.full_name,
                "cover image": cover_image_url,
                "episodes" : [],
                "total episodes" : total_episode_count
        })
            for episode in episodes:
                response_data[-1]["episodes"].append({
                "title": episode.title,
                "duration" : format_duration(episode.duration),
                "podcast Number" : episode.episode_number
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
                "episodes" : [],
                "total episodes" : total_episode_count
        })
            for episode in episodes:
                response_data[-1]["episodes"].append({
                "title": episode.title,
                "duration" : format_duration(episode.duration),
                "podcast Number" : episode.episode_number
            })
        return response_data
    else:
        return "No Editor picks Podcast found."
