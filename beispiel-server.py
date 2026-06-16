
"""
Example script showing how to represent todo lists and todo entries in Python
data structures and how to implement endpoint for a REST API with Flask.

Requirements:
* flask
"""

import uuid 

from flask import Flask, request, jsonify, abort, render_template, redirect


# initialize Flask server
app = Flask(__name__)

# define internal data structures with example data
todo_lists = [
]
todos = [
]

# add some headers to allow cross origin access to the API on this server, necessary for using preview in Swagger Editor!
@app.after_request
def apply_cors_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE, PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.route('/', methods=['GET', 'POST']) 
def index(): 
    if request.method == 'POST': 
        name = request.form.get('name') 
    if name: 
        todo_lists.append({ 'id': str(uuid.uuid4()), 'name': name }) 
        return redirect('/') 
    return render_template('index.html', todo_lists=todo_lists)

@app.route('/todo-list', methods=['GET', 'POST'])
def handle_CreateList():
    if request.method == 'GET':
        return jsonify(todo_lists), 200
    if request.method == 'POST':
        if 'name' not in request.args:
            return '', 400
        list_name = request.args['name']
        new_list = {'id': str(uuid.uuid4()), 'name': list_name}
        todo_lists.append(new_list)
        return '', 201

# define endpoint for getting and deleting existing todo lists
@app.route('/todo-list/<list_id>', methods=['GET', 'DELETE', 'POST'])
def handle_list(list_id):
    # find todo list depending on given list id
    list_item = None
    for l in todo_lists:
        if l['id'] == list_id:
            list_item = l
            break
    # if the given list id is invalid, return status code 404
    if not list_item:
        abort(404)
    if request.method == 'GET':
        # find all todo entries for the todo list with the given id
        return jsonify([i for i in todos if i['list'] == list_id])
    elif request.method == 'DELETE':
        # delete list with given id
        todo_lists.remove(list_item)
        for todo in todos[:]:
            if(todo['list'] == list_item['id']):
                todos.remove(todo)
        return '', 204
    elif request.method == 'POST':
        if 'name' not in request.args or 'description' not in request.args:
            return '', 400
        new_todo = {'id': str(uuid.uuid4()), 'name': request.args['name'], 'description': request.args['description'], 'list': list_id}
        todos.append(new_todo)
        return jsonify(new_todo), 201

@app.route('/todo-list/entry/<entry_id>', methods=['PATCH', 'DELETE'])
def handle_entry(entry_id):
    entry_item = None
    for l in todos:
        if l['id'] == entry_id:
            entry_item = l
            break
    if not entry_item:
        abort(404)
    if request.method == 'PATCH':
        for todo in todos:
            if(todo == entry_item):
                todo['name'] = request.args['name']
                todo['description'] = request.args['description']
                return '', 200
    if request.method == 'DELETE':
        for todo in todos:
            if(todo == entry_item):
                todos.remove(todo)
                return '', 204
            

if __name__ == '__main__':
    # start Flask server
    app.run(host='0.0.0.0', port=5000)
