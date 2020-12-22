from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import json, html
import os

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "jobs.db"))

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.secret_key = 'some random secret key'
db = SQLAlchemy(app)

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    description = db.Column(db.Text(2000))
    tags = db.Column(db.String(255))
    salary = db.Column(db.String(100))
    location = db.Column(db.String(100))

    def __repr__(self):
        return '<Job %r>' % self.title



@app.route('/')
def index():

    job1 = Job(title="Python developer", url="www.google.com", description="Very good job", tags="python, flask, aws", salary="$99,000", location="Germany")
    job2 = Job(title="Flask developer", url="www.linkedin.com", description="Very very super good job", tags="flask, react, aws", salary="$66,000", location="France")

    # db.session.add(job1)
    # db.session.add(job2)
    # db.session.commit()

    jobs = Job.query.all()
    for j in jobs:
        print(type(j))
    return render_template('index.html', jobs=jobs)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == "POST":
        title = request.form.get('title')
        desc = request.form.get('description')
        url = request.form.get('url')
        location = request.form.get('location')
        salary = request.form.get('salary')
        tags = request.form.get('tags')

        jobs = Job(title=title, description=desc, url=url, location=location, salary=salary, tags=tags)
        db.session.add(jobs)
        db.session.commit()
        return redirect('/')
    return render_template('add.html')


if __name__ == '__main__':
    app.run(debug=True)