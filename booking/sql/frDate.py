from datetime import datetime, timedelta

with open('rezervacije.sql', 'r', encoding='utf-8') as file:
  content = file.read()
  if (datetime.now()+timedelta(days=7)).weekday() == 2:
    content = f"{content} insert into booking_bookings (organizer_name, purpose, napomena, room_id, user_id, start_time, end_time) VALUES ('Engleski', 'kurs', 'skoro svake srede', 2, 2, 'DATE 14:30:00', 'DATE 16:00:00');"
  dofw =  (datetime.now()+timedelta(days=7)).weekday()
  if dofw in [0, 2, 4]:
    content = f"{content} insert into booking_bookings (organizer_name, purpose, napomena, room_id, user_id, start_time, end_time) VALUES ('radiologija', 'rezervisano', 'ponedeljakom, sredom i petkom', 1, 2, 'DATE 09:00:00', 'DATE 09:45:00' );"
  datum = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
  content = content.replace('DATE', datum)
  
with open('tmp.sql', 'w', encoding='utf-8') as file:  
  file.write(content)
