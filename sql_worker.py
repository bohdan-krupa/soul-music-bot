import sqlite3

class SQL:
  def __init__(self, database):
    self.connection = sqlite3.connect(database)
    self.cursor = self.connection.cursor()


  def add_bit(self, bit_type, file_id):
    with self.connection:
      query = f'INSERT INTO bits (type, file_id) VALUES ("{bit_type}", "{file_id}")'
      return self.cursor.execute(query)

  def get_bits(self, bit_type):
    with self.connection:
      query = f'SELECT * FROM bits WHERE type = "{bit_type}"'
      return self.cursor.execute(query).fetchall()


  def close(self):
    self.connection.close()