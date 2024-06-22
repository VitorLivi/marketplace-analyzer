import sys
import os

sys.path.append(os.path.abspath('./'))

from database import Database
from face_recognizer import FaceRecognizer
from uuid import UUID
from datetime import datetime

db = Database().get_database()
now = datetime.now()

month_client = []
unique_image_paths = []

day_client_collection = db.get_collection('day_client')
month_client_collection = db.get_collection('month_client')

today = now.strftime("%d-%m-%Y")
month = now.strftime("%m-%Y")

def get_unique_image_paths():
    global unique_image_paths, month

    if os.path.exists(f'./images/{month}'):
        all_image_day_folders = os.listdir(f'./images/{month}')

        for day in all_image_day_folders:
            day_image_paths = os.listdir(f'./images/{month}/{day}')

            for image_path in day_image_paths:
                unique_image_paths.append(f'./images/{month}/{day}/{image_path}')


def compare_images(image_path, image_path2):
    current_image_to_compare = FaceRecognizer.find_face_encodings(image_path)

    image_to_compare = FaceRecognizer.find_face_encodings(image_path2)
    return FaceRecognizer.is_images_similar(current_image_to_compare, image_to_compare)

def compare_month_images ():
    global unique_image_paths, month_client

    has_similar_images = True
    while has_similar_images:
        is_some_image_similar = False

        unique_image_paths = []
        get_unique_image_paths()

        if unique_image_paths is None or len(unique_image_paths) <= 1:
            print("Insufficient images to compare")
            return

        current_client_id = unique_image_paths[0].split('/')[4].split('.')[0]

        print("CURRENT CLIENT ID -------------->", current_client_id)

        current_day_client = day_client_collection.find_one({
            "_id": UUID(current_client_id)
        })

        if (current_day_client is None):
            print(f"Client {current_client_id} not find in the database")
            return

        last_entry_date_time = current_day_client["entry_date_time"]
        first_entry_date_time = current_day_client["entry_date_time"]
        total_time_spent = current_day_client["time_spent_in_seconds"]
        all_tags = current_day_client["tags"]
        times_seen = 1

        for i in range(len(unique_image_paths) - 1):
            is_similar = compare_images(unique_image_paths[0], unique_image_paths[i + 1])
            if is_similar:
                is_some_image_similar = True
                compared_client_id = unique_image_paths[i + 1].split('/')[4].split('.')[0]

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
                        "month_client_id": UUID(current_client_id)
                    }
                })

                os.remove(unique_image_paths[i + 1])

        month_client = month_client_collection.find_one({
            "_id": UUID(current_client_id)
        })

        if month_client is None:
            db.get_collection('month_client').insert_one({
                "_id": UUID(current_client_id),
                "first_entry_date_time": first_entry_date_time,
                "last_entry_date_time": last_entry_date_time,
                "total_time_spent_in_seconds": total_time_spent,
                "tags": all_tags,
                "times_seen": times_seen,
            })
                
        has_similar_images = is_some_image_similar

compare_month_images()
