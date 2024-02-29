import cv2
import math

class Designer:
    def __init__(self):
        self.initialize()

    def initialize(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 1080)
        cap.set(4, 1080)
        self.cap = cap

    def get_frame(self):
        ret, img = self.cap.read()
        self.img = img
        return img

    def check_box_overlap(self, box1, box2):
        x1, y1, x2, y2 = box1
        x3, y3, x4, y4 = box2
        
        if (x1 < x4 and x2 > x3 and y1 < y4 and y2 > y3):
            return True

        return False

    def draw_boxes(self, boxes, classNames):
        for box in boxes:
            # bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # convert to int values

            # put box in cam
            cv2.rectangle(self.img, (x1, y1), (x2, y2), (255, 0, 255), 3)

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

            cls = int(box.cls[0])
            cv2.putText(self.img, f"{classNames[cls]} {confidence}", org,
                        font, fontScale, color, thickness)

    def draw_person_counter(self, length):
        cv2.putText(self.img, f"Person count: {length}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    def is_quit_key_pressed(self):
        return cv2.waitKey(1000) == ord('q')

    def show_image(self):
        cv2.imshow("Image", self.img)

    def finalize(self):
        self.cap.release()
        cv2.destroyAllWindows()
        
