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

def compare_week_images (week_range):
    days_of_week_range = DateTimeUtils.getDaysOfWeekRange(week_range)
    existent_week_folders = get_existent_week_folders(days_of_week_range)

    unique_image_paths = get_unique_image_paths(existent_week_folders)

    for image_path in unique_image_paths:
        current_image_to_compare = FaceRecognizer.find_face_encodings(image_path)

        for image_path2 in unique_image_paths:
            if image_path != image_path2:
                image_to_compare = FaceRecognizer.find_face_encodings(image_path2)
                is_similar = FaceRecognizer.is_images_similar(current_image_to_compare, image_to_compare)

                if is_similar:
                    # remove compared image from array to avoid duplicate
                    # maybe update database adding new similarity field refering to the similar client
                    # increase counter for similar client this id

    

def get_unique_image_paths(existent_week_folders):
    for day in existent_week_folders:
        all_image_name = os.listdir(f'./images/{day}')

        print(f"ALL IMAGE NAMES --> {all_image_name}")

        for image_name in all_image_name:
            unique_image_paths.append('./images/' + day + '/' + image_name)

def get_client_image_by_date (date, client_id):
    client_image = cv2.imread(f'./images/{date}/{client_id}.jpg')

currentWeekRange = DateTimeUtils.getCurrentWeekRange()
print(f"WEEK RANGE --> {currentWeekRange[0].strftime('%d-%m-%Y')} - {currentWeekRange[1].strftime('%d-%m-%Y')}")
compare_week_images(currentWeekRange)
print(similar_clients)

# cursor = db.get_collection('day_client').find({
# "entry_date_time": {
    # "$gte": currentWeekRange[0].strftime("%d-%m-%Y"),
    # "$lte": currentWeekRange[1].strftime("%d-%m-%Y")
# }
# })

# currentWeekClients = list(cursor)

# for client in currentWeekClients:
    # print(client)

