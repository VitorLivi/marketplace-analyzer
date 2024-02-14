from inspect import currentframe
from ultralytics import YOLO
import cv2
import math
import datetime
import uuid
import os
import face_recognition

from entities.client import Client
from database import Database

dirs = os.listdir('./images/temp')
for file in dirs:
    os.remove(f'./images/temp/{file}')

date = datetime.date.strftime(datetime.date.today(), "%d-%m-%Y")

if not os.path.exists(f'./images/{date}'):
    os.makedirs(f'./images/{date}')

current_clients = []
clients = []

# db = Database()

# db.get_default_database().get_collection("client").insert_many([
#     {
#         "name": "John",
#         "age": 25
#     },
#     {
#         "name": "Jane",
#         "age": 30
#     }
# ])

# start webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1080)
cap.set(4, 1080)

# model
model = YOLO("yolov8n.pt")

# object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]

def find_overlap_boxes_with_person(boxes):
    for box in boxes:
        cls = int(box.cls[0])
        if classNames[cls] == "person":
            continue

        x1, y1, x2, y2 = box.xyxy[0]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

        box_json = {
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2
        }

        for client in current_clients:
            is_overlapping = check_box_overlap(client.image_position, box_json)
            print(f"Is overlapping --> {is_overlapping}")

            if is_overlapping:
                client.set_tag(classNames[cls])

def find_face_encodings(image_path):
    image = cv2.imread(image_path)
    face_enc = face_recognition.face_encodings(image)
    if len(face_enc) > 0 :
        return face_enc[0]
    else:
        return None

def remove_temp_image(image_path):
    print(f"Removing temp image {image_path}")
    os.remove(image_path)

def save_client_today_image(image_path):
    image = cv2.imread(image_path)
    cv2.imwrite(f'./images/{date}/{uuid.uuid4()}.jpg', image)

def on_client_exit(client):
    save_client_today_image(client.image)
    clients.remove(client)
    remove_temp_image(client.image)
    print(f"Client {client.id} removed")

def compare_similarity(new_client):
    if (len(current_clients) == 0):
        clients.append(new_client)
        return

    image_1 = find_face_encodings(new_client.image)

    if image_1 is None:
        print("No face found in the image")
        remove_temp_image(new_client.image)
        return

    print ("Current client ids -->", [client.id for client in clients])

    image_is_similar_to_some_client = False
    for client in clients:
        image_2 = find_face_encodings(client.image)
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
        remove_temp_image(new_client.image)

def on_find_person(coords):
    global current_clients

    new_uuid = uuid.uuid4()
    image_path = f'./images/temp/{new_uuid}.jpg'
    cv2.imwrite(image_path, img[coords[1]:coords[3], coords[0]:coords[2]])

    new_client = Client(new_uuid)
    new_client.set_image_position({
        "x1": coords[0],
        "y1": coords[1],
        "x2": coords[2],
        "y2": coords[3]
    })
    new_client.set_image(image_path)
    current_clients.append(new_client)


def check_box_overlap(box1, box2):
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2
    
    if (x1 < x4 and x2 > x3 and y1 < y4 and y2 > y3):
        return True

    return False


def check_clients_last_seen():
    global clients

    for client in clients:
        if (client.last_seen < datetime.datetime.now() - datetime.timedelta(seconds=5)):
            on_client_exit(client)


def after_render():
    global clients
    global current_clients

    check_clients_last_seen()

    for client in current_clients:
        compare_similarity(client)

def draw_person_counter():
    cv2.putText(img, f"Person count: {len(current_clients)}", (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

def draw_boxes(results):
    global current_clients

    current_clients = []
    for r in results:
        boxes = r.boxes
 
        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

            # class name
            cls = int(box.cls[0])
            if classNames[cls] == "person":
                on_find_person((x1, y1, x2, y2))

            # put box in cam
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # confidence
            confidence = math.ceil((box.conf[0]*100))/100
            # print("Confidence --->", confidence)
            # print("Class name -->", classNames[cls])

            # object details
            org = [x1, y1]
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2

            cv2.putText(img, f"{classNames[cls]} {confidence}", org,
                        font, fontScale, color, thickness)

        find_overlap_boxes_with_person(boxes)


while True:
    success, img = cap.read()
    results = model(img, stream=True)

    draw_boxes(results)
    draw_person_counter()
    after_render()

    cv2.imshow('Webcam', img)
    if cv2.waitKey(1000) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
