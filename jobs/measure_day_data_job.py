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

def get_today_folder():
    if os.path.exists(f'./images/{today.strftime("%d-%m-%Y")}'):
        return './images/' + today.strftime("%d-%m-%Y")

    return None

def compare_day_images (week_range):
    today_folder = get_today_folder()

    if (today_folder == None):
        return

    unique_image_paths = get_unique_image_paths(today_folder)

    for image_path in unique_image_paths:
        current_image_to_compare = FaceRecognizer.find_face_encodings(image_path)

        for image_path2 in unique_image_paths:
            if image_path != image_path2:
                image_to_compare = FaceRecognizer.find_face_encodings(image_path2)
                is_similar = FaceRecognizer.is_images_similar(current_image_to_compare, image_to_compare)

                if is_similar:
                    # do something
    

def get_unique_image_paths(today_folder):
    unique_image_paths = []
    all_image_name = os.listdir(today_folder)

    for image_name in all_image_name:
        unique_image_paths.append(today_folder + '/' + image_name)


def get_client_image_by_date (date, client_id):
    client_image = cv2.imread(f'./images/{date}/{client_id}.jpg')

compare_day_images()
