import os
from atproto import Client
from dotenv import load_dotenv

load_dotenv()

blueSkyUsername = os.environ.get("BLUESKY_HANDLE")
blueSkyPassword = os.environ.get("BLUESKY_PASSWORD")

client = Client()
client.login(blueSkyUsername, blueSkyPassword)


def post_bluesky_message(message: str):
    post = client.send_post(message)
    return post


def scrape_bluesky_posts(bluesky_profile_handle: str):
    """
    Scrapes a BlueSky user's original posts and returns them as a list of dictionaries.
    Each dictionary contains the following keys:
    - text: the content of the post
    - createdAt: the date and time the post was created
    """
    data = client.get_author_feed(
        actor=bluesky_profile_handle,
        filter='posts_and_author_threads',
        limit=30
    )

    # Extract text and created_at fields from the response
    posts = [
        {
            "text": item.post.record.text,
            "createdAt": item.post.record.created_at,
        }
        for item in data.feed
        if hasattr(item, "post") and hasattr(item.post, "record")
    ]

    return posts


if __name__ == "__main__":
    # post_bluesky_message("Nothing to see here, just trying out the atproto Python SDK.")
    print(
        scrape_bluesky_posts(bluesky_profile_handle="sflahave.bsky.social")
    )
