from celery import shared_task
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import requests
import time

import os
import logging
from bono_bar.env import BASE_DIR, env

logger = logging.getLogger(__name__)

env_path = os.path.join(BASE_DIR, '.env')

# FILE_URL = 'http://web:8000/api/book/download-booking/' 
FILE_URL = 'https://backend.bono-bar.com/api/book/download-booking/' 
FILE_PATH = 'filtered_bookings.csv'
 



@shared_task
def send_report_booking():
    try:
        response = requests.get(FILE_URL)
        time.sleep(3)
        with open(FILE_PATH, 'wb') as f:
            f.write(response.content)
        
        if response.status_code != 200:
            print(f'Ошибка при загрузке файла. Статус ответа: {response.status_code}')
        else:
            print('Файл успешно загружен.')

    except requests.exceptions.RequestException as e:
        print(f'Ошибка при загрузке файла: {e}')
        try:
            with open(FILE_PATH, 'wb') as f:
                f.write(e.response.content)
            print('Файл загружен с ошибкой.')

        except AttributeError:
            print('Файл не может быть загружен, нет содержимого ответа.')

    subject = 'Report'
    message = 'report booking: \n'
    sender_email = env('EMAIL_HOST_USER')
    recipient_email = env('EMAIL_HOST_USER')
    email = EmailMessage(subject, message, sender_email, [recipient_email])

    try:
        with open(FILE_PATH, 'rb') as f:
            email.attach('filtered_bookings.csv', f.read(), 'text/csv')
        
        # Отправляем письмо
        email.send()
    except FileNotFoundError:
        print(f'File {FILE_PATH} not found.')
    except Exception as e:
        print(f'An error occurred: {e}')



@shared_task
def my_task(stri):
    
    return stri