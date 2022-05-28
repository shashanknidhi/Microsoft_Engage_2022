import cv2
from facial_recognition.extract_encodings import encodings 
from imutils.video import VideoStream, FPS
import face_recognition as fr
import numpy as np
from facial_recognition.update_status import update_ticket_id



#To capture video
class FaceDetect(object):
    def __init__(self):
        self.vs = VideoStream(src=0).start()
        self.fps = FPS().start()
    def __del__(self):
        self.vs.stop()
    """
    Need : A camera frame object
    Do : Read the frame, find out the face location in the frame
    And : get the facial encoding data of current frame and already known encodings
    And : Compare them to find best match and update ticket id accordingly
    And : put a rectangle around the face via streaming with a text which is e-ticket no. of that particular passenger
    And : updates the frames one after another
    Return : a jpeg image in bytes format for the generator function in views.py
    """
    def get_frame(self):
        frame = self.vs.read()
        
        face_locations = fr.face_locations(frame)
        if len(face_locations) == 0:
            update_ticket_id('0')
        face_encodings = fr.face_encodings(frame, face_locations)
        known_data = encodings()
        known_face_encoding = known_data['encodings']
        known_ticket_id = known_data['ticket_id']
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = fr.compare_faces(known_face_encoding, face_encodings[0])
            ticket_id = "Unknown"

            face_distances = fr.face_distance(known_face_encoding, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                ticket_id = known_ticket_id[best_match_index]
            
            update_ticket_id(ticket_id)
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom -35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, ticket_id, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        self.fps.update()
        ret, jpeg = cv2.imencode('.jpg', frame)
        if cv2.waitKey(1) & 0xFF ==ord('q'):
            cv2.destroyAllWindow()
        
        return jpeg.tobytes()