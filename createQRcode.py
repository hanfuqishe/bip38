#__author__ = 'pete'

from bip38 import *
from bitcoin import *
from qrcode import *
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

def createQRcode(Address, PrivKey, SaveAsFile, BIP38=False):

    qrKey = QRCode(box_size=8, border=3,error_correction=ERROR_CORRECT_Q)
    qrKey.add_data(PrivKey)
    imKey = qrKey.make_image()
    imKey_w, imKey_h = imKey.size

    qrAddr = QRCode(box_size=8, border=3,error_correction=ERROR_CORRECT_M)     #create a 2nd instance to play with sizes..
    qrAddr.add_data(Address)
    imAddr = qrAddr.make_image()
    imAddr_w, imAddr_h = imAddr.size

    img = Image.open("star_field.jpg")              #background of paper wallet
    img_w, img_h = img.size

    over_w = img_w - (imAddr_w + imKey_w)
    offs = over_w / 4

    offsetKey = (580, 130)
    #offsetAddr = ((img_w /2) - imAddr_w, (img_h - imAddr_h) / 2)
    offsetAddr = (offs, (img_h - imAddr_h) / 2)

    img.paste(imKey, offsetKey)   #paste the QR's into the background image..
    img.paste(imAddr,offsetAddr)

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("DejaVuSans.ttf",14)                        #print text above and below the QR's..
    #font = ImageFont.truetype("Arial Bold.ttf",22)
    if BIP38:
        text='BIP38 encrypted:  '+ PrivKey
    else:
        text=PrivKey
    draw.text((offs, 60), 'Address:  '+ Address, (255,255,255),font)
    width, height = draw.textsize(text, font)
    draw.text((img_w - width -offs,img_h - 60),text,(255,255,255),font)

    img.save(SaveAsFile)
