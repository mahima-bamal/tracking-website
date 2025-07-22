import sqlite3
from datetime import datetime,timedelta
from app import summarize_competitors,send_mail

def send_auto_email():
    result=None
    with sqlite3.connect("users.db",check_same_thread=False) as conn:
        cursor=conn.cursor()
        cursor.execute("SELECT username,summary_date FROM users WHERE summary_date IS NOT NULL")
        result=cursor.fetchall()
        print(result)
        for i in range(len(result)):
            username=result[i][0]
            summary_datetime = datetime.fromisoformat(result[i][1].replace('Z', '+00:00'))
            check_time_thresshold=48
            current_time = datetime.now(summary_datetime.tzinfo)
            time_difference = current_time - summary_datetime
            hours_difference = time_difference.total_seconds() / 3600
            if hours_difference <= check_time_thresshold:
                mess=summarize_competitors(username)
                send_mail(username,mess)
    return None
