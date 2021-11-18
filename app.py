from flask import Flask, request, render_template, redirect
from flask_restful import Api, Resource, abort

import logging

from models import Todo, db
# logging.basicConfig(filename='F:/flasha/Lab5', level=logging.DEBUG,
#                     format=" %(asctime)s %(message)s %(levelname)s")
todo_flask_app = Flask(__name__)

todo_api = Api(todo_flask_app)

todo_flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
todo_flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class TodoLC(Resource):
    def get(self):
        try:
            todo_objects = Todo.query.filter().all()

            new_list = []
            for task in todo_objects:
                data = {
                    'id': task.id,
                    'name': task.name,
                    'priority': task.priority
                }
                new_list.append(data)
                print(data)
            return new_list
        except Exception as e:
            abort(500, message="Internal Server Error {}".format(e))

    def post(self):
        try:
            data = {
                'name': request.form.get('name'),
                'priority': request.form.get('priority'),
            }
            todo_obj = Todo(**data)
            db.session.add(todo_obj)
            db.session.commit()
            return {'message': 'Task Created Successfully'}, 201
        except Exception as e:
            abort(500, message='Internal Server Error')


class TodoRUD(Resource):
    def get(self, **kwargs):
        todo_id = kwargs.get('todo_id')
        task = Todo.query.get(todo_id)
        if not task:
            abort(404, message='Not Found')
        data = {
            'id': task.id,
            'name': task.name,
            'priority': task.priority,
        }

        return data, 200

    def delete(self, **kwargs):
        todo_id = kwargs.get('todo_id')
        task = Todo.query.get(todo_id)
        if not task:
            abort(404, message='Not Found')
        db.session.delete(task)
        db.session.commit()
        return{'message': 'Deleted Successfully'}, 200

    def patch(self, **kwargs):
        todo_id = kwargs.get('todo_id')
        task = Todo.query.get(todo_id)
        if request.form.get('name'):
            task.name = request.form.get('name')
        if request.form.get('priority'):
            task.priority = request.form.get('priority')
        db.session.commit()
        data = {
            'name': task.name,
            'priority': task.priority,
        }

        return data, 200


todo_api.add_resource(TodoLC, '/api/todo')
todo_api.add_resource(TodoRUD, '/api/todo/<int:todo_id>')


db.init_app(todo_flask_app)


@todo_flask_app.before_first_request
def initiate_db():
    db.create_all()


todo_flask_app.run(port=5000, debug=True)
