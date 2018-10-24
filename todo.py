from flask import Flask, render_template, redirect, url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////DATABASE-PATH'
db = SQLAlchemy(app)

# Database Table for Todo List
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean)

# Main Page
@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos = todos)

# Adding to ToDo List an Item
@app.route("/add/", methods = ["POST"])
def add():
    title = request.form.get("title")
    addTodo = Todo(title = title, complete = False)
    db.session.add(addTodo)
    db.session.commit()
    return redirect(url_for("index"))

# Complete an Item on the list
@app.route("/complete/<string:id>")
def complete(id):
    todoId = Todo.query.filter_by(id = id).first()
    todoId.complete = not todoId.complete
    db.session.commit()
    return redirect(url_for("index"))

# Delete an Item
@app.route("/delete/<string:id>")
def delete(id):
    todoId = Todo.query.filter_by(id = id).first()
    db.session.delete(todoId)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    db.create_all()      # Create/Read database before running the app
    app.run(debug = True)
