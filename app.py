from flask import Flask, render_template, request, redirect, session
import psycopg2

app = Flask(__name__)
app.secret_key = "secret"

conn = psycopg2.connect(
    host="localhost",
    database="student_managment",
    user="postgres",
    password="admin123"
)

# Login Page
@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur = conn.cursor()
        cur.execute("SELECT * FROM admin WHERE username=%s AND password=%s",(username,password))
        admin = cur.fetchone()

        if admin:
            session["admin"] = username
            return redirect("/dashboard")

    return render_template("login.html")

#Home page 
@app.route("/home")
def home():
    return render_template("home.html")


# Dashboard
@app.route("/dashboard")
def dashboard():
    if "admin" in session:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students")
        data = cur.fetchall()
        return render_template("dashboard.html", students=data)
    return redirect("/")

#About
@app.route("/about")
def about():
    return render_template("about.html")


#Attandance
@app.route("/attendance/<int:id>", methods=["GET","POST"])
def attendance(id):

    cur = conn.cursor()

    if request.method == "POST":

        date = request.form["date"]
        status = request.form["status"]

        cur.execute(
        "INSERT INTO attendance(student_id,date,status) VALUES(%s,%s,%s)",
        (id,date,status)
        )

        conn.commit()

    cur.execute("SELECT * FROM attendance WHERE student_id=%s",(id,))
    data = cur.fetchall()

    return render_template("attendance.html", attendance=data, student_id=id)

#Students

@app.route("/students")
def students():

    cur = conn.cursor()

    cur.execute("SELECT * FROM students")

    data = cur.fetchall()

    return render_template("students.html", students=data)

# Add Student
@app.route("/add", methods=["POST"])
def add_student():
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    course = request.form["course"]

    cur = conn.cursor()
    cur.execute(
        "INSERT INTO students(name,email,phone,course) VALUES(%s,%s,%s,%s)",
        (name,email,phone,course)
    )
    conn.commit()

    return redirect("/dashboard")


# Delete Student
@app.route("/delete/<int:id>")
def delete_student(id):
    cur = conn.cursor()
    cur.execute("DELETE FROM students WHERE student_id=%s",(id,))
    conn.commit()

    return redirect("/dashboard")


# Edit Student
@app.route("/edit/<int:id>")
def edit_student(id):
    cur = conn.cursor()
    cur.execute("SELECT * FROM students WHERE student_id=%s",(id,))
    student = cur.fetchone()

    return render_template("edit_student.html", student=student)


# Update Student
@app.route("/update/<int:id>", methods=["POST"])
def update_student(id):
    name = request.form["name"]
    email = request.form["email"]
    phone = request.form["phone"]
    course = request.form["course"]

    cur = conn.cursor()
    cur.execute(
        "UPDATE students SET name=%s email=%s,phone=%s,course=%s WHERE student_id=%s",
        (name,email,phone,course,id)
    )
    conn.commit()

    return redirect("/dashboard")


# Logout
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)