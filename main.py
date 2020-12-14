from datetime import datetime

from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    comleted = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']

        if task_content == '':
            pass

        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()

            return redirect('/')
        except AssertionError as error:
            print(error)
            return "An exception occurred"

    else:
        tasks = Todo.query.order_by(Todo.created_at).all()

        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if request.method == 'POST':
        method = request.form['_method']

        if method == 'DELETE':
            task_to_delete = Todo.query.get_or_404(id)

            try:
                db.session.delete(task_to_delete)
                db.session.commit()

                return redirect('/')
            except AssertionError as error:
                print(error)

                return "An exception occurred trying to delete the task"
        else:
            return redirect('/')
    else:
        return redirect('/')


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        method = request.form['_method']

        if method == 'PUT':
            try:
                task.content = request.form['content']

                db.session.commit()

                return redirect('/')
            except AssertionError as error:
                print(error)

                return "An exception occurred trying to delete the task"
        else:
            return redirect('/')
    else:


        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
