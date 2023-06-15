from flask import request
from flask import Flask
from flask import render_template
import pyodbc
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

driver = '{ODBC Driver 17 for SQL Server}'
server = 'sqlserver-1002119262-saarthakmudigeregirish.database.windows.net'
database = 'DataBase-1002119262-SaarthakMudigereGirish'
username = 'saarthakmudigeregirish'
password = 'Hello123'

# Establish the connection
conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')

# Create a cursor object
cursor = conn.cursor()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/page1/", methods=['GET', 'POST'])
def page1():
    salpics = []
    salpics2 = []
    city = ""
    if request.method == "POST":
        city = request.form.get('city')

        query = "SELECT TOP(1) * FROM dbo.city WHERE City=?"
        cursor.execute(query, city)

        rows = cursor.fetchall()
        for i in rows:
            salpics.append(i)

        lat = salpics[0][2]
        long = salpics[0][3]

        query2 = "SELECT * FROM dbo.city WHERE ( 6371 * ACOS(COS(RADIANS(lat)) * COS(RADIANS(?)) * COS(RADIANS(lon) - RADIANS(?)) + SIN(RADIANS(lat)) * SIN(RADIANS(?)) )) <=10000 ; "
        cursor.execute(query2, lat, long, lat)
        row2 = cursor.fetchall()
        for i in row2:
            salpics2.append(i)

    return render_template("1)Page.html", city=city, salpics=salpics, salpics2=salpics2)

'''
@app.route("/page2/", methods=['GET', 'POST'])
def page2():
    minlat = ""
    maxlat = ""
    minlong = ""
    maxlong = ""
    system = ""
    salpics = []
    if request.method == "POST":
        minlan = request.form['minlan']
        maxlan = request.form['maxlan']
        minlong = request.form['minlong']
        maxlong = request.form['maxlong']
        days = request.form['days']
        # Execute a simple select query
        query = f"SELECT * FROM dbo.city WHERE lan BETWEEN ? AND ? AND lon BETWEEN ? AND ?"
        cursor.execute(query, minlan, maxlan, minlan, maxlong)
        row = cursor.fetchall()
        if row is None:
            system = None
        else:
            for i in row:
                salpics.append(i)
    return render_template("2)Page.html", salpics=salpics, system=system)


@app.route("/page3/", methods=['GET', 'POST'])
def page3():
    salpics = []
    distance = ""
    long = ""
    if request.method == "POST":
        lat = request.form['lat']
        long = request.form['long']
        distance = request.form['distance']

        query = "SELECT * FROM dbo.all_month WHERE ( 6371 * ACOS(COS(RADIANS(latitude)) * COS(RADIANS(?)) * COS(" \
                "RADIANS(longitude) - RADIANS(?)) + SIN(RADIANS(latitude)) * SIN(RADIANS(?)) )) <=? ; "
        cursor.execute(query, lat, long, lat, distance)
        row = cursor.fetchall()
        for i in row:
            salpics.append(i)
    return render_template("3)Page.html", salpics=salpics, distance=distance)


@app.route("/cluster/", methods=['GET', 'POST'])
def cluster():
    return render_template("4)cluster.html")


'''


@app.route("/page4a/", methods=['GET', 'POST'])
def page4a():
    salpics = []
    if request.method == "POST":
        city = request.form['city']
        state = request.form['state']
        pop = request.form['pop']
        lat = request.form['lat']
        long = request.form['long']

        # Execute a query
        query = "INSERT INTO dbo.city VALUES (?,?,?,?,?)"
        cursor.execute(query, city, state, pop, lat, long)
        conn.commit()

        query = "SELECT * FROM dbo.city WHERE lat=? AND lon=? AND population=?"
        cursor.execute(query, lat, long, pop)

        # Fetch a single row
        row = cursor.fetchone()
        # Access row values
        for i in range(len(row)):
            # Assuming the table has columns named 'column1', 'column2', and 'column3'
            salpics.append(row[i])

    return render_template("4)Pagea.html", salpics=salpics)


@app.route("/page4b/", methods=['GET', 'POST'])
def page4b():
    city = ""
    state = ""
    salpics = []
    system = ""
    if request.method == "POST":
        city = request.form['city']
        state = request.form['city']

        # Execute a query
        query = "SELECT * FROM dbo.city WHERE city=? AND state=?"
        cursor.execute(query, city, state)

        # Fetch a single row
        row = cursor.fetchone()
        if row is None:
            system = None
        else:
            # Access row values
            for i in range(len(row)):
                # Assuming the table has columns named 'column1', 'column2', and 'column3'
                salpics.append(row[i])

        query = "DELETE FROM dbo.city WHERE city=? AND state=?"
        cursor.execute(query, city, state)
        conn.commit()

    return render_template("4)Pageb.html", city=city, state=state, salpics=salpics, system=system)


if __name__ == "__main__":
    app.run(debug=True)
