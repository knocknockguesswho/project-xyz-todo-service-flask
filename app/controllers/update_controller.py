from app.config.schema import Session, Todos
from app.helpers.response_helper import ResponseHelper
from flask import request
from sqlalchemy.orm import Query

class UpdateController:
  def __init__(self): pass

  def update_todo_name_by_id(self, **params):
    """
    Request Args
      `id`: int @required

    Request Form
      `todo_name`: str @required
    """
    response_helper = ResponseHelper()
    id = params['id']
    with Session() as session:
      try:
        todo_name = request.form['todo_name']
        Query(Todos, session).filter(Todos.id == id).update({Todos.todo_name: todo_name}, synchronize_session=False)
        response_helper.remove_datas()
      except Exception as e:
        response_helper.set_to_failed(str(e),400)
      finally:
        session.commit()
        return response_helper.get_response()

  def set_done_by_id(self, **params):
    """
    Request Args
      `id`: int @required
    """
    response_helper = ResponseHelper()
    id = params['id']
    with Session() as session:
      try:
        Query(Todos, session).filter(Todos.id == id).update({Todos.done: 1}, synchronize_session=False)
        response_helper.remove_datas()
      except Exception as e:
        response_helper.set_to_failed(str(e),400)
      finally:
        session.commit()
        return response_helper.get_response()