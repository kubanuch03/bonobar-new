from django.test import TestCase
import pandas as pd
import os



CACHE_TIME = 60*5
FILE_PATH = 'booking.csv'

#проверка  на запись к файлу
def write_booking_to_file(booking_data):
    new_data = pd.DataFrame([booking_data])

    if os.path.exists(FILE_PATH):
        existing_data = pd.read_csv(FILE_PATH)
        updated_data = pd.concat([existing_data, new_data], ignore_index=True)
    else:
        updated_data = new_data

    updated_data.to_csv(FILE_PATH, index=False)



test_booking_data = {
    'id': 1,
    'user_name': 'Test User',
    'start_time': '10:00',
    'end_time': '11:00',
    'will_come': '2024-07-01',
    'phone_number': '1234567890',
}

write_booking_to_file(test_booking_data)