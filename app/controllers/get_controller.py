from app.config.schema import Session, Todos
from app.helpers.response_helper import ResponseHelper
from flask import request
from sqlalchemy.orm import Query
from sqlalchemy.exc import NoResultFound

from utils import default_or_int

_ERROR_DATA_WITH_ID_NOT_FOUND_ = 'cannot find todo with id '
_ERROR_DATA_WITH_USER_ID_NOT_FOUND_ = 'cannot find todo with user_id '
_ERROR_DONE_WITH_USER_ID_NOT_FOUND_ = 'cannot find done todo with user_id '
_ERROR_CREATED_AT_NOT_FOUND_ = 'cannot find created_at '

class GetController:
  def __init__(self): pass
  
  def get_todo(self, **params):
    """
    Request Query Params
      `limit`: digit string @optional - `?limit=10` (default is 10) - `per_page`
      `last_id`: digit string @optional - `?last_id=0` (default is 0)
    """
    response_helper = ResponseHelper()
    limit = default_or_int(10, request.args.get('limit'))
    last_id = default_or_int(0, request.args.get('last_id'))
    with Session() as session:
      try:
        query = Query(Todos, session).filter(Todos.id > last_id)
        response_helper.set_data([data.get_item() for data in query.limit(limit).all()])
      except Exception as e:
        response_helper.set_to_failed(str(e),400)
      finally:
        return response_helper.get_response()

  def get_by_id(self, **params):
    """
    Request Args
      `id`: int @required

    return
    - will return data match with `id` as object or dictionary
    - will return status of 404 if no data match with `id`
    """
    response_helper = ResponseHelper()
    id = params['id']
    with Session() as session:
      try:
        query = Query(Todos, session).filter(Todos.id == id)
        response_helper.set_data(query.one().get_item())
      except Exception as e:
        status_code = 400
        msg = str(e)
        if type(e) == NoResultFound:
          status_code = 404
          msg = f'{_ERROR_DATA_WITH_ID_NOT_FOUND_}{id}'
        response_helper.set_to_failed(msg,status_code)
      finally:
        return response_helper.get_response()

  def get_by_created_at(self, **params):
    """
    Request Query Params
      `limit`: digit string @optional - `?limit=10` (default is 10)
      `last_id`: digit string @optional - `?last_id=0` (default is 0)

    Request Form
      `date_start`: date string @required `YYYY-mm-dd`
      `date_end`: date string @required `YYYY-mm-dd`

    return
      - if `date_start` is not set, would set to default as 1900-01-01
      - if `date_end` is not set, would set to default as 2100-12-31
      - if `total_item` is not set, would return all of data match to date
    """
    response_helper = ResponseHelper()
    limit = default_or_int(10, request.args.get('limit'))
    last_id = default_or_int(0, request.args.get('last_id'))
    with Session() as session:
      try:
        date_start = request.form['date_start']
        date_end = request.form['date_end']
        query = Query(Todos, session).filter(Todos.id > last_id, Todos.created_at.between(date_start, date_end))
        data = [data.get_item() for data in query.limit(limit).all()]
        if len(data) == 0: raise NoResultFound
        response_helper.set_data(data)
      except Exception as e:
        status_code = 400
        msg = str(e)
        if type(e) == NoResultFound:
          status_code = 404
          msg = f'{_ERROR_CREATED_AT_NOT_FOUND_}from {date_start} to {date_end}'
        response_helper.set_to_failed(msg,status_code)
      finally:
        return response_helper.get_response()

  def get_all_by_user_id(self, **params):
    """
    Request Query Params
      `limit`: digit string @optional - `?limit=10` (default is 10)
      `last_id`: digit string @optional - `?last_id=0` (default is 0)

    Request Args
      `user_id`: int @required

    return
    - will return data match with `id` as object or dictionary
    - will return status of 404 if no data match with `id`
    """
    response_helper = ResponseHelper()
    limit = default_or_int(10, request.args.get('limit'))
    last_id = default_or_int(0, request.args.get('last_id'))
    user_id = params['user_id']
    with Session() as session:
      try:
        query = Query(Todos, session).filter(Todos.id > last_id, Todos.user_id == user_id)
        data = [data.get_item() for data in query.limit(limit).all()]
        if len(data) == 0: raise NoResultFound
        response_helper.set_data(data)
      except Exception as e:
        status_code = 400
        msg = str(e)
        if type(e) == NoResultFound:
          status_code = 404
          msg = f'{_ERROR_DATA_WITH_USER_ID_NOT_FOUND_}{user_id}'
        response_helper.set_to_failed(msg,status_code)
      finally:
        return response_helper.get_response()

  def get_done_by_user_id(self, **params):
    """
    Request Query Params
      `limit`: digit string @optional - `?limit=10` (default is 10)
      `last_id`: digit string @optional - `?last_id=0` (default is 0)

    Request Args
      `user_id`: int @required
      
    return
    - will return data match with `id` as object or dictionary
    - will return status of 404 if no data match with `id`
    """
    response_helper = ResponseHelper()
    limit = default_or_int(10, request.args.get('limit'))
    last_id = default_or_int(0, request.args.get('last_id'))
    user_id = params['user_id']
    with Session() as session:
      try:
        query = Query(Todos, session).filter(Todos.user_id == user_id, Todos.id > last_id, Todos.done == 1)
        data = [data.get_item() for data in query.limit(limit).all()]
        if len(data) == 0: raise NoResultFound
        response_helper.set_data(data)
      except Exception as e:
        status_code = 400
        msg = str(e)
        if type(e) == NoResultFound:
          status_code = 404
          msg = f'{_ERROR_DONE_WITH_USER_ID_NOT_FOUND_}{user_id}'
        response_helper.set_to_failed(msg,status_code)
      finally:
        return response_helper.get_response()


  def get_count_from_user_id(self, **params):
    response_helper = ResponseHelper()
    user_id = params['user_id']
    with Session() as session:
      try:
        query = Query(Todos, session).filter(Todos.user_id == user_id)
        count = query.count()
        min_id = query.limit(1).one().id
        max_id = query.order_by(Todos.id.desc()).limit(1).one().id
        return response_helper.set_data({'min_id': min_id, 'count': count, 'max_id': max_id})
      except Exception as e:
        response_helper.set_to_failed(str(e),400)
      finally:
        return response_helper.get_response()