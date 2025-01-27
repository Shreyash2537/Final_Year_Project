import cv2  
import numpy as np
import tensorflow as tf
import mediapipe as mp
import pygame
import time
from gtts import gTTS
from mutagen.mp3 import MP3

mpHands = mp.solutions.hands

hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)

mpDraw = mp.solutions.drawing_utils



# Load the TensorFlow SavedModel (.pb file)
model = tf.saved_model.load('mp_hand_gesture')
print(model.signatures)

# Load class names
f = open('gesture.names', 'r')
classNames = f.read().split('\n')
f.close()

print("Hand Gesture Robot")

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Get the inference function from the loaded model
infer = model.signatures['serving_default']

while True:
    # Read each frame from the webcam
    _, frame = cap.read()

    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    className = ''
    count = 0
    # Post-process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                count += 1
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([lmx, lmy])
                
            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)

            # Predict gesture using the loaded model
            landmarks = np.array(landmarks, dtype=np.float32).reshape(1, -1)  # Reshape for the model input
            prediction = infer(tf.convert_to_tensor(landmarks))  # Use the inference function

            # Get the predicted class
            classID = np.argmax(prediction['dense_16'].numpy())  # 'dense' is the name of the output layer
            className = classNames[classID]

            if className == 'okay':
                statement = 'okay'
            elif className == 'peace':
                statement = 'peace'
            elif className == 'thumbs up':
                statement = 'thumbs up'
            elif className == 'thumbs down':
                statement = 'thumbs down'
            elif className == 'call me':
                statement = 'call me'
            elif className == 'stop':
                statement = 'stop'
            elif className == 'rock':
                statement = 'rock'
            elif className == 'live long':
                statement = 'live long'
            elif className == 'fist':
                statement = 'fist'
            elif className == 'smile':
                statement = 'smile'
            else:
                statement = ''

            # Convert the recognized gesture to speech
            if len(statement.strip()) > 0:
                myobj = gTTS(text=statement, lang='en', slow=False)
                myobj.save("voice.mp3")
                song = MP3("voice.mp3")
                pygame.mixer.init()
                pygame.mixer.music.load('voice.mp3')
                pygame.mixer.music.play()
                time.sleep(song.info.length)
                pygame.quit()
                
            # Show the prediction on the frame
            cv2.putText(frame, className, (300, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
    # Show the final output
    cv2.imshow("Gesture to voice", frame) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()
