import pyqrcode
from PIL import Image
import jwt

data = {
    "Id_AgronoMek": "Agro-05",
    "Longtitude": 10.81947,
    "Latitude" : 35.76264
}
encoded_jwt = jwt.encode(data, "AgronoMek-XenophonIT", algorithm="HS256").decode("utf-8")

url = pyqrcode.QRCode(encoded_jwt,error = 'H')
url.png('Agro-05.png',scale=10)
im = Image.open('Agro-05.png')
im = im.convert("RGBA")
logo = Image.open('AgronoMek-Logo.png')
box = (135,135,235,235)
im.crop(box)
region = logo
region = region.resize((box[2] - box[0], box[3] - box[1]))
im.paste(region,box)
im.save("Agro-05.png")
im.show()
