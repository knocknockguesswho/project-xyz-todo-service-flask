from flask import Flask
from flask_cors import CORS
from app.controllers.delete_controller import DeleteController
from app.controllers.get_controller import GetController
from app.controllers.post_controller import PostController
from app.controllers.update_controller import UpdateController

app = Flask(__name__)
# TODO: need to update cors when publishing
CORS(app, origins='*')


get_controller = GetController()
post_controller = PostController()
update_controller = UpdateController()
delete_controller = DeleteController()

# region GET METHOD
@app.route('/')
def get_todo():
    return get_controller.get_todo()

@app.route('/get-by-id/<int:id>')
def get_by_id(id: int):
  return get_controller.get_by_id(id=id)

@app.route('/get-by-created-at')
def get_by_created_at():
  return get_controller.get_by_created_at()

@app.route('/get-all-by-user-id/<int:user_id>')
def get_all_by_user_id(user_id: int):
  return get_controller.get_all_by_user_id(user_id=user_id)

@app.route('/get-done-by-user-id/<int:user_id>')
def get_done_by_user_id(user_id: int):
  return get_controller.get_done_by_user_id(user_id=user_id)

@app.route('/get-count-from-user-id/<int:user_id>')
def get_count_from_user_id(user_id: int):
  return get_controller.get_count_from_user_id(user_id=user_id)
# endregion GET METHOD


# region POST METHOD
@app.route('/add', methods=['POST'])
def add_todo():
  return post_controller.add_todo() 
# endregion POST METHOD


# region PUT METHOD
@app.route('/update-todo-name-one/<int:id>', methods=['PUT'])
def update_todo_name_by_id(id: int):
  return update_controller.update_todo_name_by_id(id=id)

@app.route('/set-done-one/<int:id>', methods=['PUT'])
def set_done_by_id(id: int):
  return update_controller.set_done_by_id(id=id)
# endregion PUT METHOD


# region DELETE METHOD
@app.route('/delete-one/<int:id>', methods=['DELETE'])
def delete_one_by_id(id: int):
  return delete_controller.delete_one_by_id(id=id)

@app.route('/delete-all', methods=['DELETE'])
def delete_all_todo():
  return delete_controller.delete_all_todo()
# endregion DELETE METHOD
