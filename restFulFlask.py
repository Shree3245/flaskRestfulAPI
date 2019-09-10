from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
import requests
app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '?????'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(ticket_id):
    if todo_id not in TODOS:
        abort(404, message="Ticket {} doesn't exist".format(ticket_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, ticket_id):
        abort_if_todo_doesnt_exist(ticket_id)
        return TODOS[ticket_id]

    def delete(self, ticket_id):
        abort_if_todo_doesnt_exist(ticket_id)
        del TODOS[ticket_id]
        return '', 204

    def put(self, ticket_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[ticket_id] = task
        return task, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoAdd(Resource):
    
    def post(self):
        args = parser.parse_args()
        ticket_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        ticket_id = 'todo%i' % ticket_id
        TODOS[ticket_id] = {'task': args['task']}
        return TODOS[ticket_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<ticket_id>')


if __name__ == '__main__':
    app.run(debug=True)