from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import sqlite3

app = Flask(__name__)
VIDEO_DIR = 'download'
DB_PATH = 'download/videos.db'


def get_unseen_videos():
    with sqlite3.connect(DB_PATH) as conn:
        return [{'title': row[0],
                 'url': row[1],
                 'video': row[2]
                 } for row in conn.execute(
            """SELECT title, url, file_path  FROM video_info WHERE is_seen=FALSE""")]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/videos')
def api_videos():
    return jsonify(get_unseen_videos())


@app.route('/seen', methods=['POST'])
def mark_seen():
    filename = request.json.get('filename')
    if filename:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute("""
            UPDATE video_info
            SET is_seen = TRUE
            WHERE file_path = ?
        """, (filename,))
        return jsonify(status='ok')
    return jsonify(status='error'), 400


@app.route('/videos/<path:filename>')
def serve_video(filename):
    return send_from_directory(VIDEO_DIR, filename)


if __name__ == '__main__':
    print((get_unseen_videos()))
    app.run(debug=True)
