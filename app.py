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

        query2 = "SELECT * FROM dbo.city WHERE ( 6371 * ACOS(COS(RADIANS(lat)) * COS(RADIANS(?)) * COS(RADIANS(lon) - RADIANS(?)) + SIN(RADIANS(lat)) * SIN(RADIANS(?)) )) <=100 ; "
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
    days = ""
    if request.method == "POST":
        minlan = request.form['minlan']
        maxlan = request.form['maxlan']
        minlong = request.form['minlong']
        maxlong = request.form['maxlong']
        days = request.form['days']
        # Execute a simple select query
        query = f"SELECT * FROM dbo.all_month WHERE mag BETWEEN ? AND ? AND CAST(time AS DATE) BETWEEN '2023-06-01' AND '2023-06-{days}'"
        cursor.execute(query, min, max)
        row = cursor.fetchall()
        if row is None:
            system = None
        else:
            for i in row:
                salpics.append(i)
    return render_template("2)Page.html", range=range, salpics=salpics, system=system)


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



@app.route("/remove/", methods=['GET', 'POST'])
def remove():
    name = ""
    salpics = []
    system = ""
    if request.method == "POST":
        name = request.form.get('name')

        # Execute a query
        query = "SELECT * FROM dbo.q1c WHERE name=?"
        cursor.execute(query, name)

        # Fetch a single row
        row = cursor.fetchone()
        print(row)
        if row is None:
            system = None
        else:
            # Access row values
            for i in range(len(row)):
                # Assuming the table has columns named 'column1', 'column2', and 'column3'
                salpics.append(row[i])

        query = "DELETE FROM dbo.q1c WHERE name = ?"
        cursor.execute(query, name)
        conn.commit()

    return render_template("remove.html", name=name, salpics=salpics, system=system)
'''


@app.route("/page4/", methods=['GET', 'POST'])
def page4():
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

    return render_template("4)Page.html", salpics=salpics)
'''

@app.route("/edit/", methods=['GET', 'POST'])
def edit():
    name = ""
    col = ""
    ele = ""
    if request.method == "POST":
        name = request.form.get('name')
        col = request.form.get('col')
        ele = request.form.get('ele')

        # Execute a simple select query
        query = "UPDATE dbo.q1c SET ?=? WHERE name=?"
        cursor.execute(query, col, ele, name)
        conn.commit()

    return render_template("edit.html", name=name, col=col, ele=ele)
'''

if __name__ == "__main__":
    app.run(debug=True)
