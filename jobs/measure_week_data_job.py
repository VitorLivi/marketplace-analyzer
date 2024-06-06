import sys
from os import path

sys.path.append(path.abspath('./'))

from database import Database
from utils.datetime_utils import DateTimeUtils
from face_recognizer import FaceRecognizer
import datetime
import cv2
import os

db = Database().get_database()
today = datetime.datetime.now()

def get_existent_week_folders(daysOfWeekRange):
    existent_week_paths = []

    for day in daysOfWeekRange:
        if os.path.exists(f'./images/{day.strftime("%d-%m-%Y")}'):
            existent_week_paths.append(day.strftime("%d-%m-%Y"))

    return existent_week_paths

def get_unique_image_paths(existent_week_folders):
    for day in existent_week_folders:
        all_image_name = os.listdir(f'./images/{day}')

        print(f"ALL IMAGE NAMES --> {all_image_name}")

        for image_name in all_image_name:
            unique_image_paths.append('./images/' + day + '/' + image_name)

def compare_images(image_path, image_path2):
    current_image_to_compare = FaceRecognizer.find_face_encodings(image_path)

    image_to_compare = FaceRecognizer.find_face_encodings(image_path2)
    return FaceRecognizer.is_images_similar(current_image_to_compare, image_to_compare)

def compare_week_images (week_range):
    days_of_week_range = DateTimeUtils.getDaysOfWeekRange(week_range)
    existent_week_folders = get_existent_week_folders(days_of_week_range)

    has_similar_images = True
    while has_similar_images:
        is_some_image_similar = False
        unique_image_paths = get_unique_image_paths(existent_week_folders)

        for i in range(len(unique_image_paths)):
            is_similar = compare_images(unique_image_paths[i], unique_image_paths[i + 1])

            if is_similar:
                is_some_image_similar = True

                # NOTE: remove similar image
                os.remove(unique_image_paths[i + 1])

                # TODO: increase counter for times he is seen
                db.get_collection('week_client').insert_one({
                    
                })
                

        has_similar_images = is_some_image_similar

def get_client_image_by_date (date, client_id):
    client_image = cv2.imread(f'./images/{date}/{client_id}.jpg')

currentWeekRange = DateTimeUtils.getCurrentWeekRange()
print(f"WEEK RANGE --> {currentWeekRange[0].strftime('%d-%m-%Y')} - {currentWeekRange[1].strftime('%d-%m-%Y')}")
compare_week_images(currentWeekRange)

# cursor = db.get_collection('day_client').find({
# "entry_date_time": {
    # "$gte": currentWeekRange[0].strftime("%d-%m-%Y"),
    # "$lte": currentWeekRange[1].strftime("%d-%m-%Y")
# }
# })

# currentWeekClients = list(cursor)

# for client in currentWeekClients:
    # print(client)

