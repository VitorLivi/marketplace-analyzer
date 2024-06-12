import sys
import os

sys.path.append(os.path.abspath('./'))

from database import Database
from utils.datetime_utils import DateTimeUtils
from face_recognizer import FaceRecognizer
from uuid import UUID
from datetime import datetime

db = Database().get_database()
today = datetime.now()

week_client = []
unique_image_paths = []

day_client_collection = db.get_collection('day_client')
week_client_collection = db.get_collection('week_client')


today = day.strftime("%d-%m-%Y")
month = today.strftime("%m-%Y")

def get_existent_week_folders(daysOfWeekRange):
    global today, month
    existent_week_paths = []

    for day in daysOfWeekRange:
        if os.path.exists(f'./images/{month}/{today}'):
            existent_week_paths.append(today)

    return existent_week_paths

def get_unique_image_paths(existent_week_folders):
    global unique_image_paths, month

    for day in existent_week_folders:
        all_image_name = os.listdir(f'./images/{month}/{day}')

        for image_name in all_image_name:
            unique_image_paths.append('./images/{month}/{day}/' + image_name)

def compare_images(image_path, image_path2):
    current_image_to_compare = FaceRecognizer.find_face_encodings(image_path)

    image_to_compare = FaceRecognizer.find_face_encodings(image_path2)
    return FaceRecognizer.is_images_similar(current_image_to_compare, image_to_compare)

def compare_week_images (week_range):
    global unique_image_paths, week_client

    days_of_week_range = DateTimeUtils.getDaysOfWeekRange(week_range)
    existent_week_folders = get_existent_week_folders(days_of_week_range)

    has_similar_images = True
    while has_similar_images:
        is_some_image_similar = False

        unique_image_paths = []
        get_unique_image_paths(existent_week_folders)

        if unique_image_paths is None or len(unique_image_paths) <= 1:
            print("Insufficient images to compare")
            return

        current_client_id = unique_image_paths[0].split('/')[3].split('.')[0]
        current_day_client = day_client_collection.find_one({
            "_id": UUID(current_client_id)
        })

        last_entry_date_time = current_day_client["entry_date_time"]
        first_entry_date_time = current_day_client["entry_date_time"]
        total_time_spent = current_day_client["time_spent_in_seconds"]
        all_tags = current_day_client["tags"]
        times_seen = 1

        for i in range(len(unique_image_paths) - 1):
            is_similar = compare_images(unique_image_paths[0], unique_image_paths[i + 1])
            if is_similar:
                is_some_image_similar = True
                compared_client_id = unique_image_paths[i + 1].split('/')[3].split('.')[0]

                compared_day_client = day_client_collection.find_one({
                    "_id": UUID(compared_client_id)
                })

                total_time_spent += compared_day_client["time_spent_in_seconds"]
                all_tags.extend(compared_day_client["tags"])
                times_seen += 1

                formated_compared_client_entry_date_time = datetime.strptime(compared_day_client["entry_date_time"], '%d-%m-%Y %H:%M:%S')
                formated_first_entry_date_time = datetime.strptime(first_entry_date_time, '%d-%m-%Y %H:%M:%S')
                formated_last_entry_date_time = datetime.strptime(last_entry_date_time, '%d-%m-%Y %H:%M:%S')

                if formated_compared_client_entry_date_time < formated_first_entry_date_time:
                    first_entry_date_time = compared_day_client["entry_date_time"]

                if formated_compared_client_entry_date_time > formated_last_entry_date_time:
                    last_entry_date_time = compared_day_client["entry_date_time"]

                day_client_collection.update_many({
                    "_id": {"$in": [UUID(current_client_id), UUID(compared_client_id)]}
                }, {
                    "$set": {
                        "week_client_id": UUID(current_client_id)
                    }
                })

                os.remove(unique_image_paths[i + 1])

        week_client = week_client_collection.find_one({
            "_id": UUID(current_client_id)
        })

        if week_client is None:
            db.get_collection('week_client').insert_one({
                "_id": UUID(current_client_id),
                "first_entry_date_time": first_entry_date_time,
                "last_entry_date_time": last_entry_date_time,
                "total_time_spent_in_seconds": total_time_spent,
                "tags": all_tags,
                "times_seen": times_seen,
            })
                
        has_similar_images = is_some_image_similar

currentWeekRange = DateTimeUtils.getCurrentWeekRange()

print(f"WEEK RANGE --> {currentWeekRange[0].strftime('%d-%m-%Y')} - {currentWeekRange[1].strftime('%d-%m-%Y')}")
compare_week_images(currentWeekRange)
