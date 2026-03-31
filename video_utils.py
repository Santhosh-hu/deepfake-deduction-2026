import cv2
from mtcnn import MTCNN

detector = MTCNN()

def extract_face_frames(video_path, max_frames=12):
    cap = cv2.VideoCapture(video_path)
    faces_list = []
    count = 0

    while cap.isOpened() and count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = detector.detect_faces(rgb)

        for face in faces:
            x, y, w, h = face["box"]

            # safety fix
            x, y = max(0, x), max(0, y)

            crop = rgb[y:y+h, x:x+w]

            if crop.size > 0:
                crop = cv2.resize(crop, (160,160))
                faces_list.append(crop)

        count += 1

    cap.release()
    return faces_list