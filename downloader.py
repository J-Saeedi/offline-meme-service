import requests
import sqlite3
import os
from redvid import Downloader  # Import redvid Downloader

# Initialize the Downloader object with max quality set to True
reddit = Downloader(max_q=True)

# Download function using the redvid object


def download(url):
    reddit.url = url
    reddit.download()
    print(f"{reddit.file_name=}")


def initialize_db(db_name="videos.db"):
    # Connect to the SQLite database (creates if it doesn't exist)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS video_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            file_path TEXT,
            url TEXT UNIQUE,
            is_seen BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    return conn, cursor


def is_url_in_db(cursor, url):
    """Check if a URL is already in the database."""
    cursor.execute("SELECT url FROM video_info WHERE url = ?", (url,))
    return cursor.fetchone() is not None


def save_video_info(cursor, title, file_path, url):
    """Save video information to the database."""
    cursor.execute(
        "INSERT INTO video_info (title, file_path, url) VALUES (?, ?, ?)", (title, file_path, url))


def main(subreddit_name="MemeVideos"):
    conn, cursor = initialize_db()

    # Reddit API URL for fetching top posts from a subreddit
    url = f"https://www.reddit.com/r/{subreddit_name}/top.json?t=all&limit=100"

    headers = {'User-Agent': 'video-downloader-script'}
    after = ""
    try:
        while 1:
            response = requests.get(url+f"&after={after}", headers=headers)
            response.raise_for_status()
            data = response.json()

            for post in data['data']['children']:
                post_data = post['data']

                if 'is_video' in post_data and post_data['is_video']:
                    title = post_data['title']
                    video_url = post_data['url']

                    # Check if the video URL is already in the database
                    if is_url_in_db(cursor, video_url):
                        print(f"Video already downloaded: {title}")
                        continue

                    # Download the video using the provided function
                    download(video_url)

                    # Retrieve the file name from the download object
                    # file_name = reddit.file_name
                    file_name = os.path.basename(reddit.file_name)
                    # file_path = os.path.join("videos", file_name)

                    # Save video info to DB
                    save_video_info(
                        cursor, title, os.path.basename(file_name), video_url)
                    conn.commit()
            after = data["data"]["after"]
            print(f"going to after={after}")

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    # Default to "MemeVideos" subreddit
    os.chdir("download")
    main()
