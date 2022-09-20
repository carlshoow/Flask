from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

#__init__
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo_sqlite'
db = SQLAlchemy(app)


#Model database
class TodoDatabase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100))
    status = db.Column(db.Boolean)



@app.route('/add', methods=['POST'])
def add_task():
    task = request.form.get('title')
    new_task = TodoDatabase(task=task, status=False)
    db.session.add(new_task)
    try:
        db.session.commit()
    except:
        print(new_task.task, new_task.status)
    
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    to_delete = TodoDatabase.query.filter_by(id=task_id).first()
    db.session.delete(to_delete)
    try:
        db.session.commit()
    except:
        print("delete was a fail")
    
    return redirect(url_for('index'))

@app.route('/update/<int:task_id>')
def update_task(task_id):
    to_update = TodoDatabase.query.filter_by(id=task_id).first()
    to_update.status = not to_update.status
    
    try:
        db.session.commit()
    except:
        print("delete was a fail")
    
    return redirect(url_for('index'))



#main page
@app.route('/')
def index():
    todo_tasks = TodoDatabase.query.all()
    return render_template('index.html', tasks=todo_tasks)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

