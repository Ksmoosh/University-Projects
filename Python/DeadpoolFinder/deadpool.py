from PIL import Image, ImageDraw, ImageChops
from matplotlib import numpy as np
import math, operator, functools

def porownaj_histogramy(deadpool, zdjecie):
    hist_deadpool = deadpool.histogram()
    hist_najlepszy = zdjecie.histogram()

    rmsBest = math.sqrt(functools.reduce(operator.add,
                        map(lambda a, b: (a - b) ** 2,
                            hist_deadpool, hist_najlepszy)) / len(hist_deadpool))

    wD, hD = deadpool.size
    wZ, hZ = zdjecie.size

    hist_deadpool[:] = [x / (wD*hD*4) for x in hist_deadpool]

    # przeszukanie calego zdjecia przeskakujac co 10 pikseli dla szybkosci
    for i in range(0, wZ - wD, 10):
        for j in range(0, hZ - hD, 10):
            box = (i, j, i + wD, j + hD)
            zdjecie_crop = zdjecie.crop(box)
            zdj_hist = zdjecie_crop.histogram()
            zdj_hist[:] = [x / (wD * hD * 4) for x in zdj_hist]
            rmsNew = math.sqrt(functools.reduce(operator.add,
                                                map(lambda a, b: (a - b) ** 2,
                                                    hist_deadpool, zdj_hist)) / len(hist_deadpool))
            if(rmsNew < rmsBest):
                rmsBest = rmsNew
                boxBest = box

    print(rmsBest)
    # ponowne przeszukanie mniejszego obszaru co 1 piksel zeby zwiekszyc dokladnosc

    for i in range(boxBest[0]-25, boxBest[2]+25, 1):
        for j in range(boxBest[1]-25, boxBest[3]+25, 1):
            box = (i, j, i + wD, j + hD)
            zdjecie_crop = zdjecie.crop(box)
            zdj_hist = zdjecie_crop.histogram()
            zdj_hist[:] = [x / (wD * hD * 4) for x in zdj_hist]
            rmsNew = math.sqrt(functools.reduce(operator.add,
                                                map(lambda a, b: (a - b) ** 2,
                                                    hist_deadpool, zdj_hist)) / len(hist_deadpool))
            if(rmsNew < rmsBest and box[0] > 0 and box[3] < wZ):
                rmsBest = rmsNew
                boxBest = box

    print(rmsBest)

    if(rmsBest < 0.007):
        deadpool2 = zdjecie.crop(boxBest)
        deadpool2.show()
        return boxBest

    # znajdz szerokosc deadpoola zmniejszajac bounding box od prawej
    for i in range(boxBest[0]+1, boxBest[2], 1):
        box = (boxBest[0], boxBest[1], i, boxBest[3])
        zdjecie_crop = zdjecie.crop(box)
        zdj_hist = zdjecie_crop.histogram()
        zdj_hist[:] = [x / ((i - boxBest[0]) * hD * 4) for x in zdj_hist]
        rmsNew = math.sqrt(functools.reduce(operator.add,
                                            map(lambda a, b: (a - b) ** 2,
                                                hist_deadpool, zdj_hist)) / len(hist_deadpool))
        if (rmsNew < rmsBest):
            rmsBest = rmsNew
            boxBest = box

    print(rmsBest)
    # znajdz szerokosc deadpoola zmniejszajac bounding box od lewej
    for i in range(boxBest[0]+1, boxBest[2], 1):
        box = (i, boxBest[1], boxBest[2], boxBest[3])
        zdjecie_crop = zdjecie.crop(box)
        zdj_hist = zdjecie_crop.histogram()
        zdj_hist[:] = [x / ((boxBest[2] - i) * hD * 4) for x in zdj_hist]
        rmsNew = math.sqrt(functools.reduce(operator.add,
                                            map(lambda a, b: (a - b) ** 2,
                                                hist_deadpool, zdj_hist)) / len(hist_deadpool))
        if (rmsNew < rmsBest):
            rmsBest = rmsNew
            boxBest = box

    wD = boxBest[2] - boxBest[0]

    print(rmsBest)
    # znajdz wysokosc deadpoola zmniejszajac bounding box od dolu
    for i in range(boxBest[1] + 1, boxBest[3], 1):
        box = (boxBest[0], boxBest[1], boxBest[2], i)
        zdjecie_crop = zdjecie.crop(box)
        zdj_hist = zdjecie_crop.histogram()
        zdj_hist[:] = [x / (wD * (i - boxBest[1]) * 4) for x in zdj_hist]
        rmsNew = math.sqrt(functools.reduce(operator.add,
                                            map(lambda a, b: (a - b) ** 2,
                                                hist_deadpool, zdj_hist)) / len(hist_deadpool))
        if (rmsNew < rmsBest):
            rmsBest = rmsNew
            boxBest = box

    print(rmsBest)
    # znajdz wysokosc deadpoola zmniejszajac bounding box od gory
    for i in range(boxBest[1] + 1, boxBest[3], 1):
        box = (boxBest[0], i, boxBest[2], boxBest[3])
        zdjecie_crop = zdjecie.crop(box)
        zdj_hist = zdjecie_crop.histogram()
        zdj_hist[:] = [x / (wD * (boxBest[3] -i) * 4) for x in zdj_hist]
        rmsNew = math.sqrt(functools.reduce(operator.add,
                                            map(lambda a, b: (a - b) ** 2,
                                                hist_deadpool, zdj_hist)) / len(hist_deadpool))
        if (rmsNew < rmsBest):
            rmsBest = rmsNew
            boxBest = box

    print(boxBest)

    return boxBest


def znajdz_deadpoola():
    im0 = Image.open("One_src_0.png")
    im1 = Image.open("One_src_1.png")

    deadpool = ImageChops.difference(im1.convert("RGB"), im0)
    box = deadpool.getbbox()

    deadpool = deadpool.crop(box)
    boxIdeadpool = im1.crop(box)

    draw = ImageDraw.Draw(im1)
    draw.rectangle(box, outline=(255, 0, 0))
    im1.save("DeadpoolZuraw.png")

    deadpool.putalpha(0)

    pixels1 = list(deadpool.getdata())
    pixels2 = list(boxIdeadpool.getdata())

    for i, v in enumerate(pixels1):
        if v == (0, 0, 0, 0):
            if(i%2 == 0):
                pixels2[i] = (255, 255, 255, 0)
            else:
                pixels2[i] = (0, 0, 0, 0)

    deadpool.putdata(pixels2)
    deadpool.save("Deadpool.png")

znajdz_deadpoola()

deadpool = Image.open("Deadpool.png")

zdjecie = Image.open("One_img1.png")
box = porownaj_histogramy(deadpool, zdjecie)
print(box)
draw1 = ImageDraw.Draw(zdjecie)
draw1.rectangle(box, outline=(255, 255, 255))
zdjecie.save("One_img1Deadpool.png")

zdjecie = Image.open("One_img2.png")
box = porownaj_histogramy(deadpool, zdjecie)
draw2 = ImageDraw.Draw(zdjecie)
draw2.rectangle(box, outline=(255, 255, 255))
zdjecie.save("One_img2Deadpool.png")

zdjecie = Image.open("One_img3.png")
box = porownaj_histogramy(deadpool, zdjecie)
draw3 = ImageDraw.Draw(zdjecie)
draw3.rectangle(box, outline=(255, 255, 255))
zdjecie.save("One_img3Deadpool.png")

zdjecie = Image.open("One_img4.png")
box = porownaj_histogramy(deadpool, zdjecie)
draw4 = ImageDraw.Draw(zdjecie)
draw4.rectangle(box, outline=(255, 255, 255))
zdjecie.save("One_img4Deadpool.png")

zdjecie = Image.open("One_img5.png")
box = porownaj_histogramy(deadpool, zdjecie)
draw5 = ImageDraw.Draw(zdjecie)
draw5.rectangle(box, outline=(255, 255, 255))
zdjecie.save("One_img5Deadpool.png")
