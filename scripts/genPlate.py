#coding=utf-8
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw, ImageColor, ImageFont
import cv2;
import numpy as np;
import os;
from math import *

import argparse
import string
import random

#font = ImageFont.truetype("Arial-Bold.ttf",14)

index = { "0": 1, "1": 2, "2": 3, "3": 4, "4": 5, "5": 6,
         "6": 7, "7": 8, "8": 9, "9": 10, "A": 11, "B": 12, "C": 13, "D": 14, "E": 15, "F": 16, "G": 17, "H": 18,
         "J": 19, "K": 20, "L": 21, "M": 22, "N": 23, "P": 24, "Q": 25, "R": 26, "S": 27, "T": 28, "U": 29, "V": 30,
         "W": 31, "X": 32, "Y": 33, "Z": 34};

chars = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
         "A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
         ];

def GenCh(f,val):
    img=Image.new("RGB", (23,70),(255,255,255))
    draw = ImageDraw.Draw(img)
    draw.text((0, 2),val,(0,0,0),font=f)
    img =  img.resize((23,70))
    A = np.array(img)

    return A

def GenCh1(f,val):
    img=Image.new("RGB", (23,70),(255,255,255))
    draw = ImageDraw.Draw(img)
    # draw.text((0, 2),val.decode('utf-8'),(0,0,0),font=f)
    draw.text((0, 2), val, (0,0,0), font=f)
    A = np.array(img)
    return A



def r(val):
    return int(np.random.random() * val)



class GenPlate:


    def __init__(self):

        #self.fontC =  ImageFont.truetype(fontCh,43,0);
        # self.fontC =  ImageFont.truetype("/home/yeleussinova/data_SSD/license_plate_generation/font/platechar.ttf",40,0)
        # self.fontE =  ImageFont.truetype("/home/yeleussinova/data_SSD/license_plate_generation/font/platechar.ttf",40,0)
        self.img = np.array(Image.new("RGB", (226,70),(255,255,255)))
        # self.bg  = cv2.resize(cv2.imread("/home/yeleussinova/data_SSD/generate_LP/images/template.bmp"),(226,70))
        # self.smu = cv2.imread("/home/yeleussinova/data_SSD/license_plate_generation/templates/smu2.jpg")


    def draw(self,val):
        offset= 0 ;

        self.img[0:70, offset+8:offset+8+23]= GenCh1(self.fontC, val[0]);
        self.img[0:70, offset+8+23+6:offset+8+23+6+23]= GenCh1(self.fontE, val[1]);
        for i in range(5):
            base = offset+8+23+6+23+17 +i*23 + i*6 ;
            self.img[0:70, base  : base+23]= GenCh1(self.fontE,val[i+2]);
        return self.img

    def generate(self,text):

            fg = self.draw(text);
            fg = cv2.bitwise_not(fg);
            com = cv2.bitwise_or(fg,self.bg);

            return com

    def hconcat_resize_min(self, im_list, interpolation=cv2.INTER_CUBIC):
        h_min = min(im.shape[0] for im in im_list)
        im_list_resize = [cv2.resize(im, (int(im.shape[1] * h_min / im.shape[0]), h_min), interpolation=interpolation)
                          for
                          im in im_list]
        return cv2.hconcat(im_list_resize)

    def genPlateString(self,pos,val):
        plateStr = "";
        box = [0, 0, 0, 0, 0];
        if(pos != -1):
            box[pos] = 1;
        for unit, cpos in zip(box,range(len(box))):
            if unit == 1:
                plateStr += val
            else:
                if cpos == 0:
                    plateStr += chars[r(11)]
                elif cpos == 1:
                    plateStr += chars[11+r(10)]
                else:
                    plateStr += chars[11 + r(10)]
        return plateStr;

    def genBatch(self, batchSize,pos,charRange, outputPath,size):
        if (not os.path.exists(outputPath)):
            os.mkdir(outputPath)
        for i in range(batchSize):
            plateStr = G.genPlateString(-1,-1)

            img = G.generate(plateStr);

            filename = os.path.join(outputPath + "/" +  plateStr + ".jpg")
            cv2.imwrite(filename, img);

    def text_generator(self, size=1):
        chars = string.ascii_uppercase
        # mong_chars = 'АБВГДЕЗИКЛМНОӨПРСТУҮХЦЧЭЯ'
        # chars= mong_chars.lower()
        return ''.join(random.choice(chars) for _ in range(size))

    def digit_generator(self, size=0):
        chars = string.digits
        return ''.join(random.choice(chars) for _ in range(size))

    def drawLabels(self, labelPath, outputPath):
        if (not os.path.exists(outputPath)):
            os.mkdir(outputPath)
        if os.path.exists(labelPath):
            labels = open(labelPath)
            lines = labels.readlines()
            for line in lines:
                imgName = os.path.basename(line.strip().split(" ")[0])
                label = line.strip().split(" ")[1]

                print(label)
                imgNew=Image.new("RGB", (226,70),(255,255,255))
                draw = ImageDraw.Draw(imgNew)
                draw.text((25, 15), label.upper(), (0,0,0), font = self.fontC)
                A = np.array(imgNew)
                filename = os.path.join(outputPath, imgName)
                cv2.imwrite(filename, cv2.resize(A, (128, 32)))
        else:
            print("label's file not found")

    def generate_img(self, count, start_id, outputPath, annot_out_path, state, square=False):

        if not os.path.exists(outputPath):
            os.mkdir(outputPath)
        if not os.path.exists(annot_out_path):
            os.mkdir(annot_out_path)
        for i in range(count):

            # gen = random.randint(0, 100)
            # if gen > 50:
            #     plateStr = G.genPlateString(-1, -1)
            # elif gen > 75:
            # plateStr = G.text_generator(2)
            plateDigit = G.digit_generator(size=5)
            plateStr = G.text_generator(size=2)
            # else:
            #     plateStr = G.text_generator(6)

            if state == 'uae_20':
                imgNew = Image.open("../templates/uae_20.png")
                # imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 42
                font = ImageFont.truetype("../font/DealerplateW05Maryland.ttf", fontsize)
                draw.text((60, -2), plateDigit, font=font, fill=(0,0,0,0))
                outLabel = 'bb' + plateDigit + ',abu-dhabi'

            if state == 'uae_bb':
                imgNew = Image.open("../templates/uae_bb.png")
                # imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 42
                font = ImageFont.truetype("../font/DealerplateW05Maryland.ttf", fontsize)
                draw.text((60, -2), plateDigit, font=font, fill=(0,0,0,0))
                outLabel = 'bb' + plateDigit + ',dubai'

            if state == 'marocco_squared':
                s = 'هـ'
                l = {
                        'أ': 'a', 'ب' : 'b', 'د':'d', 'هـ':'h', 'و':'e', 'ط':'t'
                     }
                imgNew = Image.open("../templates/marocco_squar.jpg")
                imgNew = imgNew.resize((158, 118))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 55
                font1 = ImageFont.truetype("../font/KFGQPC Uthmanic Script HAFS Regular.otf", fontsize)
                font2 = ImageFont.truetype("../font/dealerplate_california.ttf", 55)
                draw.text((20, -20), s, font=font1, fill=(50, 50, 50, 45))
                draw.text((90, 8), plateDigit, font=font2, fill=(50, 50, 50, 45))
                draw.text((23, 68), plateDigit2, font=font2, fill=(50, 50, 50, 45))

                outLabel = l[s] + plateDigit + plateDigit2



            if state == 'marocco_1':
                marokko_letters = ['a', 'b', 'd', 'h', 'e', 't']
                imgNew = Image.open("../templates/marocco_1.jpg")
                imgNew = imgNew.resize((200, 60))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 48
                font1 = ImageFont.truetype("../font/dealerplate_california.ttf", fontsize)
                font2 = ImageFont.truetype("../font/DealerplateW00Michigan.ttf", fontsize)
                draw.text((6, -2), plateDigit, font=font2, fill=(50, 50, 50, 45))
                draw.text((165, -2), plateStr, font=font2, fill=(50, 50, 50, 45))
                outLabel = plateDigit + 'e' + plateStr

            if state == 'marocco_2':
                imgNew = Image.open("../templates/marocco_2.jpg")
                imgNew = imgNew.resize((200, 60))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 48
                font1 = ImageFont.truetype("../font/dealerplate_california.ttf", fontsize)
                font2 = ImageFont.truetype("../font/DealerplateW00Michigan.ttf", fontsize)
                draw.text((12, -2), plateDigit, font=font2, fill=(40, 40, 50, 45))
                draw.text((167, -2), plateStr, font=font2, fill=(40, 40, 50, 45))
                outLabel = plateDigit + 'h' + plateStr

            if state == 'marocco_3':
                imgNew = Image.open("../templates/marocco_3.jpg")
                imgNew = imgNew.resize((200, 60))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 48
                font1 = ImageFont.truetype("../font/dealerplate_california.ttf", fontsize)
                font2 = ImageFont.truetype("../font/DealerplateW00Michigan.ttf", fontsize)
                draw.text((12, -2), plateDigit, font=font2, fill=(40, 40, 50, 45))
                draw.text((167, -2), plateStr, font=font2, fill=(40, 40, 50, 45))
                outLabel = plateDigit + 'b' + plateStr

            if state == 'marocco_4':
                imgNew = Image.open("../templates/marocco_4.jpg")
                imgNew = imgNew.resize((200, 60))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 45
                font1 = ImageFont.truetype("../font/dealerplate_california.ttf", fontsize)
                font2 = ImageFont.truetype("../font/DealerplateW00Michigan.ttf", fontsize)
                draw.text((7, 13), plateDigit, font=font1, fill=(40, 40, 50, 45))
                draw.text((167, 13), plateStr, font=font1, fill=(40, 40, 50, 45))
                outLabel = plateDigit + 'd' + plateStr

            if state == 'marocco_5':
                imgNew = Image.open("../templates/marocco_5.jpg")
                imgNew = imgNew.resize((220, 62))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 48
                font1 = ImageFont.truetype("../font/dealerplate_california.ttf", fontsize)
                font2 = ImageFont.truetype("../font/DealerplateW00Michigan.ttf", fontsize)
                draw.text((7, 13), plateDigit, font=font1, fill=(40, 40, 50, 45))
                draw.text((180, 13), plateStr, font=font1, fill=(40, 40, 50, 45))
                outLabel = plateDigit + 't' + plateStr

            if state == 'marocco_6':
                imgNew = Image.open("../templates/marocco_6.jpg")
                imgNew = imgNew.resize((200, 60))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 46
                font1 = ImageFont.truetype("../font/dealerplate_california.ttf", fontsize)
                font2 = ImageFont.truetype("../font/DealerplateW00Michigan.ttf", fontsize)
                draw.text((7, 12), plateDigit, font=font1, fill=(40, 40, 50, 45))
                draw.text((153, 12), plateStr, font=font1, fill=(40, 40, 50, 45))
                outLabel = plateDigit + 'a' + plateStr

            if state == 'oman_red_1':
                imgNew = Image.open("../templates/oman_red_1.jpg")
                imgNew = imgNew.resize((200, 60))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 52
                font = ImageFont.truetype("../font/DINEngschriftStd.otf", fontsize)
                draw.text((7, 12), plateDigit, font=font, fill=(216, 204, 208, 255))
                fontsize = 28
                font = ImageFont.truetype("../font/DINEngschriftStd.otf", fontsize)
                draw.text((97, 34), plateStr[0] + "  " + plateStr[1], font=font, fill=(216, 204, 208, 255))
                outLabel = plateDigit + plateStr.replace(" ", "").lower() + ',oman'

            if state == 'oman_red_2':
                imgNew = Image.open("../templates/oman_red_2.jpg")
                imgNew = imgNew.resize((148, 44))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 39
                font = ImageFont.truetype("../font/DINEngschriftStd.otf", fontsize)
                draw.text((2, 8), plateDigit, font=font, fill=(180, 160, 160, 255))
                fontsize = 20
                font = ImageFont.truetype("../font/DINEngschriftStd.otf", fontsize)
                draw.text((77, 28), plateStr, font=font, fill=(180, 160, 160, 255))
                outLabel = plateDigit + plateStr.replace(" ", "").lower() + ',oman'

            if state == 'uae_aa':
                imgNew = Image.open("../templates/uae_aa.png")
                # imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 60
                font = ImageFont.truetype("../font/DINEngschriftStd.otf", fontsize)
                draw.text((70, 10), plateDigit.upper(), font=font, fill=(0,0,0,0))
                outLabel = 'aa' + plateDigit + ',dubai'

            if state == 'uae_aa_up':
                imgNew = Image.open("../templates/uae_aa_up.png")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 40
                font = ImageFont.truetype("../font/DINEngschriftStd.otf", fontsize)
                draw.text((25, 35), plateDigit.upper(), font=font, fill=(0,0,0,0))
                outLabel = 'aa' + plateDigit + ',dubai'

            if state == 'oman2':
                img = Image.open("../templates/oman2.png")
                img = img.resize((190, 64))
                draw = ImageDraw.Draw(img)
                font2 = ImageFont.truetype("../font/HeartlandSans.otf", 22)
                draw.text((96, 35), plateStr.upper(), font=font2, fill=(32,11,1,255))

                img2 = Image.open("../templates/oman3.png")
                img2 = img2.resize((65, 25))
                fontsize = 30
                font = ImageFont.truetype("../font/DINEngschriftStd.otf", fontsize)
                draw2 = ImageDraw.Draw(img2)
                draw2.text((5, 2), plateDigit.upper(), font=font, fill=(32,11,1,255))
                img2 = img2.resize((75, 45))
                img.paste(img2, (5,10,80,55), img2)
                imgNew = img

            if state == 'oman':
                img = Image.open("../templates/oman.png")
                img = img.resize((90, 50))
                draw = ImageDraw.Draw(img)
                fontsize = 56
                font = ImageFont.truetype("../font/DINEngschriftStd.otf", fontsize)
                draw.text((0, 4), plateStr.upper(), font=font, fill=(32,11,1,255))
                imgNew = Image.open("../templates/oman1.png")
                img = img.resize((50, 35))
                imgNew.paste(img, (5,3,55,38), img)


            if state == 'bahrein':
                imgNew = Image.open("../templates/bahrein_1.png")
                imgNew = imgNew.resize((135, 58))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 61
                font = ImageFont.truetype("../font/DINEngschriftStd.otf", fontsize)
                draw.text((12, 8), plateStr.upper(), font=font, fill=(32,11,1,255))
                img = Image.open("../templates/bahrein.png")
                imgNew = imgNew.resize((66, 55))
                img.paste(imgNew, (0,0,66,55), imgNew)


            if state == 'uae':
                imgNew = Image.open("../templates/uae.png")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 55
                font = ImageFont.truetype("../font/DINEngschriftStd.otf", fontsize)
                draw.text((12, 22), plateStr.upper(), font=font, fill=(0,0,0,0))

            if state == 'california':
                imgNew = Image.open("../templates/california.png")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 42
                font = ImageFont.truetype("/home/yeleussinova/data_SSD/generate_LP/font/dealerplate_california.ttf", fontsize)
                draw.text((8, 24), plateStr.upper(), font=font, fill=(24, 28, 81, 255))

            if state == 'texas':
                imgNew = Image.open("../templates/texas.jpg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 35
                font = ImageFont.truetype("/home/yeleussinova/data_SSD/generate_LP/font/Cooperative-Regular.ttf",
                                          fontsize)
                if len(plateStr) == 7:
                    draw.text((10, 20), plateStr.upper()[:3] + '  ' + plateStr.upper()[3:], (0, 0, 0), font=font)
                elif len(plateStr) == 6:
                    draw.text((17, 20), plateStr.upper()[:2] + '   ' + plateStr.upper()[2:], (0, 0, 0), font=font)
                else:
                    draw.text((17, 20), plateStr.upper()[:2] + '   ' + plateStr.upper()[2:], (0, 0, 0), font=font)

            if state == 'pensylvania':
                imgNew = Image.open("../templates/pensylvania.png")
                imgNew = imgNew.resize((140, 64))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 40
                font = ImageFont.truetype("/home/yeleussinova/data_SSD/generate_LP/font/dealerplate_california.ttf",
                                          fontsize)
                draw.text((13, 15), plateStr.upper()[:3] + ' ' + plateStr.upper()[3:], font=font, fill=(24, 28, 81, 255))

            if state == 'minnesota':
                gen = random.choice([0, 1])
                imgNew = Image.open("../templates/minnesota.jpeg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 44
                font = ImageFont.truetype("/home/yeleussinova/data_SSD/generate_LP/font/DealerplateW00Wisconsin.ttf",
                                          fontsize)
                if gen:
                    color = (45, 83, 201, 255)
                else:
                    color = (0, 0, 0, 0)
                draw.text((6, 9), plateStr.upper()[:3] + '  ' + plateStr.upper()[3:], font=font, fill=color)

            if state == 'alabama':
                imgNew = Image.open("../templates/alabama.jpg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 40
                font = ImageFont.truetype("/home/yeleussinova/data_SSD/generate_LP/font/DealerplateW00Wisconsin.ttf",
                                          fontsize)
                draw.text((10, 8), plateStr.upper(), font=font, fill=(0, 0, 0, 0))

            if state == 'arizona':
                imgNew = Image.open("../templates/arizona.jpg")
                imgNew = imgNew.resize((158, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 40
                font = ImageFont.truetype(
                    "/home/yeleussinova/data_SSD/generate_LP/font/DealerplateW00Massachusetts.ttf", fontsize)
                draw.text((20, 8), plateStr.upper(), font=font, stroke_width=0, fill=(0, 0, 0, 0))

            if state == 'florida':
                    imgNew = Image.open("../templates/florida.jpg")
                    imgNew = imgNew.resize((140, 70))
                    draw = ImageDraw.Draw(imgNew)
                    fontsize = 42
                    font = ImageFont.truetype("../font/DealerplateW00New Jersey.ttf", fontsize)
                    if len(plateStr) == 6:
                        draw.text((7, 8), plateStr.upper()[:3] + '    ' + plateStr.upper()[3:], font=font, stroke_width=0, fill=(2,78,47,255))
                    else:
                        draw.text((10, 8), plateStr.upper()[:2] + '  ' + plateStr.upper()[2:], font=font, stroke_width=0, fill=(2, 78, 47, 255))

            if state == 'kentucky':
                imgNew = Image.open("../templates/kentucky.jpg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 38
                font = ImageFont.truetype("../font/DealerplateW00Pennsylvania.ttf", fontsize)
                draw.text((9, 11), plateStr.upper()[:3] + '   ' + plateStr.upper()[3:], font=font, stroke_width=0,
                          fill=(45, 64, 114, 255))

            if state == 'new_jersey':
                fontsize = 40
                font = ImageFont.truetype("../font/DealerplateW00New Jersey.ttf", fontsize)
                if len(plateStr) == 6:
                    imgNew = Image.open("../templates/new_jersey2.jpg")
                    imgNew = imgNew.resize((128, 70))
                    draw = ImageDraw.Draw(imgNew)
                    draw.text((9, 10), plateStr.upper()[:3] + '  ' + plateStr.upper()[3:], font=font, stroke_width=0,
                              fill=(0, 0, 0, 0))
                elif len(plateStr) == 7:
                    imgNew = Image.open("../templates/new_jersey1.jpg")
                    imgNew = imgNew.resize((128, 70))
                    draw = ImageDraw.Draw(imgNew)
                    draw.text((10, 8), plateStr.upper(), font=font, stroke_width=0, fill=(0, 0, 0, 0))

            if state == 'new_york':
                fontsize = 42
                font = ImageFont.truetype("../font/DealerplateW00NewYork_yellow.ttf", fontsize)
                imgNew = Image.open("../templates/new_york.png")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                draw.text((12, 7), plateStr.upper()[:3] + '    ' + plateStr.upper()[3:], font=font, stroke_width=0,
                          fill=(3, 25, 57, 255))

            if state == 'new_york_yellow':
                fontsize = 40
                font = ImageFont.truetype("../font/DealerplateW00NewYork_yellow.ttf", fontsize)
                if len(plateStr) == 7:
                    imgNew = Image.open("../templates/new_york_yellow.jpg")
                    imgNew = imgNew.resize((128, 70))
                    draw = ImageDraw.Draw(imgNew)
                    draw.text((14, 10), plateStr.upper()[:3] + '  ' + plateStr.upper()[3:], font=font, stroke_width=0,
                              fill=(0, 0, 0, 0))
                elif len(plateStr) == 5:
                    imgNew = Image.open("../templates/new_york2.jpg")
                    imgNew = imgNew.resize((128, 70))
                    draw = ImageDraw.Draw(imgNew)
                    draw.text((32, 10), plateStr.upper(), font=font, stroke_width=0, fill=(0, 0, 0, 0))
                else:
                    imgNew = Image.open("../templates/new_york2.jpg")
                    imgNew = imgNew.resize((128, 70))
                    draw = ImageDraw.Draw(imgNew)
                    draw.text((10, 10), plateStr.upper(), font=font, stroke_width=0, fill=(0, 0, 0, 0))

            if state == 'new_york_white':
                fontsize = 40
                font = ImageFont.truetype("../font/DealerplateW00NewYork_yellow.ttf", fontsize)
                if len(plateStr) == 7:
                    s = 0
                    p = 0
                    for x in plateStr.upper():
                        if x in string.ascii_uppercase:
                            s += 1
                            P = p
                        else:
                            p += 1
                            S = s
                    if S == 3:
                        imgNew = Image.open("../templates/new_york_white.jpg")
                        imgNew = imgNew.resize((128, 70))
                        draw = ImageDraw.Draw(imgNew)
                        draw.text((13, 10), plateStr.upper()[:3] + '  ' + plateStr.upper()[3:], font=font, stroke_width=0,
                                  fill=(49, 48, 84, 255))
                    if P == 5:
                        imgNew = Image.open("../templates/new_york_white1.jpg")
                        imgNew = imgNew.resize((128, 70))
                        draw = ImageDraw.Draw(imgNew)
                        draw.text((13, 10), plateStr.upper()[:5] + '  ' + plateStr.upper()[5:], font=font, stroke_width=0,
                                  fill=(49, 48, 84, 255))
                    if P == 2:
                        imgNew = Image.open("../templates/new_york_white2.jpg")
                        imgNew = imgNew.resize((128, 70))
                        draw = ImageDraw.Draw(imgNew)
                        draw.text((13, 10), plateStr.upper()[:2] + '  ' + plateStr.upper()[2:], font=font, stroke_width=0,
                                  fill=(49, 48, 84, 255))
                elif len(plateStr) == 4:
                    imgNew = Image.open("../templates/new_york_white2.jpg")
                    imgNew = imgNew.resize((128, 70))
                    draw = ImageDraw.Draw(imgNew)
                    draw.text((34, 10), plateStr.upper()[:3] + '  ' + plateStr.upper()[3:], font=font, stroke_width=0,
                              fill=(49, 48, 84, 255))
                else:
                    imgNew = Image.open("../templates/new_york_white2.jpg")
                    imgNew = imgNew.resize((128, 70))
                    draw = ImageDraw.Draw(imgNew)
                    draw.text((10, 10), plateStr.upper(), font=font, stroke_width=0, fill=(49, 48, 84, 255))

            if state == 'massachusetts':
                fontsize = 39
                font = ImageFont.truetype("../font/DealerplateW00Massachusetts.ttf", fontsize)
                imgNew = Image.open("../templates/massachusetts.png")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                if len(plateStr) == 6:
                    s = 0
                    for x in plateStr.upper():
                        if x in string.ascii_uppercase:
                            s += 1
                    if s == 6:
                        draw.text((10, 10), plateStr.upper(), font=font, stroke_width=0, fill=(185, 46, 47, 255))
                    else:
                        draw.text((7, 10), plateStr.upper()[:3] + ' ' + plateStr.upper()[3:], font=font, stroke_width=0,
                                  fill=(185, 46, 47, 255))
                elif len(plateStr) == 5:
                    draw.text((16, 10), plateStr.upper(), font=font, stroke_width=0,
                              fill=(185, 46, 47, 255))
                else:
                    draw.text((30, 10), plateStr.upper(), font=font, stroke_width=0,
                              fill=(185, 46, 47, 255))

            if state == 'maryland':
                fontsize = 42
                font = ImageFont.truetype("../font/DealerplateW05Maryland.ttf", fontsize)
                imgNew = Image.open("../templates/maryland.jpg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                if len(plateStr) == 6:
                    draw.text((8, 7), plateStr.upper()[:3] + '  ' + plateStr.upper()[3:], font=font, stroke_width=0,
                              fill=(0, 0, 0, 0))

            if state == 'texas_war':
                fontsize = 35
                font = ImageFont.truetype("../font/BwStretch-Medium.otf",
                                          fontsize)
                imgNew = Image.open("../templates/texas_war.jpg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                draw.text((8, 15), plateStr.upper()[:3] + '  ' + plateStr.upper()[3:], font=font, stroke_width=0,
                          fill=(0, 0, 0, 0))

            if state == 'texas_horse':
                fontsize = 35
                font = ImageFont.truetype("../font/dealerplate_california.ttf", fontsize)
                imgNew = Image.open("../templates/texas_horse.jpg")
                imgNew = imgNew.resize((100, 60))
                draw = ImageDraw.Draw(imgNew)
                draw.text((5, 17), plateStr.upper()[:3] + '  ' + plateStr.upper()[3:], font=font, stroke_width=0,
                          fill=(4,31,77,255))

            if state == 'michigan':
                fontsize = 40
                font = ImageFont.truetype("../font/DealerplateW00Michigan.ttf", fontsize)
                imgNew = Image.open("../templates/michigan.jpeg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                draw.text((5, 9), plateStr.upper()[:3] + '  ' + plateStr.upper()[3:], font=font, stroke_width=0,
                          fill=(17, 50, 99, 255))

            if state == 'missisippi':
                fontsize = 35
                font = ImageFont.truetype("../font/DealerplateW00Pennsylvania.ttf", fontsize)
                imgNew = Image.open("../templates/missisippi.jpeg")
                imgNew = imgNew.resize((125, 60))
                draw = ImageDraw.Draw(imgNew)
                draw.text((10, 9), plateStr.upper()[:3] + '    ' + plateStr.upper()[3:], font=font, stroke_width=0,
                                fill=(8,13,56,255))

            if state == 'ohio':
                fontsize = 39
                font = ImageFont.truetype("../font/DealerplateW00Ohio.ttf", fontsize)
                imgNew = Image.open("../templates/ohio.png")
                imgNew = imgNew.resize((125, 70))
                draw = ImageDraw.Draw(imgNew)
                s = 0
                for l in plateStr.upper():
                    if l in string.ascii_uppercase:
                        s += 1
                if s == 5:
                    draw.text((12, 12), plateStr.upper()[:5] + ' ' + plateStr.upper()[5:], font=font, stroke_width=0,
                              fill=(8, 13, 56, 255))
                else:
                    draw.text((6, 12), plateStr.upper()[:3] + ' ' + plateStr.upper()[3:], font=font, stroke_width=0,
                              fill=(8, 13, 56, 255))

            if state == 'virginia':
                fontsize = 40
                font = ImageFont.truetype("../font/DealerplateW00Virginia.ttf", fontsize)
                imgNew = Image.open("../templates/virginia.png")
                imgNew = imgNew.resize((125, 70))
                draw = ImageDraw.Draw(imgNew)
                i = random.randint(0, 1)
                if i:
                    draw.text((8, 12), plateStr.upper()[:3] + '-' + plateStr.upper()[3:], font=font, stroke_width=0,
                          fill=(0, 21, 73, 255))
                else:
                    draw.text((8, 12), plateStr.upper(), font=font, stroke_width=0,
                          fill=(0, 21, 73, 255))

            if state == 'colorado':
                fontsize = 38
                font = ImageFont.truetype("../font/DealerplateW00Michigan.ttf", fontsize)
                imgNew = Image.open("../templates/colorado.png")
                imgNew = imgNew.resize((125, 70))
                draw = ImageDraw.Draw(imgNew)
                draw.text((8, 12), plateStr.upper()[:3] + ' - ' + plateStr.upper()[3:], font=font, stroke_width=0,
                          fill=(1, 63, 49, 255))

            if state == 'colorado_new':
                fontsize = 38
                font = ImageFont.truetype("../font/DealerplateW00New Jersey.ttf", fontsize)
                imgNew = Image.open("../templates/colorado.png")
                imgNew = imgNew.resize((125, 70))
                draw = ImageDraw.Draw(imgNew)
                draw.text((8, 12), plateStr.upper()[:3] + ' - ' + plateStr.upper()[3:], font=font, stroke_width=0,
                          fill=(1, 63, 49, 255))

            if state == 'wisconsin':
                fontsize = 38
                font = ImageFont.truetype("../font/DealerplateW00Wisconsin.ttf", fontsize)
                imgNew = Image.open("../templates/wisconsin.jpg")
                imgNew = imgNew.resize((125, 70))
                draw = ImageDraw.Draw(imgNew)
                #draw.text((11, 9), plateStr.upper(), font=font, stroke_width=0, fill=(174, 46, 61, 255))
                if len(plateStr) ==3:
                    draw.text((35, 9), plateStr.upper(), font=font, stroke_width=0, fill=(174,46,61,255))
                elif len(plateStr) ==4:
                    draw.text((27, 9), plateStr.upper(), font=font, stroke_width=0, fill=(174,46,61,255))
                elif len(plateStr) ==5:
                    draw.text((20, 9), plateStr.upper(), font=font, stroke_width=0, fill=(174,46,61,255))
                elif len(plateStr) ==6:
                    draw.text((16, 9), plateStr.upper(), font=font, stroke_width=0, fill=(174,46,61,255))
                else:
                    draw.text((11, 9), plateStr.upper(), font=font, stroke_width=0, fill=(174,46,61,255))

            if state == 'wisconsin_white':
                fontsize = 38
                font = ImageFont.truetype("../font/DealerplateW00Wisconsin.ttf", fontsize)
                imgNew = Image.open("../templates/wisconsin_white.jpeg")
                imgNew = imgNew.resize((125, 70))
                draw = ImageDraw.Draw(imgNew)
                draw.text((10, 15), plateStr.upper()[:3] + ' - ' + plateStr.upper()[3:], font=font, stroke_width=0, fill=(0,0,0,0))

            if state == 'tennessee':
                fontsize = 42
                font = ImageFont.truetype("../font/DealerplateW00Wisconsin.ttf", fontsize)
                imgNew = Image.open("../templates/tennessee.jpeg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                draw.text((6, 8), plateStr.upper()[:3] + '   ' + plateStr.upper()[3:], font=font, stroke_width=0, fill=(0,0,0,0))

            if state == 'oregon_new':
                fontsize = 38
                font = ImageFont.truetype("../font/DealerplateW00New Jersey.ttf", fontsize)
                imgNew = Image.open("../templates/oregon.jpeg")
                imgNew = imgNew.resize((125, 65))
                draw = ImageDraw.Draw(imgNew)
                draw.text((7,5), plateStr.upper()[:3] + '   ' + plateStr.upper()[3:], font=font, stroke_width=0, fill=(33,48,96,255))

            if state == 'connecticut':
                    fontsize = 38
                    font = ImageFont.truetype("../font/DealerplateW05Maryland.ttf", fontsize)
                    imgNew = Image.open("../templates/connecticut.jpeg")
                    imgNew = imgNew.resize((125, 6))
                    draw = ImageDraw.Draw(imgNew)
                    draw.text((14,8), plateStr.upper()[:3] + ' ' + plateStr.upper()[3:], font=font, stroke_width=0, fill=(33,48,96,255))

            if state == 'mongolia_type0':
                imgNew = Image.new("RGB", (146, 36), (255, 255, 255))
                # draw = ImageDraw.Draw(imgNew)
                label = ' ' + plateStr[:4] + ' ' + plateStr[4:]
                print(label)
                for id, char in enumerate(label):
                    if char in string.digits:
                        char_img = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/font/black/digits/" + char + ".png")
                        char_img = char_img.resize((21, 35))
                        imgNew.paste(char_img, (id * 15, 1), char_img)
                    elif char == ' ':
                        pass
                    else:
                        char_img = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/font/black/letters/" + char + ".png")
                        char_img = char_img.resize((23, 43))
                        imgNew.paste(char_img, (id * 15, -2), char_img)

            if state == 'mongolia_type1':
                imgNew = Image.new("RGB", (160, 36), (255, 255, 255))
                # draw = ImageDraw.Draw(imgNew)
                first = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/plates/soembo.png")
                second = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/plates/mng.png")
                imgNew.paste(first, (0, 0), first)
                imgNew.paste(second, (80, 7), second)
                label = ' ' + plateStr[:4] + '  ' + plateStr[4:]
                print(label)
                for id, char in enumerate(label):

                    if char in string.digits:
                        char_img = Image.open(
                            "/home/yeleussinova/data_SSD/mongolia/mn/font/black/digits/" + char + ".png")
                        char_img = char_img.resize((21, 35))
                        if id == 1:
                            imgNew.paste(char_img, (id * 17, 1), char_img)
                        else:
                            imgNew.paste(char_img, (id * 15, 1), char_img)
                    elif char == ' ':
                        pass
                    else:
                        char_img = Image.open(
                            "/home/yeleussinova/data_SSD/mongolia/mn/font/black/letters/" + char + ".png")
                        char_img = char_img.resize((23, 43))
                        imgNew.paste(char_img, (id * 15, -2), char_img)

            if state == 'squared_type1':
                imgNew = Image.new("RGB", (88, 60), (255, 255, 255))
                # draw = ImageDraw.Draw(imgNew)
                label = plateStr
                print(label)
                for id, char in enumerate(label):
                    if char == 'a':
                        char = 'а'
                    elif char =='h':
                        char = 'н'
                    elif char == "y":
                        char = "у"
                    elif char == "m":
                        char = "м"
                    elif char == "m":
                        char = "м"

                    if char in string.digits:
                        char_img = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/font/black/digit/" + char + ".png")
                        char_img = char_img.resize((21, 25))
                        if id == 0:
                            imgNew.paste(char_img, (id * 15 + 5, 3), char_img)
                        elif id == 1:
                            imgNew.paste(char_img, (id * 15 + 7, 3), char_img)
                        elif id == 2:
                            imgNew.paste(char_img, (id * 23, 3), char_img)
                        elif id == 3:
                            imgNew.paste(char_img, (id * 21, 3), char_img)
                    elif char == ' ':
                        pass
                    else:
                        char_img = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/font/black/letter/" + char + ".png")
                        char_img = char_img.resize((16, 22))
                        imgNew.paste(char_img, (id * 15 -40, 33), char_img)

            if state == 'squared_type3':
                imgNew = Image.new("RGB", (88, 60), (255, 255, 255))
                # draw = ImageDraw.Draw(imgNew)
                first = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/plates/soembo.png").resize((15,26))
                second = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/plates/mng.png").resize((24,18))
                imgNew.paste(first, (5, 29), first)
                imgNew.paste(second, (61, 35), second)
                label = plateStr
                print(label)
                for id, char in enumerate(label):
                    if char == 'a':
                        char = 'а'
                    elif char =='h':
                        char = 'н'
                    elif char == "y":
                        char = "у"
                    elif char == "m":
                        char = "м"
                    elif char == "m":
                        char = "м"

                    if char in string.digits:
                        char_img = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/font/black/digit/" + char + ".png")
                        char_img = char_img.resize((21, 25))
                        if id == 0:
                            imgNew.paste(char_img, (id * 15 + 5, 3), char_img)
                        elif id == 1:
                            imgNew.paste(char_img, (id * 15 + 7, 3), char_img)
                        elif id == 2:
                            imgNew.paste(char_img, (id * 23, 3), char_img)
                        elif id == 3:
                            imgNew.paste(char_img, (id * 21, 3), char_img)
                    elif char == ' ':
                        pass
                    else:
                        char_img = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/font/black/letter/" + char + ".png")
                        char_img = char_img.resize((16, 22))
                        imgNew.paste(char_img, (id * 15 -40, 33), char_img)

            if state == 'california_disabled_person':
                imgNew = Image.open("../templates/california_disabled_person.png")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 39
                font = ImageFont.truetype("/home/yeleussinova/data_SSD/license_plate_generation/font/dealerplate_california.ttf", fontsize)
                draw.text((40, 28), plateStr.upper(), font=font, fill=(40,61,110,255))

            if state == 'california_disabled_person2':
                imgNew = Image.open("../templates/california_disabled_person2.png")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 40
                font = ImageFont.truetype("/home/yeleussinova/data_SSD/license_plate_generation/font/dealerplate_california.ttf", fontsize)
                draw.text((32, 28), plateStr.upper(), font=font, fill=(10, 10, 10, 255))



            img_name = str(i+start_id) + '_' + state + '.jpg'
            # txt_name_fake = plateStr + '_' + state + '_synth.txt'
            # txt_name_gan = plateStr.lower() + '_' + state + '_gan.txt'
            filename = os.path.join(outputPath, img_name)
            generated = np.array(imgNew)
            generated = cv2.cvtColor(generated, cv2.COLOR_BGR2RGB)
            if square:
                half = generated.shape[0] // 2
                top = generated[:half, :]
                bottom = generated[half:, :]
                generated = self.hconcat_resize_min([top, bottom])
            cv2.imwrite(filename, generated)
            # with open(os.path.join(annot_out_path, txt_name_fake), 'w') as f:
            #     f.writelines(plateStr)
            print(i, filename)
            with open(os.path.join(annot_out_path, img_name.replace('.jpg', '.txt')), 'w') as f:
                f.writelines(outLabel)



    def drawLabels_template(self, imageFolder, labelFolder, outputPath, state):
        if not os.path.exists(outputPath):
            os.mkdir(outputPath)

        images = os.listdir(imageFolder)
        for img_path in images:
            # try:
            f = open(os.path.join(labelFolder, img_path.replace('.png', '.txt').replace('.jpeg', '.txt')))
            label = f.readline().strip().split(',')[0]
            label = label.replace(' ', '').replace('-', '')
            if state == 'california':
                imgNew = Image.open("../templates/california.png")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 42
                font = ImageFont.truetype("../font/dealerplate_california.ttf",
                                          fontsize)
                draw.text((8, 24), label.upper(), font=font, fill=(24, 28, 81, 255))

            if state == 'texas':
                imgNew = Image.open("../templates/texas.png")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 35
                font = ImageFont.truetype("../font/Cooperative-Regular.ttf", fontsize)
                if len(label) == 7:
                    draw.text((9, 20), label.upper()[:3] + '  ' + label.upper()[3:], (0, 0, 0), font=font)
                elif len(label) == 6:
                    draw.text((17, 20), label.upper()[:2] + '   ' + label.upper()[2:], (0, 0, 0), font=font)
                else:
                    draw.text((17, 20), label.upper()[:2] + '   ' + label.upper()[2:], (0, 0, 0), font=font)

            if state == 'pensylvania':
                imgNew = Image.open("../templates/pensylvania.png")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 40
                font = ImageFont.truetype("../font/DealerplateW00Pennsylvania.ttf", fontsize)
                draw.text((10, 7), label.upper()[:3] + ' ' + label.upper()[3:], font=font, fill=(24, 28, 81, 255))

            if state == 'minnesota':
                gen = random.choice([0, 1])
                imgNew = Image.open("../templates/minnesota.jpeg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 44
                font = ImageFont.truetype("../font/DealerplateW00Wisconsin.ttf", fontsize)
                if gen:
                    color = (45,83,201,255)
                else:
                    color = (0, 0, 0, 0)
                draw.text((6, 9), label.upper()[:3] + '  ' + label.upper()[3:], font=font, fill=color)

            if state == 'minnesota_new':
                gen = random.choice([0, 1])
                imgNew = Image.open("../templates/minnesota.jpeg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 40
                font = ImageFont.truetype("../font/DINEngschriftStd.otf", fontsize)
                if gen:
                    color = (45,83,201,255)
                else:
                    color = (0, 0, 0, 0)
                draw.text((8, 25), label.upper()[:3] + '  ' + label.upper()[3:], font=font, fill=color)

            if state == 'alabama':
                imgNew = Image.open("../templates/alabama.jpg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 40
                font = ImageFont.truetype("../font/DealerplateW00Wisconsin.ttf", fontsize)
                draw.text((10, 8), label.upper(), font=font, fill=(0, 0, 0, 0))

            if state == 'arizona':
                imgNew = Image.open("../templates/arizona.jpg")
                imgNew = imgNew.resize((158, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 40
                font = ImageFont.truetype("../font/DealerplateW00Massachusetts.ttf", fontsize)
                draw.text((20, 8), label.upper(), font=font, stroke_width=0, fill=(0, 0, 0, 0))

            if state == 'florida':
                imgNew = Image.open("../templates/florida.jpg")
                imgNew = imgNew.resize((140, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 42
                font = ImageFont.truetype("../font/DealerplateW00New Jersey.ttf", fontsize)
                if len(label) == 6:
                    draw.text((7, 8), label.upper()[:3] + '    ' + label.upper()[3:], font=font, stroke_width=0, fill=(2,78,47,255))
                else:
                    draw.text((10, 8), label.upper()[:2] + '  ' + label.upper()[2:], font=font, stroke_width=0, fill=(2, 78, 47, 255))

            if state == 'kentucky':
                imgNew = Image.open("../templates/kentucky.jpg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                fontsize = 38
                font = ImageFont.truetype("../font/DealerplateW00Pennsylvania.ttf", fontsize)
                if len(label) == 6:
                    draw.text((9, 11), label.upper()[:3] + '    ' + label.upper()[3:], font=font, stroke_width=0, fill=(45,64,114,255))
                else:
                    draw.text((10, 8), label.upper()[:2] + '  ' + label.upper()[2:], font=font, stroke_width=0, fill=(45,64,114,255))

            if state == 'new_jersey':
                fontsize = 40
                font = ImageFont.truetype("../font/DealerplateW00New Jersey.ttf", fontsize)
                if len(label) == 6:
                    imgNew = Image.open("../templates/new_jersey2.jpg")
                    imgNew = imgNew.resize((128, 70))
                    draw = ImageDraw.Draw(imgNew)
                    draw.text((9, 10), label.upper()[:3] + '  ' + label.upper()[3:], font=font, stroke_width=0, fill=(0,0,0,0))
                elif len(label) == 7:
                    imgNew = Image.open("../templates/new_jersey1.jpg")
                    imgNew = imgNew.resize((128, 70))
                    draw = ImageDraw.Draw(imgNew)
                    draw.text((10, 8), label.upper(), font=font, stroke_width=0, fill=(0,0,0,0))

            if state == 'new_york':
                fontsize = 42
                font = ImageFont.truetype("../font/DealerplateW00NewYork_yellow.ttf", fontsize)
                imgNew = Image.open("../templates/new_york.png")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                draw.text((12, 7), label.upper()[:3] + '    ' + label.upper()[3:], font=font, stroke_width=0,
                          fill=(3,25,57,255))

            if state == 'new_york_yellow':
                fontsize = 40
                font = ImageFont.truetype("../font/DealerplateW00NewYork_yellow.ttf", fontsize)
                if len(label) == 7:
                    imgNew = Image.open("../templates/new_york_yellow.jpg")
                    imgNew = imgNew.resize((128, 70))
                    draw = ImageDraw.Draw(imgNew)
                    draw.text((14, 10), label.upper()[:3] + '  ' + label.upper()[3:], font=font, stroke_width=0, fill=(0,0,0,0))
                elif len(label) == 5:
                    imgNew = Image.open("../templates/new_york2.jpg")
                    imgNew = imgNew.resize((128, 70))
                    draw = ImageDraw.Draw(imgNew)
                    draw.text((32, 10), label.upper(), font=font, stroke_width=0, fill=(0,0,0,0))
                else:
                    imgNew = Image.open("../templates/new_york2.jpg")
                    imgNew = imgNew.resize((128, 70))
                    draw = ImageDraw.Draw(imgNew)
                    draw.text((10, 10), label.upper(), font=font, stroke_width=0, fill=(0, 0, 0, 0))

            if state == 'new_york_white':
                fontsize = 40
                font = ImageFont.truetype("../font/DealerplateW00NewYork_yellow.ttf", fontsize)
                if len(label) == 7:
                    s = 0
                    p = 0
                    for x in label.upper():
                        if x in string.ascii_uppercase:
                            s += 1
                            P = p
                        else:
                            p += 1
                            S = s
                    if S == 3:
                        imgNew = Image.open("../templates/new_york_white.jpg")
                        imgNew = imgNew.resize((128, 70))
                        draw = ImageDraw.Draw(imgNew)
                        draw.text((13, 10), label.upper()[:3] + '  ' + label.upper()[3:], font=font, stroke_width=0, fill=(49,48,84,255))
                    if P == 5:
                        imgNew = Image.open("../templates/new_york_white1.jpg")
                        imgNew = imgNew.resize((128, 70))
                        draw = ImageDraw.Draw(imgNew)
                        draw.text((13, 10), label.upper()[:5] + '  ' + label.upper()[5:], font=font, stroke_width=0, fill=(49, 48, 84, 255))
                    if P == 2:
                        imgNew = Image.open("../templates/new_york_white2.jpg")
                        imgNew = imgNew.resize((128, 70))
                        draw = ImageDraw.Draw(imgNew)
                        draw.text((13, 10), label.upper()[:2] + '  ' + label.upper()[2:], font=font, stroke_width=0, fill=(49, 48, 84, 255))
                elif len(label) == 4:
                    imgNew = Image.open("../templates/new_york_white2.jpg")
                    imgNew = imgNew.resize((128, 70))
                    draw = ImageDraw.Draw(imgNew)
                    draw.text((34, 10), label.upper()[:3] + '  ' + label.upper()[3:], font=font, stroke_width=0, fill=(49,48,84,255))
                else:
                    imgNew = Image.open("../templates/new_york_white2.jpg")
                    imgNew = imgNew.resize((128, 70))
                    draw = ImageDraw.Draw(imgNew)
                    draw.text((10, 10), label.upper(), font=font, stroke_width=0, fill=(49,48,84,255))

            if state == 'massachusetts':
                fontsize = 39
                font = ImageFont.truetype("../font/DealerplateW00Massachusetts.ttf", fontsize)
                imgNew = Image.open("../templates/massachusetts.png")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                if len(label) == 6:
                    s = 0
                    for x in label.upper():
                        if x in string.ascii_uppercase:
                            s += 1
                    if s == 6:
                        draw.text((10, 10), label.upper(), font=font, stroke_width=0, fill=(185,46,47,255))
                    else:
                        draw.text((7, 10), label.upper()[:3] + ' ' + label.upper()[3:], font=font, stroke_width=0,
                                  fill=(185, 46, 47, 255))
                elif len(label) == 5:
                    draw.text((16, 10), label.upper(), font=font, stroke_width=0,
                              fill=(185, 46, 47, 255))
                else:
                    draw.text((30, 10), label.upper(), font=font, stroke_width=0,
                              fill=(185, 46, 47, 255))

            if state == 'maryland':
                fontsize = 42
                font = ImageFont.truetype("../font/DealerplateW05Maryland.ttf", fontsize)
                imgNew = Image.open("../templates/maryland.jpg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                if len(label) == 6:
                    draw.text((8, 7), label.upper()[:3] + '  ' + label.upper()[3:], font=font, stroke_width=0, fill=(0,0,0,0))

            if state == 'texas_war':
                fontsize = 35
                font = ImageFont.truetype("../font/BwStretch-Medium.otf", fontsize)
                imgNew = Image.open("../templates/texas_war.jpg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                draw.text((10, 15), label.upper()[:3] + '  ' + label.upper()[3:], font=font, stroke_width=0,
                              fill=(0, 0, 0, 0))

            if state == 'texas_horse':
                fontsize = 35
                font = ImageFont.truetype("../font/dealerplate_california.ttf", fontsize)
                imgNew = Image.open("../templates/texas_horse.jpg")
                imgNew = imgNew.resize((100, 60))
                draw = ImageDraw.Draw(imgNew)
                draw.text((5, 17), label.upper()[:3] + '  ' + label.upper()[3:], font=font, stroke_width=0,
                              fill=(4,31,77,255))

            if state == 'michigan':
                fontsize = 40
                font = ImageFont.truetype("../font/DealerplateW00Michigan.ttf", fontsize)
                imgNew = Image.open("../templates/michigan.jpeg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                draw.text((5, 9), label.upper()[:3] + '  ' + label.upper()[3:], font=font, stroke_width=0,
                              fill=(17,50,99,255))

            if state == 'missisippi':
                fontsize = 35
                font = ImageFont.truetype("../font/DealerplateW00Pennsylvania.ttf", fontsize)
                imgNew = Image.open("../templates/missisippi.jpeg")
                imgNew = imgNew.resize((125, 60))
                draw = ImageDraw.Draw(imgNew)
                draw.text((10, 9), label.upper()[:3] + '    ' + label.upper()[3:], font=font, stroke_width=0,
                              fill=(8,13,56,255))

            if state == 'ohio':
                fontsize = 39
                font = ImageFont.truetype("../font/DealerplateW00Ohio.ttf", fontsize)
                imgNew = Image.open("../templates/ohio.png")
                imgNew = imgNew.resize((125, 70))
                draw = ImageDraw.Draw(imgNew)
                s = 0
                for l in label.upper():
                    if l in string.ascii_uppercase:
                        s += 1
                if s == 5:
                    draw.text((12, 12), label.upper()[:5] + ' ' + label.upper()[5:], font=font, stroke_width=0,
                              fill=(8,13,56,255))
                else:
                    draw.text((6, 12), label.upper()[:3] + ' ' + label.upper()[3:], font=font, stroke_width=0,
                              fill=(8, 13, 56, 255))

            if state == 'virginia':
                fontsize = 40
                font = ImageFont.truetype("../font/DealerplateW00Virginia.ttf", fontsize)
                imgNew = Image.open("../templates/virginia.png")
                imgNew = imgNew.resize((125, 70))
                draw = ImageDraw.Draw(imgNew)
                draw.text((8, 12), label.upper(), font=font, stroke_width=0,
                              fill=(0,21,73,255))

            if state == 'colorado':
                fontsize = 38
                font = ImageFont.truetype("../font/DealerplateW00Michigan.ttf", fontsize)
                imgNew = Image.open("../templates/colorado.png")
                imgNew = imgNew.resize((125, 70))
                draw = ImageDraw.Draw(imgNew)
                draw.text((8, 12), label.upper()[:3] + ' - ' + label.upper()[3:], font=font, stroke_width=0,
                              fill=(1,63,49,255))

            if state == 'wisconsin':
                fontsize = 38
                font = ImageFont.truetype("../font/DealerplateW00Wisconsin.ttf", fontsize)
                imgNew = Image.open("../templates/wisconsin.jpg")
                imgNew = imgNew.resize((125, 70))
                draw = ImageDraw.Draw(imgNew)
                if len(label) ==3:
                    draw.text((35, 9), label.upper(), font=font, stroke_width=0, fill=(174,46,61,255))
                elif len(label) ==4:
                    draw.text((27, 9), label.upper(), font=font, stroke_width=0, fill=(174,46,61,255))
                elif len(label) ==5:
                    draw.text((20, 9), label.upper(), font=font, stroke_width=0, fill=(174,46,61,255))
                elif len(label) ==6:
                    draw.text((16, 9), label.upper(), font=font, stroke_width=0, fill=(174,46,61,255))
                else:
                    draw.text((11, 9), label.upper(), font=font, stroke_width=0, fill=(174,46,61,255))

            if state == 'wisconsin_white':
                fontsize = 38
                font = ImageFont.truetype("../font/DealerplateW00Wisconsin.ttf", fontsize)
                imgNew = Image.open("../templates/wisconsin_white.jpeg")
                imgNew = imgNew.resize((125, 70))
                draw = ImageDraw.Draw(imgNew)
                draw.text((10, 15), label.upper()[:3] + ' - ' + label.upper()[3:], font=font, stroke_width=0, fill=(0,0,0,0))

            if state == 'tennessee':
                fontsize = 42
                font = ImageFont.truetype("../font/DealerplateW00Wisconsin.ttf", fontsize)
                imgNew = Image.open("../templates/tennessee.jpeg")
                imgNew = imgNew.resize((128, 70))
                draw = ImageDraw.Draw(imgNew)
                draw.text((6, 8), label.upper()[:3] + '   ' + label.upper()[3:], font=font, stroke_width=0, fill=(0,0,0,0))

            if state == 'oregon_new':
                fontsize = 38
                font = ImageFont.truetype("../font/DealerplateW00New Jersey.ttf", fontsize)
                imgNew = Image.open("../templates/oregon.jpeg")
                imgNew = imgNew.resize((125, 65))
                draw = ImageDraw.Draw(imgNew)
                draw.text((7,5), label.upper()[:3] + '   ' + label.upper()[3:], font=font, stroke_width=0, fill=(33,48,96,255))

            if state == 'connecticut':
                fontsize = 38
                font = ImageFont.truetype("../font/DealerplateW05Maryland.ttf", fontsize)
                imgNew = Image.open("../templates/connecticut.jpeg")
                imgNew = imgNew.resize((125, 70))
                draw = ImageDraw.Draw(imgNew)
                draw.text((14,8), label.upper()[:3] + ' ' + label.upper()[3:], font=font, stroke_width=0, fill=(33,48,96,255))

            if state == 'mongolia_type0':
                imgNew = Image.new("RGB", (146, 36), (255, 255, 255))
                # draw = ImageDraw.Draw(imgNew)
                label = ' ' + label[:4] + ' ' + label[4:]
                print(label)
                for id, char in enumerate(label):
                    if char == 'a':
                        char = 'а'
                    elif char =='h':
                        char = 'н'
                    elif char == "y":
                        char = "у"

                    if char in string.digits:
                        char_img = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/font/black/digits/" + char + ".png")
                        char_img = char_img.resize((21, 35))
                        imgNew.paste(char_img, (id * 15, 1), char_img)
                    elif char == ' ':
                        pass
                    else:
                        char_img = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/font/black/letters/" + char + ".png")
                        char_img = char_img.resize((23, 43))
                        imgNew.paste(char_img, (id * 15, -2), char_img)

            if state == 'mongolia_type1':
                imgNew = Image.new("RGB", (160, 36), (255, 255, 255))
                # draw = ImageDraw.Draw(imgNew)
                first = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/plates/soembo.png")
                second = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/plates/mng.png")
                imgNew.paste(first, (0, 0), first)
                imgNew.paste(second, (80, 7), second)
                label = ' ' + label[:4] + '  ' + label[4:]

                print(label)
                for id, char in enumerate(label):
                    if char == 'a':
                        char = 'а'
                    elif char =='h':
                        char = 'н'
                    elif char == "y":
                        char = "у"
                    elif char == "m":
                        char = "м"

                    if char in string.digits:
                        char_img = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/font/black/digits/" + char + ".png")
                        char_img = char_img.resize((21, 35))
                        if id == 1:
                            imgNew.paste(char_img, (id * 17, 1), char_img)
                        else:
                            imgNew.paste(char_img, (id * 15, 1), char_img)
                    elif char == ' ':
                        pass
                    else:
                        char_img = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/font/black/letters/" + char + ".png")
                        char_img = char_img.resize((23, 43))
                        imgNew.paste(char_img, (id * 15, -2), char_img)

            if state == 'squared_type1':
                imgNew = Image.new("RGB", (88, 60), (255, 255, 255))
                # draw = ImageDraw.Draw(imgNew)
                print(label)
                for id, char in enumerate(label):
                    if char == 'a':
                        char = 'а'
                    elif char =='h':
                        char = 'н'
                    elif char == "y":
                        char = "у"
                    elif char == "m":
                        char = "м"
                    elif char == "m":
                        char = "м"

                    if char in string.digits:
                        char_img = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/font/black/digit/" + char + ".png")
                        char_img = char_img.resize((21, 25))
                        if id == 0:
                            imgNew.paste(char_img, (id * 15 + 5, 3), char_img)
                        elif id == 1:
                            imgNew.paste(char_img, (id * 15 + 7, 3), char_img)
                        elif id == 2:
                            imgNew.paste(char_img, (id * 23, 3), char_img)
                        elif id == 3:
                            imgNew.paste(char_img, (id * 21, 3), char_img)
                    elif char == ' ':
                        pass
                    else:
                        char_img = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/font/black/letter/" + char + ".png")
                        char_img = char_img.resize((16, 22))
                        imgNew.paste(char_img, (id * 15 -40, 33), char_img)

            if state == 'squared_type3':
                imgNew = Image.new("RGB", (88, 60), (255, 255, 255))
                # draw = ImageDraw.Draw(imgNew)
                first = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/plates/soembo.png").resize((15,26))
                second = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/plates/mng.png").resize((24,18))
                imgNew.paste(first, (5, 29), first)
                imgNew.paste(second, (61, 35), second)
                label1 = ' ' + label[:4]
                label2 = ' ' + label[4:]
                print(label)
                for id, char in enumerate(label):
                    if char == 'a':
                        char = 'а'
                    elif char =='h':
                        char = 'н'
                    elif char == "y":
                        char = "у"
                    elif char == "m":
                        char = "м"
                    elif char == "m":
                        char = "м"

                    if char in string.digits:
                        char_img = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/font/black/digit/" + char + ".png")
                        char_img = char_img.resize((21, 25))
                        if id == 0:
                            imgNew.paste(char_img, (id * 15 + 5, 3), char_img)
                        elif id == 1:
                            imgNew.paste(char_img, (id * 15 + 7, 3), char_img)
                        elif id == 2:
                            imgNew.paste(char_img, (id * 23, 3), char_img)
                        elif id == 3:
                            imgNew.paste(char_img, (id * 21, 3), char_img)
                    elif char == ' ':
                        pass
                    else:
                        char_img = Image.open("/home/yeleussinova/data_SSD/mongolia/mn/font/black/letter/" + char + ".png")
                        char_img = char_img.resize((16, 22))
                        imgNew.paste(char_img, (id * 15 - 40, 33), char_img)


if __name__ == '__main__':
    # G = GenPlate("../font/platech.ttf", '../font/platechar.ttf')
    G = GenPlate()

    # G.genBatch(10,2,range(31,65),"/home/yeleussinova/data_SSD/generate_LP/GeneratedPlateSamples",(272,72))

    state = 'uae_20'

    ann_out_path = "/home/arman/data_1TB/uae/generated/uae_20"
    synth_out_path = "/home/arman/data_1TB/uae/generated/uae_20"
    G.generate_img(count=1, start_id=1, outputPath=synth_out_path, annot_out_path=ann_out_path, state=state)

    # image_folder = "/home/yeleussinova/data_SSD/mongolia/plates/squared/images/" + state
    # label_folder = "/home/yeleussinova/data_SSD/mongolia/plates/squared/labels"
    # output_path = "/home/yeleussinova/data_SSD/mongolia/plates/gan_images/" + state + "_fake"

    # G.drawLabels_template(image_folder, label_folder, output_path, state)

