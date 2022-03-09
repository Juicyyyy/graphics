from PIL import Image
import numpy as np

#функция черного, белого и красного изображения
def square_1(h, w, colour):
    data = np.zeros((h, w, 3), dtype = np.uint8)
    data[0:512, 0:512] = colour
    img = Image.fromarray(data, 'RGB')
    img.show()

#функция градиента от черного к белому
def square_2(h, w):
    data = np.zeros((h, w, 3), dtype=np.uint8)
    u = data.shape[2]
    n = data.shape[1]
    k = data.shape[0]
    for i in range(k):
        for j in range(n):
            for l in range(u):
                if data[i][j][l] == 0:
                    data[i][j][l] = (i+j+l) % 256
    img = Image.fromarray(data, 'RGB')
    img.show()

class Colour:
    colour_array = [0, 0, 0]

    def __init__(self, colour_array):
        self.colour_array = colour_array

class Picture:
    h = 512
    w = 512
    picture_array = np.zeros((h, w, 3), dtype=np.uint8)
    default_colour = [0, 0, 0]

    def __init__(self, h, w, col: Colour):
        self.h = h
        self.w = w
        self.picture_array = np.zeros((h, w, 3), dtype=np.uint8)
        self.default_colour = col.colour_array
        self.picture_array[0:h, 0:w] = col.colour_array

    def create_from_array(self, array):
        self.picture_array = array

    def set_pixel(self, x, y, color: Colour):
        self.picture_array[int(x), int(y)] = color.colour_array

    def show_picture(self):
        img = Image.fromarray(self.picture_array, 'RGB')
        img.show()

    def clear(self):
        self.picture_array[0:self.h, 0:self.w] = self.default_colour

#функция отрисовки звезды
def star_builder(variant, delta_t, pic_star, pic_colour):
    for i in range(13):
        a = (2 * np.pi * i) / 13
        variant(100 + 95 * np.cos(a), 100 + 95 * np.sin(a), 100, 100, pic_star, pic_colour, delta_t)
    pic_star.show_picture()

#функция отрисовки линий 1 вариант
def line_1(x1, y1, x0, y0, pic: Picture, colour: Colour, delta_t=0.1):
    t = 0.0
    while t < 1.0:
        x = x0 * (1.0 - t) + x1 * t
        y = y0 * (1.0 - t) + y1 * t
        pic.set_pixel(x, y, colour)
        t += delta_t

#функция отрисовки линий 2 вариант
def line_2(x1, y1, x0, y0, pic: Picture, colour: Colour, delta_t):
    x = x0
    while x <= x1:
        t = (x - x0) / (x1 - x0)
        y = y0 * (1.0 - t) + y1 * t
        pic.set_pixel(x, y, colour)
        x += 1

#функция отрисовки линий 3 вариант, вносим правки
def line_3(x1, y1, x0, y0, pic: Picture, colour: Colour, delta_t=0.0):
    steep = False
    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    x = x0
    while x <= x1:
        t = (x - x0) / (x1 - x0)
        y = y0 * (1.0 - t) + y1 * t
        if steep:
            pic.set_pixel(y, x, colour)
        else:
            pic.set_pixel(x, y, colour)
        x += 1

#функция отрисовки линий 4 вариант (алгоритм Брезенхема)
def line_4(x1, y1, x0, y0, pic: Picture, colour: Colour, delts_t=0.0):
    steep = False
    if abs(x0 - x1) < abs(y0 - y1):
        x0, y0 = y0, x0
        x1, y1 = y1, x1
        steep = True
    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0
    dx = x1 - x0
    dy = y1 - y0
    derror = abs(dy / float(dx))
    error = 0.
    y = y0
    for x in range(int(x0), int(x1) + 1):
        if steep:
            pic.set_pixel(y, x, colour)
        else:
            pic.set_pixel(x, y, colour)
        error += derror
        if error > 0.5:
            if y1 > y0:
                y += 1
            else:
                y -= 1
            error -= 1.

#функция считывания вершин из файла
def peaks_file(filename):
    f = open(filename)
    s = f.read().split('\n')
    source = list()

    for i in s:
        if len(i) != 0 and i[0] == 'v' and i[1] == ' ':
            source.append(i)
    workspace = list()
    for i in source:
        workspace.append(i.split())
    return workspace

#функция считывания полигонов из файла
def polygon_file(filename):
    f = open(filename)
    s = f.read().split('\n')
    source = list()

    for i in s:
        if len(i) != 0 and i[0] == 'f' and i[1] == ' ':
            source.append(i)
    workspace = list()
    for i in source:
        workspace.append(i.split())
    result = list()

    for i in workspace:
        result.append([i[1].split('/')[0], i[2].split('/')[0], i[3].split('/')[0]])
    return result

if __name__ == '__main__':

    # №_1
    #создание черного изображения
    square_1(512, 512, [0, 0, 0])
    #создание белого изображения
    square_1(512, 512, [255, 255, 255])
    #создание красного изображения
    square_1(512, 512, [255, 0, 0])
    #создание изображения с градиентом
    square_2(512, 512)

    # №_3
    default_picture_colour = Colour([0, 0, 0])
    colour = Colour([255, 255, 255])
    pic = Picture(200, 200, default_picture_colour)

    #отрисовка звезды 1 вариант при дельта = 0.01 => получаем линии
    delta_t = 0.01
    star_builder(line_1, delta_t, pic, colour)
    pic.clear()

    #отрисовка звезды 1 вариант при дельта = 0.1 => получаем пунктир
    delta_t = 0.1
    star_builder(line_1, delta_t, pic, colour)
    pic.clear()

    #отрисовка звезды 2 вариант (не рабочий)
    star_builder(line_2, delta_t, pic, colour)
    pic.clear()

    #отрисовка звезды 3 вариант (рабочий)
    star_builder(line_3, delta_t, pic, colour)
    pic.clear()

    #отрисовка звезды 4 вариант (алгоритм Брезенхема)
    star_builder(line_4, delta_t, pic, colour)
    pic.clear()

    # №_5
    pic = Picture(1000, 1000, default_picture_colour)

    #массив вершин
    peaks_array = peaks_file('StormTrooper.obj')

    #отрисовка вершин
    for i in range(1, len(peaks_array)):
        line_1(float(peaks_array[i][1]) * 100 + 500, float(peaks_array[i][2]) * 100 + 500,
               float(peaks_array[i - 1][1]) * 100 + 500, float(peaks_array[i - 1][2]) * 100 + 500,
               pic, colour, 1000)

    # №_7
    #массив полигонов
    polygon_array = polygon_file('StormTrooper.obj')

    #отрисовка полигонов 
    for i in polygon_array:
        i_0 = int(i[0]) if int(i[0]) > 0 else len(peaks_array) - 1 + int(i[0]) 
        i_1 = int(i[1]) if int(i[1]) > 0 else len(peaks_array) - 1 + int(i[1])  
        i_2 = int(i[2]) if int(i[2]) > 0 else len(peaks_array) - 1 + int(i[2]) 

        #первое ребро (вершины 1 и 2)
        line_4(float(peaks_array[i_0 - 1][1]) * 100 + 500, float(peaks_array[i_0 - 1][2]) * 100 + 500,
               float(peaks_array[i_1 - 1][1]) * 100 + 500 + 1, float(peaks_array[i_1 - 1][2]) * 100 + 500 + 1,
               pic, colour, 1000)

        #второе ребро (вершины 1 и 3)
        line_4(float(peaks_array[i_0 - 1][1]) * 100 + 500, float(peaks_array[i_0 - 1][2]) * 100 + 500,
               float(peaks_array[i_2 - 1][1]) * 100 + 500 + 1, float(peaks_array[i_2 - 1][2]) * 100 + 500 + 1,
               pic, colour, 1000)

        #третье ребро (вершины 2 и 3)
        line_4(float(peaks_array[i_1 - 1][1]) * 100 + 500, float(peaks_array[i_1 - 1][2]) * 100 + 500,
               float(peaks_array[i_2 - 1][1]) * 100 + 500 + 1, float(peaks_array[i_2 - 1][2]) * 100 + 500 + 1,
               pic, colour, 1000)
    pic.show_picture()
