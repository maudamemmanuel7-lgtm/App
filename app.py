from flask import Flask, render_template, request, render_template_string, url_for
import sqlite3
import os

app = Flask(__name__)
MEDIA_FOLDER = os.path.join(app.static_folder, "media")

CATEGORIES = {
    "education": "Education",
    "nature": "Nature",
    "technology": "Technology",
    "sports": "Sports",
    "entertainment": "Entertainment",
    "general": "General"
}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
VIDEO_EXTENSIONS = {".mp4", ".webm", ".ogg", ".mov"}


def get_media():
    media = []

    for media_type in ("pictures", "videos"):
        for category, category_name in CATEGORIES.items():
            folder = os.path.join(MEDIA_FOLDER, media_type, category)

            if not os.path.isdir(folder):
                continue

            for filename in sorted(os.listdir(folder)):
                filepath = os.path.join(folder, filename)

                if not os.path.isfile(filepath):
                    continue

                extension = os.path.splitext(filename)[1].lower()

                if media_type == "pictures":
                    if extension not in IMAGE_EXTENSIONS:
                        continue
                    kind = "picture"
                else:
                    if extension not in VIDEO_EXTENSIONS:
                        continue
                    kind = "video"

                media.append({
                    "name": filename,
                    "category": category,
                    "category_name": category_name,
                    "kind": kind,
                    "url": url_for(
                        "static",
                        filename=f"media/{media_type}/{category}/{filename}"
                    )
                })

    return media

DATABASE = os.path.join(
os.path.dirname(os.path.abspath(__file__)),
"admissions.db"
)

@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")

@app.route("/about")
@app.route("/about.html")
def about():
    return render_template("about.html")

@app.route("/gallery")
@app.route("/gallery.html")
def gallery():
    media = get_media()
    return render_template(
        "gallery.html",
        media=media,
        categories=CATEGORIES
    )

@app.route("/register", methods=["GET", "POST"])
@app.route("/register.html", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        student_name = request.form.get("fullname", "").strip()
        print("FORM SUBMITTED:", repr(student_name))

        if not student_name:
            return "Please enter the student's full name."

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute(
        "INSERT INTO applications (fullname) VALUES (?)",
        (student_name,)
        )

        connection.commit()
        connection.close()

        print("A new admission application was received.")
        print("Student name:", student_name)
        print("Application saved to the database.")

        return render_template_string("""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Application Received</title>
    </head>
    <body style="font-family: Arial; text-align: center; padding: 50px;">
        <h1>Application Received!</h1>
        <p>Thank you, {{ name }}.</p>
        <p>Your application has been saved successfully.</p>
        <a href="/register">Return to Admission Form</a>
    </body>
    </html>
        """, name=student_name)

    return render_template("register.html")
if __name__ == "__main__":
    app.run(debug=True)
