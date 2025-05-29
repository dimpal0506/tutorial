from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.title}>"

# Home page - view all tasks
@app.route('/')
def index():
    tasks = Task.query.order_by(Task.due_date).all()
    return render_template('index.html', tasks=tasks)

# Add a new task
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form.get('description')
        due_date = request.form.get('due_date')
        if due_date:
            due_date = datetime.strptime(due_date, '%Y-%m-%d')
        else:
            due_date = None

        new_task = Task(title=title, description=description, due_date=due_date)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_task.html')

# Update a task
@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form.get('description')
        due_date = request.form.get('due_date')
        task.due_date = datetime.strptime(due_date, '%Y-%m-%d') if due_date else None
        task.completed = 'completed' in request.form
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_task.html', task=task)

# Delete a task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

