from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired


class StudentForm(FlaskForm):
	first_name = StringField('Name', 
							validators=[DataRequired(), Length(min=2, max=20)],
							render_kw ={"placeholder": "First name"})
	last_name = StringField('Last name',
							validators = [DataRequired(),Length(min=2, max=20)],
							render_kw = {"placeholder": "Last name"})
	id_number = StringField('Identification Number',
							validators=[DataRequired(), Length(min=8, max=9)],
							render_kw = {"placeholder": "ID Number"})
	course = SelectField('Course', 
							choices = [])
	year_level = SelectField('Year Level',
							validators = [DataRequired()],
							render_kw = {"placeholder": "Year Level"} ,
							choices=[('1st Year', '1st Year'), 
									 ('2nd Year', '2nd Year'),
									 ('3rd Year', '3rd Year'), 
									 ('4th Year', '4th Year'),
									 ('5th Year', '5th Year')])
	gender = StringField('Gender',
							validators=[InputRequired(), Length(min=4, max=45)])
	submit = SubmitField('Submit')
	
class CoursesForm(FlaskForm):
	course_code = StringField('Course Code', 
							validators=[DataRequired(), Length(min=3, max =15)])
	course_name = StringField('Course Name',
							validators = [DataRequired(),Length(min=10, max =90)])
	college = SelectField('College Department',
							choices=[])
	submit = SubmitField('Submit')

class CollegeForm(FlaskForm):
	college_code = StringField('College Code', 
							validators=[DataRequired(), Length(min=3, max=8)])
	college_name = StringField('College Name',
							validators = [DataRequired(),Length(min=10, max=90)])
	submit = SubmitField('Submit')


class SearchStudentForm(FlaskForm):
	search_field = StringField(label='search',
						validators=[DataRequired()],)
	search_by = SelectField(label='Search By:',
						choices=[('all', 'All'),
									('id_number', 'ID Number'), 
									('first_name', 'First Name'),
									('last_name', 'Last name'),
									('course', 'Course'),
									('yr_level', 'Year Level'),
									('gender', 'Gender')])
	search_submit = SubmitField('Search')

class SearchCourseForm(FlaskForm):
	search_field = StringField('search',
						validators=[DataRequired()])
	search_by = SelectField(label='Search By:',
						choices=[('all', 'All'),
									('course_code', 'Course Code'), 
									('course_name', 'Course Name'),
									('course_college', 'College')])
	search_submit = SubmitField('Search')

class SearchCollegeForm(FlaskForm):
	search_field = StringField('search',
						validators=[DataRequired()])
	search_by = SelectField(label='Search By:',
						choices=[('all', 'All'),
									('college_code', 'College Code'), 
									('college_name', 'College Name')])
	search_submit = SubmitField('Search')



