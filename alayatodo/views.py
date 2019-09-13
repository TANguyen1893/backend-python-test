from alayatodo import app
from flask import (
    g,
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

    sql = "SELECT * FROM users WHERE username = '%s' AND password = '%s';"
    cur = g.db.execute(sql % (username, password))
    user = cur.fetchone()
    if user:
        session['user'] = dict(user)
        session['logged_in'] = True
        return redirect('/todo')

    return redirect('/login')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user', None)
    return redirect('/')


@app.route('/todo/<id>', methods=['GET'])
def todo(id):
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s';" % id)
    todo = cur.fetchone()
    return render_template('todo.html', todo=todo)

@app.route('/todo/<id>/json', methods=['GET'])
def todo_json(id):
    if not session.get('logged_in'):
        return redirect('/login')
    cur = g.db.execute("SELECT * FROM todos WHERE id ='%s' AND user_id=%d;" % (id, int(session['user']['id'])))
    todo = cur.fetchone()
    print(todo)
    if not todo:
        return make_response(dict(status="Not found", code="404", message="This todo item could not be found or you are not authorized to view it"), 404)
    return jsonify(dict(todo))

@app.route('/todo', methods=['GET'])
@app.route('/todo/', methods=['GET'])
def todos():
    if not session.get('logged_in'):
        return redirect('/login')
    cur = g.db.execute("SELECT * FROM todos;")
    todos = cur.fetchall()
    return render_template('todos.html', todos=todos)


@app.route('/todo', methods=['POST'])
@app.route('/todo/', methods=['POST'])
def todos_POST():
    if not session.get('logged_in'):
        return redirect('/login')
    description = request.form.get('description', '')
    if not description:
        return make_response("You must enter a description", 400)
    g.db.execute(
        "INSERT INTO todos (user_id, description) VALUES ('%s', '%s');"
        % (session['user']['id'], description)
    )
    g.db.commit()
    return redirect('/todo')

@app.route('/todo/<id>/complete', methods=['POST'])
def todo_complete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    complete = 1 - int(request.form.get('complete', 1))
    g.db.execute(
        "UPDATE todos SET complete = %d WHERE user_id = %d and id = %d;"
        % (int(complete), int(session['user']['id']), int(id))
    )
    g.db.commit()
    return redirect('/todo')

@app.route('/todo/<id>', methods=['POST'])
def todo_delete(id):
    if not session.get('logged_in'):
        return redirect('/login')
    g.db.execute("DELETE FROM todos WHERE id ='%s';" % id)
    g.db.commit()
    return redirect('/todo')
