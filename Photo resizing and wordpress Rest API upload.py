#This code works in Google's Colab and should work on Linux machines. 
#Using Colab and Google Drive, the code searches a folder for jpg images, resizes those images, and uploads them to a selected wordpress site. 
#It is super useful if you have lots of large images to upload and don't want to handle them individually. 
from google.colab import drive
drive.mount('/content/drive')
!CC="cc -mavx2" pip install -U --force-reinstall pillow-simd
import PIL
from PIL import Image
import glob
import os

import requests 
import json
import base64

url = 'https://myurl.com/wp-json/wp/v2'
user = 'my username'
password = 'my-password'
creds = user + ":" + password
token = base64.b64encode(creds.encode())

inputFolder = '/content/drive/My Drive/WebPics/Uploads/'
archiveFolder = '/content/drive/My Drive/WebPics/Archive/'
outputFolder = '/content/drive/My Drive/WebPics/Final/'

#os.mkdir('/content/drive/My Drive/WebPics/Final/')
i = 0
for img in glob.glob(inputFolder + "/*.*"): #pulls images from Uploads folder and resizes them
  image = Image.open(img)
  image.save('/content/drive/My Drive/WebPics/Archive/image6.6.2022.2.%04i.JPG' %i, optimize = True, quality = 100) #Change Date every time, or change name entirely
  print(image.format, image.size, image.mode)
  new_image_width = image.size[0]
  new_image_height = image.size[1] 
  print(new_image_height)
  print(new_image_width)
  aspect_ratio =  new_image_height / new_image_width 
  print(aspect_ratio)
  if new_image_width > new_image_height:
    new_image_width = 1200
    new_image_height = int((new_image_width * image.size[1]) / image.size[0]) 
  else:
    new_image_width = 800
    new_image_height = int((new_image_width * image.size[1]) / image.size[0])
  print(new_image_width, new_image_height)
  #imgResized = image
  imgResized = image.resize((new_image_width, new_image_height), resample = 1)
  imgResized.save("/content/drive/My Drive/WebPics/Final/image6.6.2022.2.%04i.JPG" %i, optimize = True, quality = 70) #Saves images into Final folder - Make sure to change the 
  i +=1
  print(imgResized.format, imgResized.size, imgResized.mode)
for img in glob.glob(outputFolder + "/*.JPG"): 
  header = {'Authorization': 'Basic ' + token.decode('utf-8')}
  #print(img)
  media = {
    'file': open(img, 'rb'),
    'caption': 'This is the universal image caption.',
    'description': 'This is the universal image description.' 
  }
  print(media)
  image = requests.post(url + '/media', headers = header, files = media)
  imageURL = str(json.loads(image.content)['source_url'])
