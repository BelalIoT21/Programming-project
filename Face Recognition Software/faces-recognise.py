# importera de nödvändiga biblioteken
import serial
import cv2
import pickle

# Ställer in seriell port till COM4 vid överföringshastighet på 9600
port = serial.Serial('COM4', 9600)

# Ladda ansiktskaskadklassificerare
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

# Ladda den tränade ansiktsigenkänningsmodellen
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")

# Ladda etiketterna
labels = {"person_name": 1}
with open("labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v: k for k, v in og_labels.items()}
    print(labels)

# Öppna videoinspelningen
cap = cv2.VideoCapture(0)

while True:
    # Fånga bildruta för bildruta
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for (x, y, w, h) in faces:
        # Extrahera regionen av intresse (ROI)
        roi_gray = gray[y:y+h, x:x+w]  # (ycord_start, ycord_end)
        roi_color = frame[y:y+h, x:x+w]

        # Känn igen ansiktet
        id_, conf = recognizer.predict(roi_gray)
        if conf >= 15 and conf <= 65:
            print(id_)
            print(labels[id_])
            # Skriv ut den förutsedda etiketten
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = labels[id_]
            color = (255, 255, 255)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            # skicka 0 eller 1 till Arduino baserat på ID
            if id_ == 0:
                port.write(b'0')
            elif id_ == 1 or id_ == 2:
                port.write(b'1')
        else:
            # Om ansiktet inte känns igen, märk det som "Okänt"
            print("unknown")
            # Skriv ut den förutsedda etiketten
            font = cv2.FONT_HERSHEY_SIMPLEX
            name = "unknown"
            color = (0, 0, 255)
            stroke = 2
            # skicka 2 till Arduino om ansiktet är okänt
            port.write(b'2')
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)

        # Rita en rektangel runt ansiktet
        color = (255, 0, 0)  # BGR 0-255
        stroke = 2
        end_cord_x = x + w -20
        end_cord_y = y + h +20
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)

    # Visa den resulterande ramen
    cv2.imshow('frame', frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# När allt är klart släpper du infångningen
cap.release()
cv2.destroyAllWindows()