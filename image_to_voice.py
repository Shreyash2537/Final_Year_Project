# Import required packages
import cv2
import pytesseract
import pygame
import time
from gtts import gTTS
from mutagen.mp3 import MP3

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'  # Ensure this path is correct

# Read image from which text needs to be extracted
img = cv2.imread("image1.jpg")

# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Performing OTSU threshold
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

# Specify structure shape and kernel size.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# Creating a copy of image for display
im2 = img.copy()

# Extracted text variable
text1 = ''
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)

    # Drawing a rectangle on copied image
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Cropping the text block for giving input to OCR
    cropped = im2[y:y + h, x:x + w]

    # Apply OCR on the cropped image
    text1 += ' ' + pytesseract.image_to_string(cropped)

# Clean up the recognized text
text1 = text1.strip()

# Check if text was recognized
print('\n--------------Recognized Text------------\n')
print(text1)  

# Convert the text to speech if recognized
if text1:
    myobj = gTTS(text=text1, lang='en', slow=False)
else:
    print("No text recognized from the image.")
    myobj = gTTS(text="Sorry, no text could be recognized.", lang='en', slow=False)

# Save the speech to an mp3 file
myobj.save("voice.mp3")

# Play the audio
print('\n--------------Playing------------\n')
song = MP3("voice.mp3")
pygame.mixer.init()
pygame.mixer.music.load('voice.mp3')
pygame.mixer.music.play()
time.sleep(song.info.length)  # Wait for the audio to finish playing
pygame.quit()

# Display the image with the detected text boxes
cv2.imshow('Image to voice', im2)
cv2.waitKey(0)  # Wait for a key press to close the window
cv2.destroyAllWindows()  # Close all OpenCV windows
