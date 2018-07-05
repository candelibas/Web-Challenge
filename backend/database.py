import sqlite3
import datetime

dbconn = sqlite3.connect('data/database.db', check_same_thread=False)
db = dbconn.cursor()

def create_table():
  db.execute("CREATE TABLE IF NOT EXISTS udemyReviews(rev_avg REAL, rev_course_title TEXT, rev_datestamp TEXT, rev_time TEXT)")

def save_review_daily(rev_avg, rev_course_title, rev_datestamp, rev_time): # rev_avg, rev_course_title, rev_datestamp, rev_course_id
  create_table()
  
  db.execute("INSERT INTO udemyReviews (rev_avg, rev_course_title, rev_datestamp, rev_time) VALUES(?, ?, ?, ?)", 
              (rev_avg, rev_course_title, rev_datestamp, rev_time))
  dbconn.commit()

def read_reviews_daily():
  todayDate = datetime.datetime.today().strftime('%d.%m.%Y')
  db.execute("SELECT * FROM udemyReviews WHERE rev_datestamp = ?", [todayDate])
  rows = db.fetchall()
  
  return rows

#save_review_daily(4.36, "Java programming")