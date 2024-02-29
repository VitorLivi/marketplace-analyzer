from ultralytics import YOLO
import cv2
import datetime
import uuid
import os
import face_recognition
from designer import Designer

from entities.client import Client

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
    global current_clients
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
            is_overlapping = designer.check_box_overlap(client.image_position, box_json)
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

def remove_client_temp_image(image_path):
    print(f"Removing temp image {image_path}")
    os.remove(image_path)

def save_client_today_image(image_path):
    image = cv2.imread(image_path)
    cv2.imwrite(f'./images/{date}/{uuid.uuid4()}.jpg', image)

def on_client_exit(client):
    global clients

    save_client_today_image(client.image)
    clients.remove(client)
    remove_client_temp_image(client.image)
    print(f"Client {client.id} removed")

def compare_similarity(new_client):
    global current_clients, clients

    if (len(current_clients) == 0):
        clients.append(new_client)
        return

    image_1 = find_face_encodings(new_client.image)

    if image_1 is None:
        print("No face found in the image")
        remove_client_temp_image(new_client.image)
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
        remove_client_temp_image(new_client.image)

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

def check_clients_last_seen():
    global clients

    for client in clients:
        if (client.is_client_exited()):
            on_client_exit(client)

def after_render():
    global current_clients

    check_clients_last_seen()

    for client in current_clients:
        compare_similarity(client)

designer = Designer()

while True:
    img = designer.get_frame()
    results = model(img, stream=True)

    print(f"Current clients length --> {len(current_clients)}")

    current_clients = []
    for r in results:
        boxes = r.boxes
 
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

            designer.draw_boxes(boxes, classNames)
            designer.draw_person_counter(len(current_clients))

            # class name
            cls = int(box.cls[0])
            if classNames[cls] == "person":
                on_find_person((x1, y1, x2, y2))

    designer.show_image()
    after_render()
    if designer.is_quit_key_pressed():
        break

designer.finalize()
