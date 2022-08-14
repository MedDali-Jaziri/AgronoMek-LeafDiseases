from fastapi import FastAPI, File, UploadFile, Request
from fastapi.staticfiles import StaticFiles
import uvicorn
from BackHard import *
from fastapi.middleware.cors import CORSMiddleware
import pyqrcode
from PIL import Image
import jwt

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return 'Hello in our planted disease detector by Xenophon-IT !!'
    # return {"message": "Hello World"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    image = read_file_as_image(await file.read())

    # print(image)
    img_batch = np.expand_dims(image, 0)
    
    prediction = Model.predict(img_batch)

    # print("Predicition")
    # print(CLASS_NAMES[prediction[0]])

    predicted_class = CLASS_NAMES[np.argmax(prediction[0])]
    confidence = np.max(prediction[0])

    print(predicted_class)
    print(float(confidence))

    # if(confidence>=0.9999):
    #     return {
    #         'class': predicted_class,
    #         'confidence': float(confidence)
    #     }
    # else:
    #     return{
    #         'class': "كيفاش إتحبني نعرفها علمني علني سيدي سيدي",
    #         'confidence': float(confidence)
    #     }

    return  {
            "class": predicted_class,
            "confidence": float(confidence)
        }

#This request post for get all the informations of companys user
@app.post("/QRCodeGenerator")
async def qrCodeGenerator(request: Request):
    req = await request.json()
    lop = req['lop']
    latitude = req['latitude']
    longitude = req['longitude']
    
    data = {
    "Id_AgronoMek": lop,
    "Longtitude": latitude,
    "Latitude" : longitude
    }
    encoded_jwt = jwt.encode(data, "AgronoMek-XenophonIT", algorithm="HS256").decode("utf-8")
    url = pyqrcode.QRCode(encoded_jwt,error = 'H')
    url.png("static/"+lop+".png",scale=10)
    im = Image.open("static/"+lop+".png")
    im = im.convert("RGBA")
    logo = Image.open('AgronoMek-Logo.png')
    box = (135,135,235,235)
    im.crop(box)
    region = logo
    region = region.resize((box[2] - box[0], box[3] - box[1]))
    im.paste(region,box)
    im.save("static/"+lop+".png")
    
    # return FileResponse('Images\Agro-01.png')
    return {
        "message" : "http://localhost:5050/static/"+lop+".png",
        "nameGreenHouse": lop
    }

# run the application
if __name__ == "__main__":
    uvicorn.run(app, host='localhost',port=5050)