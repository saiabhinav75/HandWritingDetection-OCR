import cv2,os
from easyocr import Reader
from flask import current_app as app,redirect,url_for

font=cv2.FONT_HERSHEY_SIMPLEX
fontscale=1
color=(40, 100, 250)
thickness=2
from word_segmentation import thresholding,dilation,contours,segmenting
path=""
img=cv2.imread(path)

langs=["en"]
print("Languages to be parsed",langs)

reader=Reader(langs,gpu=True)

@app.route("/display/<filename>",method=['GET'])
def display_output(filename):
    img=cv2.imread("static/uploads/" + filename)
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    h,w, c=img.shape

    if w > 1000:
        new_w=1000
        ar=w/h
        new_h=int(new_w/ar)
        img=cv2.resize(img,(new_w,new_h),interpolation=cv2.INTER_AREA)

    thresh_img=thresholding(img.copy())
    dilated=dilation(thresh_img.copy())
    contour_lines=contours(dilated.copy())
    listOfWords=segmenting(img,contour_lines)

    for i in range(len(listOfWords)):
        roi = img[listOfWords[i][1]:listOfWords[i][3], listOfWords[i][0]:listOfWords[i][2]]
        result=reader.readtext(roi)
        if len(result):
            word=result[0][1]
            print(word)
            x,y=listOfWords[i][0],listOfWords[i][1]
            cv2.putText(img,word,(x-1,y-1),font,fontscale,color,thickness,cv2.LINE_AA)

        cv2.imwrite("output/"+filename,img)
    return redirect(url_for('output',filename='uploads/' + filename),code=301)
