# Offline Meme Service

A Python application that lets you watch fresh memes offline, directly in your browser!  
**Backend:** Flask & Python  
**Frontend:** HTML, CSS, JavaScript

---

## Project Overview

**Offline Meme Service** is divided into two main components:

- **Web App (`app.py`):**  
  A local web server that serves meme videos to your browser, letting you browse and watch memes one by one.

- **Reddit Downloader (`downloader.py`):**  
  A command-line utility that fetches meme videos from [r/MemeVideos](https://reddit.com/r/MemeVideos), downloads them for offline use, and populates the local database.

---

## Getting Started

### Prerequisites

- Python 3.7 or newer  
- `pip` for installing dependencies


### Installation

1. **Clone this repository:**

    ```bash
    git clone https://github.com/J-Saeedi/offline-meme-service.git
    cd offline-meme-service
    ```

2. **Install required packages:**

    ```bash
    pip install flask requests sqlite3 redvid
    ```


---

## Usage

### Step 1: Download Memes

Before running the web server, you need to fill your local library with memes.

```bash
python3 downloader.py
```
This will create a database (`download/videos.db`) and download some videos from `r/MemeVideos`.
Wait a few seconds for the download and database setup to complete. *(no need to wait until it is done, after a few seconds go to the next step)*

###  Step 2: Run the Web Server

```bash
python3 app.py
```

This will start a Flask web server.

### Step 3: Open in Browser

Go to http://127.0.0.1:5000 in your web browser and enjoy your freshly downloaded meme videos!



## How To Use

 ### Next Video:
* Click the Next button or press the right arrow key on your keyboard to watch the next meme.

### Prevent Auto-Play:
* Click on the red bar to stop the next video from autoplaying.

### No Repeats:
* Every video shown is unique and won't be repeated in the same session.

### Tracking Unseen Memes:
* Check how many memes you have left to watch in download/videos.db.

### No Going Back:
* There is no way to go back to a previous meme, so savor each one!



## Directory Structure

```code
offline-meme-service/
├── app.py               # Flask web application
├── downloader.py        # Reddit video downloader
├── download/
│   └── videos.db        # Meme video database
│   └── [...]            # downloaded videos
├── static/              # CSS assets
│   └── style.css
└── templates/
    └── index.html
```

## Notes

 - Your meme library grows each time you run `downloader.py`.
 - `videos.db` tracks what you've already watched. Delete it to reset progress.
 - Subreddit Selection: Modify downloader.py to change the target subreddit (default: `r/MemeVideos`).
 - Video Limits: Adjust the `max_videos` parameter in `downloader.py` to control how many videos are downloaded.