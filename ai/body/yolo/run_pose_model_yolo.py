from flask import Flask, render_template, Response, request
import cv2
import numpy as np
from collections import deque
import joblib
from get_pose_landmark_yolo import get_yolo_landmarks_from_image, initialize_yolo_model
from ultralytics import YOLO
from typing import List
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# XGBoost 모델을 로드하는 함수
def load_pose_model(model_path: str):
    try:
        print(f"XGBoost 모델을 로드합니다... (경로: {model_path})")
        model = joblib.load(model_path)
        print("모델 로드 완료!")
        return model
    except Exception as e:
        print(f"모델 로딩 중 오류가 발생했습니다: {e}")
        return None

# 포즈 예측 함수
def predict_pose(model, landmarks: List) -> int:
    try:
        if len(landmarks) != 17:
            print(f"오류: 랜드마크 개수가 17개가 아닙니다 (현재: {len(landmarks)}개).")
            return -1
        feature_vector = np.array(landmarks).flatten()
        feature_vector_2d = feature_vector.reshape(1, -1)
        prediction = model.predict(feature_vector_2d)
        return prediction[0]
    except Exception as e:
        print(f"예측 중 오류 발생: {e}")
        return -1

# 넘어짐 상태 감지 함수
def run(fall_classifier_model, landmark_data: List) -> bool:
    FALLEN_CLASS_ID = 1
    if not landmark_data:
        return False
    for person_landmarks in landmark_data:
        predicted_class = predict_pose(fall_classifier_model, person_landmarks)
        if predicted_class == -1:
            continue
        if predicted_class == FALLEN_CLASS_ID:
            return True
    return False

# 비디오 스트리밍 처리
def process_video():
    cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("🚨 오류: 웹캠을 열 수 없습니다.")
        return
    
    classifier_model_path = 'yolo/xgb_yolo_model.joblib'
    pose_detector = initialize_yolo_model()
    fall_classifier = load_pose_model(classifier_model_path)

    if not all([pose_detector, fall_classifier]):
        print("⛔️ 모델 초기화에 실패하여 프로그램을 종료합니다.")
        return

    WINDOW_SIZE = 150  # 최근 150개 프레임을 기억
    FALL_THRESHOLD_RATIO = 0.9  # 윈도우의 70% 이상이 '넘어짐'일 때 최종 판단
    FALL_THRESHOLD = int(WINDOW_SIZE * FALL_THRESHOLD_RATIO)
    detection_history = deque(maxlen=WINDOW_SIZE)
    is_fall_confirmed = False  # 최종 넘어짐 판단 상태

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # 1. YOLO 모델로 포즈 추정
        results = pose_detector(frame, verbose=False, conf=0.7)
        annotated_frame = results[0].plot()

        # 2. 랜드마크 데이터 추출
        landmark_data = []
        if results[0].keypoints and len(results[0].keypoints.xy) > 0:
            for kps in results[0].keypoints:
                person_landmarks = []
                coords = kps.xyn[0]
                confs = kps.conf[0]
                for i in range(len(coords)):
                    person_landmarks.append((coords[i][0].item(), coords[i][1].item(), confs[i].item()))
                landmark_data.append(person_landmarks)

        # 3. 현재 프레임의 넘어짐 여부 판단
        is_fallen_current_frame = run(fall_classifier, landmark_data)

        # 4. 현재 프레임의 결과를 detection_history에 추가
        detection_history.append(is_fallen_current_frame)

        # 5. 윈도우 내 '넘어짐' 탐지 횟수 계산
        fall_count_in_window = sum(detection_history)

        # 6. 최종 넘어짐 상태 판단
        if fall_count_in_window >= FALL_THRESHOLD:
            is_fall_confirmed = True
            print(f"넘어짐 감지! (최근 {WINDOW_SIZE}개 프레임 중 {fall_count_in_window}번 감지)")
        elif fall_count_in_window == 0:
            is_fall_confirmed = False
        
        # 7. 최종 판단 결과에 따라 텍스트 표시
        if is_fall_confirmed:
            cv2.putText(annotated_frame, "FALL DETECTED", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)

        # 8. 결과를 화면에 보여주기
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    return render_template('pose.html')

@app.route('/video_feed')
def video_feed():
    return Response(process_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/save_users', methods=['POST'])
def save_users():
    global userd
    data = request.json
    userd = data.get('users', [])
    return {"message": "User list updated."}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
