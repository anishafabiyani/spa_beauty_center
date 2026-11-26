from flask import Flask, render_template, request, redirect, session
import pymysql

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database connection
db = pymysql.connect(host="localhost", user="root", password="", database="spa_center_db")
cursor = db.cursor()

# Home Page with Form
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        first_name = request.form["first_name"]
        email = request.form["email"]
        plan = request.form["plan"]
        booking_date = request.form["booking_date"]
        comments = request.form["comments"]

        sql = "INSERT INTO bookings (first_name, email, plan, booking_date, comments) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (first_name, email, plan, booking_date, comments))
        db.commit()
        
        return "Booking Successful!"
    
    return render_template("index.html")

# Admin Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        cursor.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()
        
        if user:
            session["admin"] = username
            return redirect("/admin")
        else:
            return "Invalid Credentials!"
    
    return render_template("login.html")

# Admin Panel to View Bookings
@app.route("/admin")
def admin_panel():
    if "admin" in session:
        cursor.execute("SELECT * FROM bookings")
        data = cursor.fetchall()
        return render_template("admin.html", data=data)
    return redirect("/login")

# Logout
@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect("/login")

if __name__ == "__main__":
    app.run(debug=True)
