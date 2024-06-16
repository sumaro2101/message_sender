from mail_center.celery import app

from .services import send_mails

@app.task
def send(user_email):
    
    return send_mails(user_email)
