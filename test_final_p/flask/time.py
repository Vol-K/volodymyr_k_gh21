import sqlite3 # замість cs50
from datetime import datetime, time, date

## А так на реальному сервері - https://www.pythonanywhere.com/
dbb = sqlite3.connect('D:\\VS_Code\\project_Club\\venv\\datbase\\club.db', check_same_thread=False)
db = dbb.cursor()

# тур
round = 11
# конкретний матч
match_id = 137

# матчі певного тура
all_matches_in_tur = db.execute ("SELECT * FROM m3 WHERE match_id = :match_id ORDER BY round DESC, mtch_round DESC",\
						   dict(match_id=match_id))
all_matches_in_tur = all_matches_in_tur.fetchall()

match_day = all_matches_in_tur[0][6]
match_time = all_matches_in_tur[0][7]

# допоміжні дані (для об'єднання дня та часу матчу в одне поле)
space = ' '
pre_match_day_time = match_day + "{}" + match_time
match_day_time = pre_match_day_time.format(space)


# переганяємо у формат 'datetime.datetime' для порівняння з актуальним часом прогноза чи зміни прогноза
#match_day_time = datetime.strptime(match_day_time, '%Y-%m-%d %H:%M')
#match_day_time = datetime.timestamp(match_day_time)
match_day_time = datetime.timestamp(datetime.strptime(match_day_time, '%Y-%m-%d %H:%M'))

# перевірка актуального часу (без мілісекунд)
date_and_time_now = datetime.now()
print("1 datetime.now - ", date_and_time_now)
print(type(date_and_time_now))

date_and_time_now = datetime.strftime(date_and_time_now, "%Y-%m-%d %H:%M")
print("2 datetime.now - ", date_and_time_now)
print(type(date_and_time_now))

date_and_time_now = datetime.strptime(date_and_time_now, '%Y-%m-%d %H:%M')
print("3 datetime.now - ", date_and_time_now)
print(type(date_and_time_now))
date_and_time_now = datetime.timestamp(date_and_time_now)
# date_and_time_now = date_and_time_now.replace(second=0, microsecond=0)
print("4 datetime.now - ", date_and_time_now)
print("date_and_time_now - ", date_and_time_now)

# коригуємо часовий пояс сервера (додаємо +2 години)
timestamp = date_and_time_now
timestamp = timestamp + 7200                        ###60 сек * 60 хв * 2 години
print("timestamp - ", timestamp)
print(type(timestamp))

# порівнюємо час початку матча і час запила прогноза (чи його зміни)
delta = match_day_time - timestamp
#delta = datetime.fromtimestamp(delta).strftime('%H:%M')
print("delta - ", delta)
if delta < 0:
	print("huynya")

