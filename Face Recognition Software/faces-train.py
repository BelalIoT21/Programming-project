# import the required libraries
import cv2
import os
import numpy as np
from PIL import Image
import pickle


cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")

recognise = cv2.face.LBPHFaceRecognizer_create()

# Skapat en funktion 
def getdata():

    current_id = 0
    label_id = {} #ordbok
    face_train = [] # list
    face_label = [] # list
    
    # Hitta sökvägen till baskatalogen, dvs sökvägen där denna fil placeras
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Jag har skapat "image_data"-mappen som innehåller data så i princip
    # Jag lägger till dess väg till basbanan
    my_face_dir = os.path.join(BASE_DIR,'images')

    # Hitta alla mappar och filer i mappen "image_data".
    for root, dirs, files in os.walk(my_face_dir):
        for file in files:

            # Kontrollerar om filen har extensionen ".png" eller ".jpg"
            if file.endswith("png") or file.endswith("jpg"):

                # Lägga till sökvägen till filen med bassökvägen
                # så du har i princip bildens sökväg
                path = os.path.join(root, file)

                # Tar namnet på mappen som etikett, dvs hans/hennes namn
                label = os.path.basename(root).lower()

                # tillhandahålla etikett-ID som 1 eller 2 och så vidare för olika personer
                if not label in label_id:
                    label_id[label] = current_id
                    current_id += 1
                ID = label_id[label]

                # konvertera bilden till gråskalebild
                # du kan också använda cv2-biblioteket för denna åtgärd
                pil_image = Image.open(path).convert("L")

                # konvertera bilddata till numpy array
                image_array = np.array(pil_image, "uint8")
        
                # identifiera ansiktena
                face = cascade.detectMultiScale(image_array)

                # hitta intresseregionen och lägga till data
                for x,y,w,h in face:
                    img = image_array[y:y+h, x:x+w]
                #image_array = cv2.rectangle(image_array,(x,y),(x+w,y+h),(255,255,255),3)
                    cv2.imshow("Test",img)
                    cv2.waitKey(1)
                    face_train.append(img)
                    face_label.append(ID)

    # sträng etikettdata till en fil
    with open("labels.pickle", 'wb') as f:
        pickle.dump(label_id, f)
   

    return face_train,face_label

# skapar ".yml"-fil
face,ids = getdata()
recognise.train(face, np.array(ids))
recognise.save("trainner.yml")