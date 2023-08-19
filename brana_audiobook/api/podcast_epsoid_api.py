import frappe

def get_podcast_episode_list(podcast):
    # Custom function to retrieve a list of Podcast Episodes for a given Podcast
    episodes = frappe.get_all(
        "Podcast Episode",
        filters={"podcast": podcast},
        fields=["name", "title", "description", "episode_number", "air_date", "audio_file", "total_listening_time"]
    )
    return episodes

