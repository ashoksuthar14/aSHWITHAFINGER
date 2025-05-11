from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)

# File to store student data
STUDENTS_FILE = 'students.json'

def load_students():
    if os.path.exists(STUDENTS_FILE):
        with open(STUDENTS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_students(students):
    with open(STUDENTS_FILE, 'w') as f:
        json.dump(students, f, indent=4)

def calculate_age(dob):
    today = datetime.now()
    birth_date = datetime.strptime(dob, '%Y-%m-%d')
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/students')
def students():
    return render_template('students.html')

@app.route('/register_student', methods=['POST'])
def register_student():
    students = load_students()
    
    name = request.form['name']
    rollno = request.form['rollno']
    dob = request.form['dob']
    email = request.form['email']
    
    # Calculate age
    age = calculate_age(dob)
    
    # Add student data
    students[rollno] = {
        'name': name,
        'rollno': rollno,
        'dob': dob,
        'age': age,
        'college': 'VJIT',
        'branch': 'AI',
        'email': email
    }
    
    save_students(students)
    return redirect(url_for('students'))

@app.route('/search_student')
def search_student():
    rollno = request.args.get('rollno', '').strip()
    students = load_students()
    student = students.get(rollno)
    return render_template('students.html', student=student, search_rollno=rollno)

if __name__ == '__main__':
    app.run(debug=True)
