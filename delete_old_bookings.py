import sqlite3
from datetime import datetime, timedelta 

def deleteRecords():
  try:
    connection = sqlite3.connect('db.sqlite3')
    cur = connection.cursor()
    yesterday = datetime.now() - timedelta(days=1)
    cur.execute("DELETE FROM booking_bookings WHERE start_time < ?", (yesterday,))
    connection.commit()
    print("Old records deleted successfully")
    connection.close()
  except Exception as e:
    print(e)
  finally:
    if connection:
      connection.close()
      print("Database connection is closed")

deleteRecords()
