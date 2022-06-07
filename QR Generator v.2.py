#This is a different way to create a standard QR code. 

!pip install QRCode

# Importing library
import qrcode
  
# Data to encode
data = "https://url.com"
  
# Creating an instance of QRCode class
qr = qrcode.QRCode(version = 1,
                   box_size = 10,
                   border = 5)
  
# Adding data to the instance 'qr'
qr.add_data(data)
  
qr.make(fit = True)
img = qr.make_image(fill_color = 'red',
                    back_color = 'white')
  
img.save('QRname.png')
