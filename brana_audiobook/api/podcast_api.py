import frappe
from frappe.utils import format_duration
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
    favorite = frappe.get_doc("Brana User Profile", user.email)
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
            if not favorite.wish_list:
                is_favorite = 0
            else:
                for item in favorite.wish_list:
                    if item.title == podcast.title:
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
    favorite = frappe.get_doc("Brana User Profile", user.email)
    host = frappe.get_doc("User", podcast.host)
    is_favorite = 0
    if not favorite.wish_list:
        is_favorite = 0
    else:
        for item in favorite.wish_list:
            if item.title == podcast_id:
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
    favorite = frappe.get_doc("Brana User Profile", user.email)
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
            if not favorite.wish_list:
                is_favorite = 0
            else:
                for item in favorite.wish_list:
                    if item.title == podcast.title:
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
    favorite = frappe.get_doc("Brana User Profile", user.email)
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
            if not favorite.wish_list:
                is_favorite = 0
            else:
                for item in favorite.wish_list:
                    if item.title == podcast.title:
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
