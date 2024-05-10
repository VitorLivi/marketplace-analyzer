import cv2
import os
import face_recognition
from face_recognizer import FaceRecognizer
from designer import Designer
from entities.client import Client
from utils.file_utils import FileUtils
from recognizer import Recognizer
from database import Database
import time

FileUtils.remove_all_in_dir(os.path.abspath('./images/temp'))
FileUtils.create_today_dir(os.path.abspath('./images'))

current_clients = []
clients = []

db = Database()
def on_client_exit(client):
    global clients

    client.calc_time_spent()
    client.save_today_image()

    print(f"Client TIME SPENT {client.time_spent}")

    db.get_database().get_collection("day_client").insert_one(client.to_json())

    clients.remove(client)
    client.remove_temp_image()
    print(f"Client {client.id} removed")

def compare_clients_similarity(new_client):
    global current_clients, clients

    if (len(current_clients) == 0):
        clients.append(new_client)
        return

    image_1 = FaceRecognizer.find_face_encodings(new_client.image)

    if image_1 is None:
        print("No face found in the image")
        new_client.remove_temp_image()
        return

    print ("Current client ids -->", [client.id for client in clients])

    image_is_similar_to_some_client = False
    for client in clients:
        image_2 = FaceRecognizer.find_face_encodings(client.image)
        isImageSimilar = face_recognition.compare_faces([image_1], image_2)[0]
            
        if isImageSimilar:
            client.set_last_seen()
            image_is_similar_to_some_client = True
            break

    if not image_is_similar_to_some_client:
        print("Image is not similar to any client")
        clients.append(new_client)
    else:
        print("Image is similar to some client")
        new_client.remove_temp_image()

def on_find_person(coords):
    global current_clients

    if coords is None:
        return

    new_client = Client()
    image_path = f'./images/temp/{new_client.id}.jpg'
    cv2.imwrite(image_path, img[coords[1]:coords[3], coords[0]:coords[2]])

    new_client.set_image_position({
        "x1": coords[0],
        "y1": coords[1],
        "x2": coords[2],
        "y2": coords[3]
    })
    new_client.set_image(image_path)
    current_clients.append(new_client)


def on_find_gun(coords):
    print(f"Gun found at {coords}")


def check_clients_last_seen():
    global clients

    for client in clients:
        if (client.is_client_exited()):
            on_client_exit(client)

designer = Designer()
recognizer = Recognizer()

last_gun_model_execution = None
seconds_to_execute_gun_model = 2
while True:
    img = designer.get_frame()
    results = recognizer.run(img)

    if (last_gun_model_execution != None):
        print(f"Time to execute gun model --> {time.time() - last_gun_model_execution}")
    if last_gun_model_execution == None or (time.time() - last_gun_model_execution) > seconds_to_execute_gun_model:
        print("Running gun model")
        last_gun_model_execution = time.time()
        gun_results = recognizer.run_gun_model(img)

        for r in gun_results:
            class_name = r.names.get(0)
            boxes = r.boxes
            
            for box in boxes:
                if class_name == "gun":
                    on_find_gun(box.xyxy[0])

                designer.draw_boxes(boxes, [class_name])


    print(f"Current clients length --> {len(current_clients)}")

    current_clients = []
    for r in results:
        boxes = r.boxes
 
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

            designer.draw_boxes(boxes, Recognizer.classNames)
            designer.draw_person_counter(len(current_clients))

            cls = int(box.cls[0])
            if Recognizer.classNames[cls] == "person":
                on_find_person((x1, y1, x2, y2))

            designer.find_overlap_boxes_with_clients(current_clients)

    designer.show_image()
    check_clients_last_seen()
    
    for client in current_clients:
        compare_clients_similarity(client)

    if designer.is_quit_key_pressed():
        break

designer.finalize()
