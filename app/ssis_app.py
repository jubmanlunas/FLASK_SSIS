from flask import Flask, render_template, url_for, flash, redirect
from forms import StudentForm, CollegeForm, CoursesForm, SearchStudentForm, SearchCourseForm, SearchCollegeForm
from flask_mysqldb import MySQL


app = Flask(__name__)

app.config['SECRET_KEY'] = '6db52b5de40105e38bb4f3951b7c3303'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'gigatt02'
app.config['MYSQL_DB'] = 'ssis_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

 
mysql = MySQL(app)

@app.route('/')
@app.route('/view_students', methods=["POST", "GET"])
def view_students():
	form = StudentForm()
	search_form = SearchStudentForm()
	cur = mysql.connection.cursor()
	cur.execute(''' SELECT course_code, course_name FROM course ''')
	courses = cur.fetchall()
	course_options = [tuple(course.values()) for course in courses]
	form.course.choices = course_options
	cur.execute(''' SELECT * FROM students ''')
	students_data = cur.fetchall()
	return render_template('student/view_students.html', 
							students_data=students_data,
							search_form=search_form,
							form=form)

@app.route('/view_courses', methods=["POST", "GET"])
def view_courses():
	form = CoursesForm()
	search_form = SearchCourseForm()
	cur = mysql.connection.cursor()
	cur.execute(''' SELECT * FROM course ''')
	courses_data = cur.fetchall()
	cur = mysql.connection.cursor()
	cur.execute(''' SELECT college_code, college_name FROM college ''')
	colleges = cur.fetchall()
	college_options = [tuple(college.values()) for college in colleges]
	form.college.choices = college_options
	return render_template('course/view_courses.html', 
							courses_data=courses_data,
							form=form,
							search_form=search_form)

@app.route('/view_colleges')
def view_colleges():
	form = CollegeForm()
	search_form = SearchCollegeForm()
	cur = mysql.connection.cursor()
	cur.execute(''' SELECT * FROM college ''')
	colleges_data = cur.fetchall()
	return render_template('college/view_colleges.html', 
							colleges_data=colleges_data,
							form=form,
							search_form=search_form)

@app.route('/add_student',  methods=["POST", "GET"])
def add_student():
	form = StudentForm()
	cur = mysql.connection.cursor()
	cur.execute(''' SELECT course_code, course_name FROM course ''')
	courses = cur.fetchall()
	course_options = [tuple(course.values()) for course in courses]
	form.course.choices = course_options
	if form.validate_on_submit():
		first = form.first_name.data
		last = form.last_name.data
		idnumber = form.id_number.data
		kurso = form.course.data
		yrlevel = form.year_level.data
		gender = form.gender.data
		cur = mysql.connection.cursor()
		cur.execute('''INSERT INTO students VALUES(%s,%s,%s,%s,%s,%s)''',(idnumber,first, last, kurso,yrlevel,gender))
		mysql.connection.commit()
		flash("{} has been added".format(first), "success")
		return redirect(url_for('view_students'))
		cur.close()
	return render_template('student/view_students.html', title = 'Add Student', form = form)

@app.route('/add_course',  methods=["POST", "GET"])
def add_course():
	form = CoursesForm()
	cur = mysql.connection.cursor()
	cur.execute(''' SELECT college_code, college_name FROM college ''')
	colleges = cur.fetchall()
	college_options = [tuple(college.values()) for college in colleges]
	form.college.choices = college_options
	if form.validate_on_submit():
		course_code = form.course_code.data
		course_name = form.course_name.data
		college = form.college.data
		cur = mysql.connection.cursor()
		cur.execute('''INSERT INTO course VALUES(%s,%s,%s)''',(course_code,course_name, college))
		mysql.connection.commit()
		flash("{} has been added".format(course_code), "success")
		return redirect(url_for('view_courses'))
		cur.close()
	return render_template('course/view_courses.html', title = 'Add Course', form = form)


@app.route('/add_college',  methods=["POST", "GET"])
def add_college():
	form = CollegeForm()
	cur = mysql.connection.cursor()
	if form.validate_on_submit():
		college_code = form.college_code.data
		college_name = form.college_name.data
		cur = mysql.connection.cursor()
		cur.execute('''INSERT INTO college VALUES(%s,%s)''',(college_code,college_name))
		mysql.connection.commit()
		flash("College added successfully", "success")
		return redirect(url_for('view_colleges'))
		cur.close()
	return render_template('course/view_colleges.html', title = 'Add Course', form = form)

	

@app.route('/del_student/<id_number>', methods=["POST", "GET"])
def del_student(id_number):
	form = StudentForm()
	cursor = mysql.connection.cursor()
	cursor.execute("DELETE FROM students WHERE id_number = %s", (id_number,))
	cursor.close()
	mysql.connection.commit()
	flash("Student {}'s records have been deleted successfully.".format(id_number), 
          "danger")
	return redirect((url_for("view_students")))

@app.route('/del_course/<course_code>', methods=["POST", "GET"])
def del_course(course_code):
	cursor = mysql.connection.cursor()
	cursor.execute("DELETE FROM course WHERE course_code = %s", (course_code,))
	cursor.close()
	mysql.connection.commit()
	flash("Student {}'s records have been deleted successfully.".format(course_code), 
          "danger")
	return redirect((url_for("view_courses")))

@app.route('/del_college/<college_code>', methods=["POST", "GET"])
def del_college(college_code):
	cursor = mysql.connection.cursor()
	cursor.execute("DELETE FROM college WHERE college_code = %s", (college_code,))
	cursor.close()
	mysql.connection.commit()
	flash("Student {}'s records have been deleted successfully.".format(college_code), 
          "danger")
	return redirect((url_for("view_colleges")))



if __name__=='__main__':
	app.run(debug=True)