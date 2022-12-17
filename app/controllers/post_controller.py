from app.config.schema import Session, Todos
from app.helpers.response_helper import ResponseHelper
from flask import request

class PostController:
  def __init__(self): pass
  
  def add_todo(self, **params):
    """
    Request Form
      `user_id`: int @required
      `todo_name`: str @required
      `parent_id`: int or empty str @required

    set `parent_id` to integer,
    need to assign with `digit str` value or `empty str` if no parent
    """
    response_helper = ResponseHelper()
    with Session() as session:
      try:
        user_id = request.form['user_id']
        todo_name = request.form['todo_name']
        parent_id = request.form['parent_id']
        if len(parent_id) > 0:
          if parent_id.isdigit(): parent_id = int(parent_id)
          else: raise Exception('parent_id must be integer or empty string')
        else: parent_id = None
        session.add(Todos(user_id=user_id, todo_name=todo_name, parent_id=parent_id, done=None))
        session.commit()
        response_helper.remove_datas()
      except Exception as e:
        if e.__cause__ is not None: response_helper.set_to_failed(str(e.__cause__), 400)
        else: response_helper.set_to_failed(str(e), 400)
      finally:
        return response_helper.get_response()