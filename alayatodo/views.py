from alayatodo import app, database
from alayatodo.models.models import *
from flask import (
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    session
    )


@app.route('/')
def home():
    with app.open_resource('../README.md', mode='r') as f:
        readme = f.read()
        return render_template('index.html', readme=readme)


@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_POST():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(username=username).first()
    if not user or not user.does_password_match(password):
        flash("Invalid user name or password")
        return redirect('/login')

    session['user'] = user.serialize()
    session['logged_in'] = True
    return redirect('/todo')



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todos.query.filter_by(id=id, user_id=session['user']['id']).first()
    if not todo:
        return make_response(dict(status="Not found", code="404", message="This todo item could not be found or you are not authorized to view it"), 404)
    return render_template('todo.html', todo=todo)

@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    if not session.get('logged_in'):
        return redirect('/login')
    todo = Todos.query.filter_by(id=id, user_id=session['user']['id']).first()
    if not todo:
        return make_response(dict(status="Not found", code="404", message="This todo item could not be found or you are not authorized to view it"), 404)
    return jsonify(todo.serialize())

@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    todos = Todos.query.filter_by(user_id=session['user']['id']).all()
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    description = request.form.get('description', '')
    if not description:
        return make_response("You must enter a description", 400)
    todo = Todos(user_id=session['user']['id'], description=description)
    database.session.add(todo)
    database.session.commit()
    flash('You have just added a todo!')
    return redirect('/todo')

@app.route('/todo/<id>/complete', methods=['POST'])
def todo_complete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    complete = 1 - int(request.form.get('complete', 1))
    database.session.query(Todos).filter_by(id=id, user_id=session['user']['id']).update({"complete":complete})
    database.session.commit()
    return redirect('/todo')

@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    database.session.query(Todos).filter_by(id=id, user_id=session['user']['id']).delete()
    database.session.commit()
    flash('You have just deleted a todo!')
    return redirect('/todo')
