import numpy as np
import cv2

import DenseDepth.test as net
import os


def video(vid,path='/home/AlekceyDan/SamsungProject/DenseDepth'):


  for name in os.listdir('/home/AlekceyDan/SamsungProject/DenseDepth/'):
    if name.endswith(".png"):
      os.remove('/home/AlekceyDan/SamsungProject/DenseDepth/'+name)

  cap = cv2.VideoCapture(vid)
  frame = []
  flag = True
  i=0
  while(flag):
    flag = cap.read()[0]
    if flag == False:
      break
    a = cv2.resize(cap.read()[1],(640,480))
    a = a-a.min()
    a = a/a.max()*255
    cv2.imwrite(path+'/tes_in'+str(i)+'.png',a)
    a = net.depth_net(input_im=path+'/tes_in'+str(i)+'.png',out_im=path+'/tes'+str(i)+'.png')

    i+=1
  cap.release()


def save():
  os.system("ffmpeg -r 20 -i /home/AlekceyDan/SamsungProject/DenseDepth/tes%01d.png -vcodec mpeg4 -y /home/AlekceyDan/SamsungProject/movie.mp4")

