from datetime import datetime, timedelta
import sqlite3
#import os


def main():
  # Change the current working directory to the root directory of your project
  #os.chdir(os.path.dirname(os.getcwd()))

  # sql statement for add English kurs on Wednesday
  sql_01 = "insert into booking_bookings (organizer_name, purpose, napomena, room_id, user_id, start_time, end_time) VALUES ('Engleski', 'kurs', 'skoro svake srede', 2, 2, 'DATE 14:30:00', 'DATE 16:00:00');"
  # sql statement for add rezervacije on Monday, Wednesday and Friday
  sql_02 = "insert into booking_bookings (organizer_name, purpose, napomena, room_id, user_id, start_time, end_time) VALUES ('radiologija', 'rezervisano', 'ponedeljakom, sredom i petkom', 1, 2, 'DATE 09:00:00', 'DATE 09:45:00' );"
  
  with open('svakog_radnog_dana.sql', 'r', encoding='utf-8') as file:
    content = file.read()
  dofw =  (datetime.now()+timedelta(days=7)).weekday()
  
  if dofw == 2:
    content = f"{content} {sql_01}"
  
  if dofw in [0, 2, 4]:
    content = f"{content} {sql_02}"
    
    datum = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    content = content.replace('DATE', datum)
    
  with open('tmp.sql', 'w', encoding='utf-8') as file:  
    file.write(content)

  sqlCommands = content.split(';')

  try:  
    connection = sqlite3.connect('../db.sqlite3')
    cur = connection.cursor()
    
    # delete old records
    yesterday = datetime.now() - timedelta(days=1)
    cur.execute("DELETE FROM booking_bookings WHERE start_time < ?", (yesterday,))
    
    # adding records for next week
    for sqlComand in sqlCommands:
      cur.execute(sqlComand)
    connection.commit()
    print("Records created successfully")
  except Exception as e:
      print(e)
  finally:
    if connection:
      connection.close()
      print("Database connection is closed")

if __name__ == '__main__':
  main()
