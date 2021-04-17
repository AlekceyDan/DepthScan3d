import cv2
import numpy as np


def start(im):
    fileStl = 'test_3d.stl'
    fileIm = im
    #fileIm = "test.jpg"
    stl = open(fileStl, 'w')

    im = cv2.imread(fileIm)

    im = cv2.flip(im, 1)
    ''' 
        *
        * Чтобы не было резких границ сгаживаем, а также нормируем чтобы несильно вытянутой была модель 
        *
    '''
    im = cv2.normalize(im, im, 0, 30, norm_type=cv2.NORM_MINMAX)
    im = cv2.GaussianBlur(im, (0, 0), 3)

    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # im = abs(255-im)
    im = cv2.resize(im, (640, 240))

    # gray = 255-gray
    # blur = cv2.resize(blur,(400,400))
    # gray = cv2.normalize(gray, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    # opencv-python

    # Функция по созданию треугольника
    def makeTriangle(cd_1, cd_2, cd_3):
        stl.write(o_1 + "facet normal 0 0 0")
        stl.write(o_2 + "outer loop")
        stl.write(o_3 + "vertex " + " ".join(cd_1))
        stl.write(o_3 + "vertex " + " ".join(cd_2))
        stl.write(o_3 + "vertex " + " ".join(cd_3))
        stl.write(o_2 + "endloop \n\tendfacet")

    x = 0
    y = 0
    cd_1 = ['0', '0', '0']  # первая вершина треульника в формате (x, y, intensity)
    cd_2 = ['0', '0', '0']  # вторая вершина треульника в формате (x, y, intensity)
    cd_3 = ['0', '0', '0']  # третья вершина треульника в формате (x, y, intensity)

    file = 'STL_project-1.stl'

    o_1 = "\n\t"
    o_2 = "\n\t\t"
    o_3 = "\n\t\t\t"

    stl.write("solid")

    # Создаем основу модели
    for i in range(im.shape[1] - 1):
        cd_1 = [str(i), "0", "0"]
        cd_3 = [str(i + 1), str(im.shape[0] - 1), "0"]
        cd_2 = [str(i), str(im.shape[0] - 1), "0"]
        makeTriangle(cd_1, cd_2, cd_3)
    for i in range(im.shape[1] - 1):
        cd_1 = [str(i + 1), str(im.shape[0] - 1), "0"]
        cd_3 = [str(i), "0", "0"]
        cd_2 = [str(i + 1), "0", "0"]
        makeTriangle(cd_1, cd_2, cd_3)

    # Создаем рельеф
    for i in range(im.shape[1]):
        for k in range(im.shape[0] - 1):
            if i != im.shape[1] - 1:
                try:

                    cd_1 = [str(i), str(k), str(im[k, i])]
                    cd_2 = [str(i + 1), str(k), str(im[k, i + 1])]
                    cd_3 = [str(i + 1), str(k + 1), str(im[k + 1, i + 1])]

                except:
                    print('er')
                makeTriangle(cd_1, cd_2, cd_3)
                try:
                    cd_1 = [str(i), str(k), str(im[k, i])]
                    cd_2 = [str(i + 1), str(k + 1), str(im[k + 1, i + 1])]
                    cd_3 = [str(i), str(k + 1), str(im[k + 1, i])]
                except:
                    print('er')
                makeTriangle(cd_1, cd_2, cd_3)
    stl.write("\nendsolid")
    stl.close()
    print('Done!')