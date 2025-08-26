# 0번 카메라 테스트

from flask import Flask, render_template, Response, request, redirect, url_for
import cv2
import os
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import torch
import torch.nn.functional as F
from ultralytics import YOLO
from flask_cors import CORS  # 🔹 추가

app = Flask(__name__)
CORS(app)  # 🔹 모든 도메인 허용
# 캠 0: 얼굴 인증용
camera = cv2.VideoCapture(0)

# 얼굴 인증 시 저장 (예시)
verified_users = []  # 전역 리스트 또는 Redis, DB 사용

# def refresh():
    # db에서 인증한 사람 받아서 보여줘야됨
    

def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            


@app.route('/')
def index():
    # return render_template('index.html')  # HTML 템플릿 렌더링
    return render_template('index.html', verified_users=verified_users)

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/users', methods=['GET'])
def get_users():
    print("보내기",verified_users)
    return verified_users

@app.route('/verify', methods=['POST'])
def verify():
    mtcnn = MTCNN(image_size=160, margin=0)
    model = InceptionResnetV1(pretrained='vggface2').eval()
    
    success, frame = camera.read()
    if not success:
        print("웹캠 캡처 실패")
        return redirect(url_for('fail'))

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    captured_image = Image.fromarray(frame_rgb)
    face2 = mtcnn(captured_image)

    if face2 is None:
        print("❌ 얼굴 인식 실패 (캡처)")
        return redirect(url_for('fail'))

    embedding2 = model(face2.unsqueeze(0))

    # ✅ 이미지 폴더에서 모든 등록 이미지 확인
    image_folder = 'images'
    for filename in os.listdir(image_folder):
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            try:
                img_path = os.path.join(image_folder, filename)
                img = Image.open(img_path)
                face1 = mtcnn(img)

                if face1 is None:
                    print(f"⚠️ 얼굴 인식 실패: {filename}")
                    continue

                embedding1 = model(face1.unsqueeze(0))
                similarity = F.cosine_similarity(embedding1, embedding2)
                print(f"{filename} 유사도: {similarity.item():.4f}")
                
                # name = filename.replace(",jpg","")
                name = filename.rsplit(".", 1)[0]

                if similarity.item() >= 0.7:
                    print("✅ 인증 성공")
                    # verified_users["name"] = name
                    verified_users.append(name)
                    # verified_users.append({
                    #     "name" : f"{name}"
                    # })
                    # print(verified_users)
                    # return redirect(url_for('success'))
                    return redirect(url_for('success', name=name))

            except Exception as e:
                print(f"오류 발생: {filename} - {e}")
                continue

    print("❌ 모든 이미지와 불일치 - 인증 실패")
    return redirect(url_for('fail'))



@app.route('/success')
def success():
    # return result_page("인증 성공", "✅ 입장하세요!")
    name = request.args.get('name')
    return result_page("인증 성공", f"✅ {name}님, 입장하세요!")

@app.route('/fail')
def fail():
    return result_page("인증 실패", "❌ 금일 근무자가 아닙니다!")
    
def result_page(title, message):
    return f"""
    <html>
    <head>
        <title>{title}</title>
        <script>
            let countdown = 5;
            function updateCountdown() {{
                document.getElementById('countdown').innerText = countdown;
                countdown--;
                if (countdown < 0) {{
                    window.location.href = "/";
                }} else {{
                    setTimeout(updateCountdown, 1000);
                }}
            }}
            window.onload = updateCountdown;
        </script>
    </head>
    <body>
        <h2>{message}</h2>
        <p><span id="countdown"></span>초 후 홈으로 돌아갑니다.</p>
    </body>
    </html>
    """

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
    

# uvicorn serverTest2:app --host 0.0.0.0 --port 5000 --reload

# python serverTest2.py