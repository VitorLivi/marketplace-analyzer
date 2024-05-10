import cv2
import face_recognition

class FaceRecognizer:
    @staticmethod
    def find_face_encodings(image_path):
        image = cv2.imread(image_path)
        face_enc = face_recognition.face_encodings(image)
        if len(face_enc) > 0 :
            return face_enc[0]
        else:
            return None

    @staticmethod
    def is_images_similar(image_1, image_2):
        return face_recognition.compare_faces([image_1], image_2)[0]
