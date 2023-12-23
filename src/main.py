import cv2
import dlib
import numpy as np
import getpass
import datetime
from db.models import DB

def calculate_EAR(eye):
    """
    This function calculates the Eye Aspect Ratio (EAR) which is a ratio used to determine if the eye is closed or open.
    It takes as input the coordinates of the six landmark points in one eye.
    The EAR is the ratio of the distance between the vertical eye landmarks and the distance between the horizontal eye landmarks.
    If the EAR is below a certain threshold, it indicates that the eye is closed.

    Parameters:
    eye (np.array): A numpy array containing the (x, y) coordinates of the six landmark points in the eye.

    Returns:
    ear (float): The Eye Aspect Ratio.
    """
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    C = np.linalg.norm(eye[0] - eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

# threshold for EAR below which we consider the eye to be closed
EAR_THRESHOLD = 0.2

# Load the detector
detector = dlib.get_frontal_face_detector()

# Load the predictor
predictor = dlib.shape_predictor("./model/shape_predictor_68_face_landmarks.dat")

# read the image
cap = cv2.VideoCapture(0)
db = DB()

while True:
    _, frame = cap.read()

    # Convert image into grayscale
    gray = cv2.cvtColor(src=frame, code=cv2.COLOR_BGR2GRAY)

    # Use detector to find faces
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(image=gray, box=face)

        # get the coordinates of the left eye
        left_eye = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(36, 42)])
        # get the coordinates of the right eye
        right_eye = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(42, 48)])

        cv2.rectangle(frame, (left_eye[0][0], left_eye[1][1]), (left_eye[3][0], left_eye[5][1]), (0, 255, 0), 1)
        cv2.rectangle(frame, (right_eye[0][0], right_eye[1][1]), (right_eye[3][0], right_eye[5][1]), (0, 255, 0), 1)

        # calculate the EAR for both eyes
        left_ear = calculate_EAR(left_eye)
        right_ear = calculate_EAR(right_eye)

        # average the EAR scores for both eyes
        ear = (left_ear + right_ear) / 2.0

        if ear < EAR_THRESHOLD:
            # Save to database
            username = getpass.getuser()
            db.insert_user(username)
            db.insert_user_history(username, datetime.datetime.now())
            print("*"*50)
            print("Saved to database!")
            print("*"*50)
            # Display a text
            cv2.putText(frame, "Eye is closed!", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        else:
            continue

    cv2.imshow("WebCam", frame) # Display the frame

    # Wait for user input - q, then you will stop the loop
    key = cv2.waitKey(delay=1)

    if key == ord("q"):
        break

# Close all windows
cap.release()
cv2.destroyAllWindows()
