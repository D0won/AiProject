from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
import torch
from PIL import Image
import model as m
import cv2
import serial
import time

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# 기본 페이지 : 웹브라우저에서 카메라 영상 확인
@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# MNIST 모델 로드
model = m.CNN()
model.load_state_dict(torch.load('mnist_model.pth', map_location=torch.device('mps')))
model.eval()

# 전역 변수로 예측 결과 저장
prediction_result = {"prediction": None}

# 웹캠에서 프레임을 캡처하고 예측하는 함수
def capture_and_predict(frame):
    global prediction_result
    # 프레임을 PIL 이미지로 변환
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)).convert('L')
    
    # 이미지를 모델 입력 형식에 맞게 전처리
    preprocess = m.transforms.Compose([
        m.transforms.Grayscale(num_output_channels=1),
        m.transforms.Resize((28, 28)),
        m.transforms.ToTensor(),
    ])
    image_tensor = preprocess(image).unsqueeze(0)
    
    # 모델을 사용하여 예측 수행
    with torch.no_grad():
        output = model(image_tensor)
        prediction = torch.argmax(output, dim=1).item()
    
    prediction_result = {"prediction": prediction}
    # 예측된 숫자를 아두이노로 전송
    # sendArduino(prediction)
    
# def sendArduino(prediction) :
#     arduino = serial.Serial('/dev/tty.usbserial-120', 9600)

#     if arduino.is_open :
#         print("시리얼 포트가 열려있습니다.")

#     else :
#         print("시리얼 포트를 열 수 없습니다.")
#     time.sleep(2)

#     arduino_num = str(prediction) + '\n'
#     arduino.write(arduino_num.encode())
#     arduino.close() 
    
# 예측 결과를 반환하는 엔드포인트
@app.get("/prediction")
async def get_prediction():
    return JSONResponse(content=prediction_result)

# 웹캠에서 프레임을 스트리밍하는 엔드포인트
@app.get("/video_feed")
async def video_feed():
    def generate_frames():
        camera = cv2.VideoCapture(0)
        while True:
            success, frame = camera.read()
            if not success:
                break
            else:
                # 프레임을 캡처하고 예측 수행
                capture_and_predict(frame)
                
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                
                time.sleep(1/60)
        camera.release()
    
    return StreamingResponse(generate_frames(), media_type="multipart/x-mixed-replace; boundary=frame")