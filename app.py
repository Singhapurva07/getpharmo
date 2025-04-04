from flask import Flask, render_template, request
import pymysql

pymysql.install_as_MySQLdb()  # Install PyMySQL as MySQLdb
import MySQLdb  # Import MySQLdb after installation

app = Flask(__name__)

# MySQL Database Connection using MySQLdb
db = MySQLdb.connect(
    host="localhost",
    port=3306,  # Default MySQL port
    user="root",  # Replace with your local MySQL username
    password="theanimesh2005",  # Replace with your local MySQL password
    database="hospital_db"  # Replace with the name of your local database
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

        if name and email and phone and subject and message:  # Validation check
            try:
                cursor = db.cursor()  # Create a cursor for executing SQL queries
                insert_query = """
                    INSERT INTO contacts (name, email, phone, subject, message)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(insert_query, (name, email, phone, subject, message))
                db.commit()  # Commit the transaction
                success_message = "Successfully stored in the database!"  # Success message
            except Exception as e:
                print(f"Error inserting into database: {e}")
                db.rollback()  # Rollback if there's an error
                error_message = "Error storing data in the database. Please try again."
            finally:
                cursor.close()  # Close the cursor
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
