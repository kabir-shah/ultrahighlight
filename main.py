import cv2
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\shah95758\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract"

def image_to_text(image):
    text = ""

    _, threshold = cv2.threshold(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    dilation = cv2.dilate(threshold, kernel, iterations = 1)
    contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        cropped_image = image[y:y + h, x:x + w]
        text += pytesseract.image_to_string(cropped_image)
    
    return text

camera = cv2.VideoCapture(0)
_, image = camera.read()
images = [image]

while True:
    if cv2.waitKey(1) == 32:
        _, image = camera.read()
        images.append(image)
    if cv2.waitKey(1) == 27:
        break

    cv2.imshow("Ultralight", image)

image = cv2.hconcat(images)
print(image_to_text(image))

#image = cv2.putText(image, image_to_text(image), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
#cv2.imwrite('input.png', image)
#image = cv2.imread("input.png")
cv2.destroyAllWindows()
