from flask import Flask, render_template, request, redirect
import pymysql
from werkzeug.middleware.proxy_fix import ProxyFix  # Handles reverse proxy headers

pymysql.install_as_MySQLdb()
import MySQLdb

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

# Redirect www.getpharmo.com to getpharmo.com
@app.before_request
def redirect_www():
    if request.host.startswith("www."):
        return redirect(request.url.replace("www.", "", 1), code=301)

# MySQL Database Connection
db = MySQLdb.connect(
    host="tramway.proxy.rlwy.net",
    port=54114,
    user="root",
    password="hOQnmWNoBVBYyjjWlZrzvZvCMApaZIvT",
    database="railway"
)

@app.route('/', methods=['GET', 'POST'])
def home():
    success_message = ""
    error_message = ""

    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        subject = request.form.get("subject")
        message = request.form.get("message")

        if name and email and phone and subject and message:
            try:
                cursor = db.cursor()
                insert_query = """
                    INSERT INTO contacts (name, email, phone, subject, message)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (name, email, phone, subject, message))
                db.commit()
                success_message = "Successfully stored in the database!"
            except Exception as e:
                print(f"Error inserting into database: {e}")
                db.rollback()
                error_message = "Error storing data in the database. Please try again."
            finally:
                cursor.close()
        else:
            error_message = "Please fill in all required fields."

    return render_template('index.html', success_message=success_message, error_message=error_message)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('servicesmid.html')

@app.route('/services-right')
def services_right():
    return render_template('servicesright.html')

@app.route('/services-left')
def services_left():
    return render_template('servicesleft.html')

@app.route('/nine-nine-nine')
def nine_nine_nine():
    return render_template('999.html')

@app.route('/one-nine-nine-nine')
def one_nine_nine_nine():
    return render_template('1999.html')

@app.route('/two-nine-nine-nine')
def two_nine_nine_nine():
    return render_template('2999.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
