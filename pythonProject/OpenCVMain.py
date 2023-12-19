import cv2
import numpy as np
from imutils.video import VideoStream
import imutils
from time import sleep

# название окна подстройки
WINDOWNAME = "Настройка тона"

# минимальный размер контуров пятна
BLOBSIZE = 1500

# константы насыщенности и яркости
S_MIN = 29
S_MAX = 255
V_MIN = 148
V_MAX = 255

# цвет прямоугольника (B, G, R)
RECTCOLOR = (0, 255, 0)

# толщина линии прямоугольника
RTHICK = 2

# определяем функцию проверки размера пятна
def checkSize(w, h):
    if w * h > BLOBSIZE:
        return True
    else:
        return False

# определяем пустую функцию
def empty(a):
    pass

# определяем размеры кадра
frameSize = (320, 240)

# создаём объект видео потока
vs = VideoStream(src=0, usePiCamera=True, resolution=frameSize, framerate=32).start()

# ждём окончания инициализации видеопотока
sleep(2)

# создаём окно с ползунком
cv2.namedWindow(WINDOWNAME)
cv2.resizeWindow(WINDOWNAME, 500, 100)
cv2.createTrackbar("Hue", WINDOWNAME, 0, 180, empty)

while True:

        # получаем кадр изображения
        image = vs.read()

        # получаем максимальный и минимальный тон из значения ползунка
        h_min = cv2.getTrackbarPos("Hue", WINDOWNAME) - 10
        h_max = cv2.getTrackbarPos("Hue", WINDOWNAME) + 10

        # определяем границы цвета в HSV
        lower_range = np.array([h_min, S_MIN, V_MIN])
        upper_range = np.array([h_max, S_MAX, V_MAX])

        # конвертируем изображение в HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # создаём маску выбранного цвета
        thresh = cv2.inRange(hsv, lower_range, upper_range)

        # побитово складываем оригинальную картинку и маску
        bitwise = cv2.bitwise_and(image, image, mask=thresh)

        # показываем картинку маски цвета
        cv2.imshow("bitwise", bitwise)

        # удаляем цвет из маски
        gray = cv2.cvtColor(bitwise, cv2.COLOR_BGR2GRAY)

        # ищем контуры в картинке
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # если контуры найдены...
        if len(contours) != 0:


            # выводим найденные контуры
            #cv2.drawContours(image, contours, -1, 255, 1)

            # находим контуры бОльшего размера
            c = max(contours, key = cv2.contourArea)

            # получаем координаты прямоугольника, в который они вписаны
            x,y,w,h = cv2.boundingRect(c)

            # если прямоугольник достаточного размера...
            if checkSize(w, h):

                # выводим его
                cv2.rectangle(image, (x, y), (x+w, y+h), RECTCOLOR, RTHICK)

        # Показываем картинку с квадратом выделения
        cv2.imshow("Image", image)

        # Если была нажата клавиша ESC
        k = cv2.waitKey(1)
        if k == 27:

            # прерываем выполнение цикла
            break

# закрываем все окна
cv2.destroyAllWindows()

# останавливаем видео поток
vs.stop()