import csv
import io
import os
import environ
from pathlib import Path

from core.models import SystemQuide, Student
import inspect

#############################################
#####  Import User from request
#############################################
def get_user_from_request():
    request = [
        frame_record[0].f_locals["request"]
        for frame_record in inspect.stack()
        if frame_record[3] == "get_response"
    ][0]
    return request.user

def students_import_from_csv(csv_file):
    env = environ.Env()
    BASE_DIR = Path(__file__).resolve().parent.parent
    environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
    new_password = env('FEED_IMPORT_USER_PASSWORD')
    new_users = 0
    updated_users = 0
    new_group = SystemQuide.objects.get(pk=1).feed_group_id
    reader = csv.DictReader(io.StringIO(csv_file.read().decode('utf-8')))

    for line in reader:
        if not Student.objects.filter(email=line['email']).exists():
            username = 'feed' + line['email']
            new_student = Student.objects.create(username=username, email=line['email'],
                                                 first_name=line['first_name'], last_name=line['first_name'],
                                                 patronymic=line['patronymic'], )
            new_student.set_password(new_password)
            new_student.active_group_id = new_group
            new_student.save()
            new_users += 1
        else:
            new_student = Student.objects.get(email=line['email'], )
            if not new_group in new_student.all_group_id.all():
                new_student.all_group_id.add(new_group)
                updated_users += 1
    result_string = str(new_users) + ' добавлено новых студентов. '
    result_string += str(updated_users) + ' обновлено студентов.'

    return result_string


async def asyncio_send_mail(message_text, email):
    from email.message import EmailMessage
    import aiosmtplib
    message = EmailMessage()
    message["From"] = "hamstertest197@yandex.ru"
    message["To"] = email
    message["Subject"] = "portal message"
    message.set_content(message_text)
    from app.settings import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
    try:
        await aiosmtplib.send(
            message,
            hostname=EMAIL_HOST,
            username=EMAIL_HOST_USER,
            password=EMAIL_HOST_PASSWORD
        )
    except aiosmtplib.errors.SMTPException:
        print(1)
        pass


