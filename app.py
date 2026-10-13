from flask import Flask, render_template, request, render_template_string

app = Flask(__name__)


@app.route("/")
@app.route("/index.html")
def home():
    return render_template("index.html")


@app.route("/about")
@app.route("/about.html")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
@app.route("/register.html", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        student_name = request.form.get("fullname", "")

        print("A new admission application was received.")
        print("Student name:", student_name)

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
                <p>Python has successfully received your form submission.</p>
                <a href="/register">Return to Admission Form</a>
            </body>
            </html>
        """, name=student_name)

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
