import cv2
import time
import datetime


capture = cv2.VideoCapture(0)


face_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml') 
body_cascade=cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml')


detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5

frame_size = (int(capture.get(3)), int(capture.get(4))) # get the width and height of the frame
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # fourcc is a 4-character code that specifies the video codec


while True:
    x, frame = capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5) # using 1.3 to balance between speed and accuracy, 5 is the number of faces to detect
    bodies = body_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) + len(bodies) > 0:
        if detection:
            timer_started = False # if someone keeps leaving and coming back in frame, we want to ensure one video not multiple milisecond ones
        
        else:
            detection = True
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            out = cv2.VideoWriter(f'video_{current_time}.mp4', fourcc, 20.0, frame_size) # create a video writer object
            print("Started recording!")
    elif detection:
        if timer_started:
            if time.time()-detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                print("Stop recording!")
        else:
            timer_started = True
            detection_stopped_time = time.time()
        

    if detection:
        out.write(frame)
    

   # for (x, y, width, height) in faces:
    #    cv2.rectangle(frame, (x, y), (x+width, y+height), (0, 0, 255), 3) # frame, top left corner, bottom right corner, BGR color, thickness

  
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break

out.release()
capture.release()
cv2.destroyAllWindows() # destroy the window showing video capturing device