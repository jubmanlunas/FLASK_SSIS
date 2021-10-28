from flask import render_template, url_for, flash, redirect, request
from app.forms import *
from app import app, mysql

@app.route('/')
@app.route('/view_students', methods=["POST", "GET"])
def view_students():
	form = StudentForm()
	search_form = SearchStudentForm()
	form.course.choices = course_options()
	cur = mysql.connection.cursor()
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
	form.college.choices = college_options()
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
	form.course.choices = course_options()
	if form.validate_on_submit():
		id_number = form.id_number.data
		first_name = form.first_name.data
		last_name = form.last_name.data
		course = form.course.data
		yr_level = form.year_level.data
		gender = form.gender.data
		cur = mysql.connection.cursor()
		cur.execute(''' INSERT INTO students VALUES(%s,%s,%s,%s,%s,%s) ''',(id_number,first_name, last_name, course, yr_level, gender))
		mysql.connection.commit()
		flash("Student has been added, successfully!", "success")
		return redirect(url_for('view_students'))
		cur.close()
	return render_template('student/view_students.html', title = 'Add Student', form = form)

@app.route('/add_course',  methods=["POST", "GET"])
def add_course():
	form = CoursesForm()
	form.college.choices = college_options()
	if form.validate_on_submit():
		course_code = form.course_code.data
		course_name = form.course_name.data
		college = form.college.data
		cur = mysql.connection.cursor()
		cur.execute(''' INSERT INTO course VALUES(%s,%s,%s) ''',(course_code,course_name, college))
		mysql.connection.commit()
		flash("Course has been added, successfully!", "success")
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
		cur.execute(''' INSERT INTO college VALUES(%s,%s) ''',(college_code,college_name))
		mysql.connection.commit()
		flash("College has been added, successfully!", "success")
		return redirect(url_for('view_colleges'))
		cur.close()
	return render_template('course/view_colleges.html', title = 'Add Course', form = form)


@app.route('/edit_student/<id_number>',  methods=["POST", "GET"])
def edit_student(id_number):
	cursor = mysql.connection.cursor()
	cursor.execute(''' SELECT * FROM students WHERE id_number = %s ''', (id_number,))
	existing_data = cursor.fetchall()
	data = [tuple(data.values()) for data in existing_data]
	form = StudentForm()
	form.course.choices = course_options()
	if form.validate_on_submit():
		first_name = form.first_name.data
		last_name = form.last_name.data
		id_ = form.id_number.data
		course = form.course.data
		yr_level = form.year_level.data
		gender = form.gender.data
		cur = mysql.connection.cursor()
		cur.execute(''' UPDATE students SET first_name = %s, 
											last_name = %s, 
											course = %s, 
											year_level = %s, 
											gender = %s 
										WHERE id_number = %s ''',(first_name, last_name, course, yr_level, gender, id_))
		mysql.connection.commit()
		flash("Student has been updated, successfully!", "success")
		return redirect(url_for('view_students'))
		cur.close()

	elif request.method == "GET":
		form.id_number.data = data[0][0]
		form.first_name.data = data[0][1]
		form.last_name.data = data[0][2]
		form.course.data = data[0][3]
		form.year_level.data = data[0][4]
		form.gender.data = data[0][5]
		form.submit.label.text = "Update"
	return render_template('student/edit_student.html', 
							title = 'Update Student', 
							id_number=id_number,
							form=form)

@app.route('/edit_course/<course_code>',  methods=["POST", "GET"])
def edit_course(course_code):
	cursor = mysql.connection.cursor()
	cursor.execute(''' SELECT * FROM course WHERE course_code = %s ''', (course_code,))
	existing_data = cursor.fetchall()
	data = [tuple(data.values()) for data in existing_data]
	form = CoursesForm()
	form.college.choices = college_options()
	if form.validate_on_submit():
		course_coda=form.course_code.data
		course_name = form.course_name.data
		college = form.college.data
		cur = mysql.connection.cursor()
		cur.execute(''' UPDATE course SET course_name = %s, 
										  course_college = %s
										WHERE course_code = %s ''',( course_name, college, course_coda,))
		mysql.connection.commit()
		flash("Course has been updated, successfully!", "success")
		return redirect(url_for('view_courses'))
		cur.close()

	elif request.method == "GET":
		form.course_code.data = data[0][0]
		form.course_name.data = data[0][1]
		form.college.data = data[0][2]
		form.submit.label.text = "Update"
	return render_template('course/edit_courses.html', 
							title = 'Update Student', 
							form = form)

@app.route('/edit_college/<college_code>',  methods=["POST", "GET"])
def edit_college(college_code):
	cursor = mysql.connection.cursor()
	cursor.execute(''' SELECT * FROM college WHERE college_code = %s ''', (college_code,))
	existing_data = cursor.fetchall()
	data = [tuple(data.values()) for data in existing_data]
	form = CollegeForm()
	if form.validate_on_submit():
		college_coda=form.college_code.data
		college_name = form.college_name.data
		cur = mysql.connection.cursor()
		cur.execute(''' UPDATE college SET college_name = %s 
										WHERE college_code = %s ''',( college_name, college_coda,))
		mysql.connection.commit()
		flash("College has been updated, successfully!", "success")
		return redirect(url_for('view_colleges'))
		cur.close()

	elif request.method == "GET":
		form.college_code.data = data[0][0]
		form.college_name.data = data[0][1]
		form.submit.label.text = "Update"
	return render_template('college/edit_college.html', 
							title = 'Update College', 
							form = form)


@app.route('/del_student/<id_number>', methods=["POST", "GET"])
def del_student(id_number):
	form = StudentForm()
	cursor = mysql.connection.cursor()
	cursor.execute("DELETE FROM students WHERE id_number = %s", (id_number,))
	cursor.close()
	mysql.connection.commit()
	flash("Student has been deleted, successfully!", 
          "danger")
	return redirect((url_for("view_students")))

@app.route('/del_course/<course_code>', methods=["POST", "GET"])
def del_course(course_code):
	cursor = mysql.connection.cursor()
	cursor.execute("DELETE FROM course WHERE course_code = %s", (course_code,))
	cursor.close()
	mysql.connection.commit()
	flash("Course has been deleted, successfully!", 
          "danger")
	return redirect((url_for("view_courses")))

@app.route('/del_college/<college_code>', methods=["POST", "GET"])
def del_college(college_code):
	cursor = mysql.connection.cursor()
	cursor.execute("DELETE FROM college WHERE college_code = %s", (college_code,))
	cursor.close()
	mysql.connection.commit()
	flash("College has been deleted, successfully!", 
          "danger")
	return redirect((url_for("view_colleges")))


@app.route('/student_search', methods=["POST", "GET"])
def student_search():
	search_form = SearchStudentForm()
	form = StudentForm()
	field = search_form.search_field.data
	searchby = search_form.search_by.data
	cursor = mysql.connection.cursor()
	if(searchby == 'all'):
		cursor.execute(''' SELECT * FROM students WHERE id_number REGEXP %s or 
														first_name REGEXP %s or 
														last_name REGEXP %s or 
														course REGEXP %s or
														year_level REGEXP %s or
														gender REGEXP %s ''', ([field], [field], [field], [field], [field], [field]))
		students_data = cursor.fetchall()
	if(searchby == 'id_number'):
		cursor.execute(''' SELECT * FROM students WHERE id_number REGEXP %s ''', [field])
		students_data = cursor.fetchall()
	if(searchby == 'first_name'):
		cursor.execute(''' SELECT * FROM students WHERE first_name REGEXP %s ''', [field])
		students_data = cursor.fetchall()
	if(searchby == 'last_name'):
		cursor.execute(''' SELECT * FROM students WHERE last_name REGEXP %s ''', [field])
		students_data = cursor.fetchall()
	if(searchby == 'course'):
		cursor.execute(''' SELECT * FROM students WHERE course REGEXP %s ''', [field])
		students_data = cursor.fetchall()
	if(searchby == 'yr_level'):
		cursor.execute(''' SELECT * FROM students WHERE year_level REGEXP %s ''', [field])
		students_data = cursor.fetchall()
	if(searchby == 'gender'):
		cursor.execute(''' SELECT * FROM students WHERE gender REGEXP %s ''', [field])
		students_data = cursor.fetchall()
	flash("Search results for \" {} \"".format(field), 
          "success")
	return render_template('student/view_students.html', 
							students_data=students_data,
							search_form=search_form,
							form=form,
							title='Search Results') 

@app.route('/course_search', methods=["POST", "GET"])
def course_search():
	search_form = SearchCourseForm()
	form = CoursesForm()
	field = search_form.search_field.data
	searchby = search_form.search_by.data
	cursor = mysql.connection.cursor()
	if(searchby == 'all'):
		cursor.execute(''' SELECT * FROM course WHERE course_code REGEXP %s or 
														course_name REGEXP %s or 
														course_college REGEXP %s ''', ([field], [field], [field]))
		courses_data = cursor.fetchall()
	if(searchby == 'course_code'):
		cursor.execute(''' SELECT * FROM course WHERE course_code REGEXP %s ''', [field])
		courses_data = cursor.fetchall()
	if(searchby == 'course_name'):
		cursor.execute(''' SELECT * FROM course WHERE course_name REGEXP %s ''', [field])
		courses_data = cursor.fetchall()
	if(searchby == 'course_college'):
		cursor.execute(''' SELECT * FROM course WHERE course_college REGEXP %s ''', [field])
		courses_data = cursor.fetchall()
	flash("Search results for \" {} \"".format(field), 
          "success")
	return render_template('course/view_courses.html', 
							courses_data=courses_data,
							search_form=search_form,
							form=form,
							title='Search Results') 

@app.route('/college_search', methods=["POST", "GET"])
def college_search():
	search_form = SearchCollegeForm()
	form = CollegeForm()
	field = search_form.search_field.data
	searchby = search_form.search_by.data
	cursor = mysql.connection.cursor()
	if(searchby == 'all'):
		cursor.execute(''' SELECT * FROM college WHERE college_code REGEXP %s or 
														college_name REGEXP %s ''', ([field], [field]))
		colleges_data = cursor.fetchall()
	if(searchby == 'college_code'):
		cursor.execute(''' SELECT * FROM college WHERE college_code REGEXP %s ''', [field])
		colleges_data = cursor.fetchall()
	if(searchby == 'college_name'):
		cursor.execute(''' SELECT * FROM college WHERE college_name REGEXP %s ''', [field])
		colleges_data = cursor.fetchall()
	flash("Search results for \" {} \"".format(field), 
          "success")
	return render_template('college/view_colleges.html', 
							colleges_data=colleges_data,
							search_form=search_form,
							form=form,
							title='Search Results') 


def course_options():
	cursor = mysql.connection.cursor()
	cursor.execute(''' SELECT course_code, course_name FROM course ''')
	courses = cursor.fetchall()
	options = [tuple(course.values()) for course in courses]
	return options

def college_options():
	cursor = mysql.connection.cursor()
	cursor.execute(''' SELECT college_code, college_name FROM college ''')
	colleges = cursor.fetchall()
	options = [tuple(college.values()) for college in colleges]
	return options


