import numpy
from PIL import Image
import cv2

color_deficit = 'd'
im = cv2.imread('yi.jfif')
#im =cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
RGB = numpy.asarray(im, dtype=float)

lms2lmsd = numpy.array([[1,0,0],[0.494207,0,1.24827],[0,0,1]])

lms2lmsp = numpy.array([[0,2.02344,-2.52581],[0,1,0],[0,0,1]])

lms2lmst = numpy.array([[1,0,0],[0,1,0],[-0.395913,0.801109,0]])

rgb2lms = numpy.array([[17.8824,43.5161,4.11935],[3.45565,27.1554,3.86714],[0.0299566,0.184309,1.46709]])

lms2rgb = numpy.linalg.inv(rgb2lms)

err2mod = numpy.array([[0,0,0],[0.7,1,0],[0.7,0,1]])

if color_deficit == 'd':
    lms2lms_deficit = lms2lmsd
elif color_deficit == 'p':
    lms2lms_deficit = lms2lmsp
elif color_deficit == 't':
    lms2lms_deficit = lms2lmst

    
LMS = numpy.zeros_like(RGB)               
for i in range(RGB.shape[0]):
    for j in range(RGB.shape[1]):
        rgb = RGB[i,j,:3]
        LMS[i,j,:3] = numpy.dot(rgb2lms, rgb)

_LMS = numpy.zeros_like(RGB)  
for i in range(RGB.shape[0]):
    for j in range(RGB.shape[1]):
        lms = LMS[i,j,:3]
        _LMS[i,j,:3] = numpy.dot(lms2lms_deficit, lms)

_RGB = numpy.zeros_like(RGB) 
for i in range(RGB.shape[0]):
    for j in range(RGB.shape[1]):
        _lms = _LMS[i,j,:3]
        _RGB[i,j,:3] = numpy.dot(lms2rgb, _lms)



error = (RGB-_RGB)

ERR = numpy.zeros_like(RGB) 
for i in range(RGB.shape[0]):
    for j in range(RGB.shape[1]):
        err = error[i,j,:3]
        ERR[i,j,:3] = numpy.dot(err2mod, err)

dtpn = ERR + RGB
    
for i in range(RGB.shape[0]):
    for j in range(RGB.shape[1]):
        dtpn[i,j,0] = max(0, dtpn[i,j,0])
        dtpn[i,j,0] = min(255, dtpn[i,j,0])
        dtpn[i,j,1] = max(0, dtpn[i,j,1])
        dtpn[i,j,1] = min(255, dtpn[i,j,1])
        dtpn[i,j,2] = max(0, dtpn[i,j,2])
        dtpn[i,j,2] = min(255, dtpn[i,j,2])

result = dtpn.astype('uint8')
    
im_converted = Image.fromarray(result, mode='RGB')
cv2.imshow("Deutranope",_RGB.astype('uint8'))
cv2.imwrite("Deutranope.jpg",_RGB.astype('uint8'))
cv2.imshow("Result",result)
cv2.imwrite("Result.jpg",result)

cv2.imshow("Original",RGB.astype('uint8'))
cv2.imwrite("Original.jpg",RGB.astype('uint8'))


    
