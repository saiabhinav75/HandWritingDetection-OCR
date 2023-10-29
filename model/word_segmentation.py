import cv2
import numpy as np,matplotlib.pyplot as plt

# image=cv2.imread(r"static\uploads\handwritten3.jpg")
def thresholding(image):
    img_gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret,thresh=cv2.threshold(img_gray,80,255,cv2.THRESH_BINARY_INV)
    # plt.imshow(thresh,cmap='gray')
    return thresh


def dilation(img):
    kernel=np.ones((10,20),np.uint8)
    dilated=cv2.dilate(img,kernel,iterations=1)
    return dilated

def contours(img):
    (contours, heirarchy) = cv2.findContours(img.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    sorted_contours_lines = sorted(contours, key = lambda ctr : cv2.boundingRect(ctr)[1]) # (x, y, w, h)
    return sorted_contours_lines

def segmenting(img,contour_lines):
    img2 = img.copy()
    listOfWords=[]
    for ctr in contour_lines:
        
        x,y,w,h = cv2.boundingRect(ctr)
        cv2.rectangle(img2, (x,y), (x+w, y+h), (40, 100, 250), 2)
        listOfWords.append([x,y,x+w,y+h])
    return listOfWords

# thresh_img=thresholding(image.copy())
# dilated=dilation(thresh_img.copy())
# contour_lines=contours(dilated.copy())
# listOfWords=segmenting(image,contour_lines)
# print(listOfWords)
# plt.imshow(listOfWords)
# plt.show()
