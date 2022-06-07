#This program takes a square png or jpg and converts it into a QR code.
#For a complete explanation of how to use it go to https://thealmoner.com/fundraising-qr-codes/
!pip install amzqr
from PIL import Image
from google.colab import drive
drive.mount('/content/drive')

#note, line 8 is a command line instruction run through the Colab interface. 

!amzqr https://goldenharvest.org/donate/ -n /content/drive/MyDrive/QRcode/MainDonateQR.png -p /content/drive/MyDrive/QRcode/Icon_Green_Background.png -c  
