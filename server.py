from fastapi import FastAPI, File, UploadFile
import uvicorn
from BackHard import *
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
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

# run the application
if __name__ == "__main__":
    uvicorn.run(app, host='localhost',port=5050)