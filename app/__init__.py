from flask import Flask,render_template,request,redirect,url_for,flash
import mysql.connector

app=Flask(__name__)
app.secret_key = "secret key"
mydb = mysql.connector.connect(
    host="forlearn.mysql.database.azure.com",
    port=3306,
    user="zebi",
    passwd="18082001Rak.",
    database="students"
)
cur = mydb.cursor()


@app.route('/')
def welcome():
    return render_template("index.html")

@app.route('/create',methods=['POST',"GET"])
def create():
    if request.method=="POST":
        roll = int(request.form['roll'])
        fname=str(request.form['fname'])
        lname=str(request.form['lname'])
        email=str(request.form['email'])
        phone=str(request.form['phone'])
        cgpa=round(float(request.form['cgpa']),2)
        cur.execute('select roll from student')
        if roll in cur:
            flash('Roll already added')
        elif fname!="" and not(roll in cur):
            cur.execute("insert into student (roll, fname, lname, email, phone, cgpa) values ('{}','{}','{}','{}','{}','{}')".format(roll,fname,lname,email,phone,cgpa))
            flash("Student added")
            mydb.commit()
        return redirect(url_for("create"))
    return render_template('create_form.html')

@app.route('/view',methods=['POST',"GET"])
def view():
    cur.execute('select * from student')
    t=[i for i in cur.fetchall()]
    return render_template('view_form.html',rows=t)

@app.route('/view-single',methods=['POST','GET'])
def viewsingle():
    if request.method=="POST":
        roll=int(request.form['roll'])
        cur.execute('select roll from student')
        rolls=[i[0] for i in cur.fetchall()]
        if roll!=0 and (roll in rolls):
            cur.execute("select * from student where roll={}".format(roll))
            temp=[i for i in cur.fetchall()]
            t=[i for i in temp[0]]
            return render_template('view_single.html',rows=t)
    t=['null','null','null','null','null','null']
    return render_template("view_single.html",rows=t)

@app.route('/update',methods=['POST',"GET"])
def update():
    if request.method=='POST':
        roll = int(request.form['roll'])
        fname=str(request.form['fname'])
        lname=str(request.form['lname'])
        email=str(request.form['email'])
        phone=str(request.form['phone'])
        cgpa=round(float(request.form['cgpa']),2)
        cur.execute('select roll from student')
        rolls=[i[0] for i in cur.fetchall()]
        if fname!="" and (roll in rolls):
            cur.execute('update student set fname="{}", lname="{}", email="{}", phone="{}", cgpa="{}" where roll={}'.format(fname,lname,email,phone,cgpa,roll))
            mydb.commit()
            flash("Student Modified")
            return redirect(url_for('update'))
        elif not(roll in rolls):
            flash('Student not found')
    return render_template('update_form.html')

@app.route('/delete', methods=['POST','GET'])
def delete():
    if request.method=='POST':
        roll=int(request.form['roll'])
        if roll!=0:
            cur.execute('select roll from student')
            rolls=[i[0] for i in cur.fetchall()]
            if not(roll in rolls):
                flash("Student not found")
                return redirect(url_for('delete'))
            cur.execute('delete from student where roll={}'.format(roll))
            mydb.commit()
            flash("Student Deleted")
        return redirect(url_for("delete"))
    return render_template('delete_form.html')  