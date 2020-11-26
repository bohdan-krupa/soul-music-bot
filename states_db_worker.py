from vedis import Vedis
from config import StatesList, STATES_DB_NAME

class States:
  @staticmethod
  def get_state(user_id):
    with Vedis(STATES_DB_NAME) as db:
      try:
        return db[user_id].decode()
      except Exception as e:
        print(e)
        return StatesList.START.value

  @staticmethod
  def set_state(user_id, value):
    with Vedis(STATES_DB_NAME) as db:
      try:
        db[user_id] = value
        return True
      except Exception as e:
        print(e)
        return False