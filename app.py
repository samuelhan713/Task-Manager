from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'   #this tells us where the database is located
db = SQLAlchemy(app) #initializing the database

class Todo(db.Model): #creating the model for the database
    id = db.Column(db.Integer, primary_key = True) #columns
    content = db.Column(db.String(200), nullable = False) #limits the user from creating a task and leaving the content empty
    date_created = db.Column(db.DateTime, default = datetime.utcnow) #gets the date created

    def __repr__(self):
        return '<Task %r>' % self.id



@app.route('/', methods=['POST', 'GET']) #adding two methods this route can accept (regarding the database)
def index():
    if request.method == 'POST': #if the request is 'post' (when the button is clicked)
        task_content = request.form['content'] #task_content will contain the input value
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task) #adds a new task to the list
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'  #catching errors
    else:
        tasks = Todo.query.order_by(Todo.date_created).all() #you can change all to first to get the most recent one
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    tasks_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(tasks_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'    

@app.route('/update/<int:id>', methods = ['Get', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST': 
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an error updating your task"

    else:
        return render_template('update.html', task=task) 



if __name__ == '__main__':
    app.run(debug = True)