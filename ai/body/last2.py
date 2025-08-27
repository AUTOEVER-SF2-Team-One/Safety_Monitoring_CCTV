import sys
sys.path.append('c:\\users\\한국전파진흥협회\\appdata\\local\\packages\\pythonsoftwarefoundation.python.3.11_qbz5n2kfra8p0\\localcache\\local-packages\\python311\\site-packages')

from datetime import datetime
from flask import Flask, render_template, Response, request
import pymysql
from flask_cors import CORS
import cv2
import numpy as np
from ultralytics import YOLO
from flask_socketio import SocketIO, emit
from sort.sort import Sort  # SORT 알고리즘 사용
from PIL import Image, ImageDraw, ImageFont
from yolo.get_pose_landmark_yolo import get_yolo_landmarks_from_image, initialize_yolo_model
from collections import deque
import joblib
from typing import List
import time  # 시간 측정용
import winsound
import os

trr = [0, 0, 0, 0]
# Flask 애플리케이션 생성
app = Flask(__name__)
CORS(app)  # CORS 허용 (크로스 도메인 요청 허용)
socketio = SocketIO(app)  # Flask와 함께 SocketIO 객체 생성

font_path = "C:\\Users\\한국전파진흥협회\\Desktop\\java\\새 폴더 (2)\\Safety_Monitoring_CCTV-main\\Safety_Monitoring_CCTV-main\\body\\NanumGothic.ttf"  # 폰트 파일 경로 (서버에 해당 폰트가 있어야 함)
font = ImageFont.truetype(font_path, 20)  # 폰트 크기 20으로 설정
#db계정 연결
db = pymysql.connect(host='127.0.0.1', user='root', password='root', db='pleaseworkcompany', charset='utf8')
cursor = db.cursor()

#global
# hat_count = 0
no_hat_count = {}
previous_hat_status = {}
dic_hat_status = {}
no_hat_start_time = {}
hat_status = "No Hat"
danger_start_time = 0
fall_start_time = 0

#사각형 바닥의 중앙 좌표 뽑기
def box_base_center(box): 
    x1, y1, x2, y2 = box   # 객체 추적된 (사람,지게차) 좌표
    cx = (x1 + x2) // 2    # x축 중앙 (사각형의 가로 중심)
    cy = y2                # y축 하단 좌표 (바닥)
    return np.array([cx, cy]) # 사각형의 바닥 중앙 좌표

# - 두 점 사이의 유클리드 거리(직선 거리)를 계산
def euclidean_distance(p1, p2):
    return np.linalg.norm(p1 - p2) # 두 점 간 거리 계산
# 모자 착용 유무 판단
def is_hat_in_person(person_box, hat_box, threshold=0.5):
    px1, py1, px2, py2 = person_box
    hx1, hy1, hx2, hy2 = hat_box
    trr[0] = hx1
    trr[1] = hy1
    trr[2] = hx2
    trr[3] = hy2
    # 모자 박스 아래쪽(y2)이 사람 박스 위쪽(y1)보다 너무 아래에 있으면 False
    person_height = py2 - py1
    if hy2 > py1 + person_height * 0.3:
        return False

    inter_x1 = max(px1, hx1)
    inter_y1 = max(py1, hy1)
    inter_x2 = min(px2, hx2)
    inter_y2 = min(py2, hy2)
    # 사람 박스와 모자 박스 사이의 겹치는 영역
    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)
    # 모자 영역
    hat_area = (hx2 - hx1) * (hy2 - hy1)
    if hat_area == 0:
        return False

    # 겹침 비율과 임계값에 따라 모자 착용 유무 판단
    ratio = inter_area / hat_area
    return ratio > threshold

# 모델 불러오기
person_model = YOLO('C:\\Users\\한국전파진흥협회\\Desktop\\java\\새 폴더 (2)\\Safety_Monitoring_CCTV-main\\Safety_Monitoring_CCTV-main\\body\\person_model_yolov8m.pt')
hat_model = YOLO("C:\\Users\\한국전파진흥협회\\Desktop\\java\\새 폴더 (2)\\Safety_Monitoring_CCTV-main\\Safety_Monitoring_CCTV-main\\body\\hat_model_v1.pt")

tracker = Sort()

#cctv Cam
cap = cv2.VideoCapture(0)

# 의자 실제 높이 (m)와 초점 거리(픽셀)
REAL_CHAIR_HEIGHT = 1.0
FOCAL_LENGTH_PIXELS = 700
K_chair = REAL_CHAIR_HEIGHT * FOCAL_LENGTH_PIXELS

# 실험적 보정 계수 (실제 거리와 영상 거리 차이 보정용)
SCALE_FACTOR = 0.4  # 필요에 따라 조정하세요

WARNING_DISTANCE = 200  # 픽셀 기준 경고 임계값
output_width = 800
output_height = 600
paused = False

userd = []  # 사용자의 이름 목록
track_id_to_name = {}  # 객체 추적 ID와 이름을 매핑할 딕셔너리
disappeared_names = []  # 사라진 사용자 목록

#이름 매칭
def map_ids_to_names(detected_ids):
    global track_id_to_name, disappeared_names, userd
    current_ids = set(detected_ids)  # 현재 감지된 ID 세트
    tracked_ids = set(track_id_to_name.keys())  # 이전에 추적된 ID 세트

    disappeared_ids = tracked_ids - current_ids  # 사라진 ID들
    for did in disappeared_ids:
        name = track_id_to_name.pop(did, None)  # 사라진 ID에 해당하는 이름 제거
        if name and name in userd:
            disappeared_names.append(name)  # 사라진 사용자 목록에 추가

    new_ids = current_ids - tracked_ids  # 새로 감지된 ID들
    assigned_names = set(track_id_to_name.values())  # 이미 할당된 이름들
    available_names = disappeared_names.copy()  # 사라진 사용자 목록을 복사하여 사용

    # 아직 할당되지 않은 이름을 available_names에 추가
    for name in userd:
        if name not in assigned_names and name not in available_names:
            available_names.append(name)

    # 새로 감지된 ID에 이름을 할당
    for track_id in new_ids:
        if available_names:
            assigned_name = available_names.pop(0)  # 가능한 이름을 하나 할당
            track_id_to_name[track_id] = assigned_name
            if assigned_name in disappeared_names:
                disappeared_names.remove(assigned_name)  # 사라진 목록에서 이름 제거
        else:
            track_id_to_name[track_id] = f"사람{track_id}"  # 이름이 없으면 기본적으로 "사람{ID}"로 지정

    return {tid: track_id_to_name[tid] for tid in detected_ids}

# WebSocket 이벤트 처리
@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# WebSocket을 통해 실시간으로 벌점 보내기
def send_penalty():
    global no_hat_count
    socketio.emit('penalty_update', no_hat_count)  # WebSocket을 통해 실시간으로 벌점 데이터 전송

# CCTV 영상 처리 함수
def process_video():
    global danger_start_time
    global fall_start_time
    while cap.isOpened():
        ISFALL = 0 #넘어진 사람이 있는지
        ISHAT = 0 #모자를 안쓴 사람이 있는지
        ISDANGER = 0 #위험지역에 있는 사람이 있는지
        if not paused:
            ret, frame = cap.read()
            if not ret:
                break
            frame_time = datetime.now().strftime("%Y%m%d%H%M%S.%d")[:-3]  # 밀리초까지 출력
            print(f"📸 Frame captured at: {frame_time}")
            # 1) 사람 감지
            person_results = person_model(frame, verbose=False, conf = 0.6)[0]
            person_boxes_conf = []
            for det in person_results.boxes:
                if int(det.cls[0]) == 0:
                    x1, y1, x2, y2 = map(int, det.xyxy[0])
                    conf = float(det.conf[0])
                    person_boxes_conf.append([x1, y1, x2, y2, conf])

            person_boxes_np = np.array(person_boxes_conf) if len(person_boxes_conf) > 0 else None
            # 2) 사람 트래킹
            if person_boxes_np is not None:
                tracks = tracker.update(person_boxes_np)
            else:
                tracks = []

            # 3) 모자 감지
            hat_results = hat_model(frame, verbose=False, conf = 0.4)[0]
            hat_boxes = []
            for det in hat_results.boxes:
                x1, y1, x2, y2 = map(int, det.xyxy[0])
                hat_boxes.append([x1, y1, x2, y2])

            # 4) 의자 감지 (사람 모델에서 클래스 56 = chair)
            chair_boxes = []
            for det in person_results.boxes:
                cls = int(det.cls[0])
                if cls == 56:
                    x1, y1, x2, y2 = map(int, det.xyxy[0])
                    chair_boxes.append([x1, y1, x2, y2])
            # 5) 넘어짐 감지
            classifier_model_path = 'yolo/xgb_yolo_model.joblib'
            pose_detector = initialize_yolo_model()
            fall_classifier = load_pose_model(classifier_model_path)
            results = pose_detector(frame, verbose=False, conf=0.7)
            annotated_frame = results[0].plot()
            landmark_data = []
            if results[0].keypoints and len(results[0].keypoints.xy) > 0:
                for kps in results[0].keypoints:
                    person_landmarks = []
                    coords = kps.xyn[0]
                    confs = kps.conf[0]
                    for i in range(len(coords)):
                        person_landmarks.append((coords[i][0].item(), coords[i][1].item(), confs[i].item()))
                    landmark_data.append(person_landmarks)
            is_fallen_current_frame = run(fall_classifier, landmark_data)

             # 이창열 : 트래킹 추적
            detected_track_ids = [int(track[4]) for track in tracks]  # 트래킹된 객체의 ID
            name_map = map_ids_to_names(detected_track_ids)  # ID에 해당하는 이름 매핑
            
            # OpenCV에서 Pillow 이미지로 변환
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame_rgb)
            draw = ImageDraw.Draw(pil_img)
            
            global no_hat_count, hat_status, previous_hat_status, dic_hat_status

            # tracks와 관련된 각 사람의 모자 상태를 추적
            for track in tracks:
                x1, y1, x2, y2, track_id = map(int, track)
                name = name_map.get(track_id, f"ID{track_id}")
                person_box = [x1, y1, x2, y2]

                # 모자 착용 여부 판단
                # 모자 착용 여부 판단
                hat_status = "No Hat"
                # dic_hat_status[name] = "No Hat" 
                for hat in hat_boxes:
                    if is_hat_in_person(person_box, hat, threshold=0.5):
                        hat_status = "Hat"
                        dic_hat_status[name] = "Hat"
                        break

                # 모자 상태에 따라 색상 지정
                color = (0, 255, 0) if hat_status == "Hat" else (0, 255, 255)  # 초록=모자 있음, 노랑=없음
                label_text = f"{name}: {hat_status}"
                
                 # `no_hat_count`에 해당 이름이 없다면 초기화
                if name not in no_hat_count:
                    no_hat_count[name] = 0  # 값이 없을 때만 0으로 초기화

                # `previous_hat_status` 값이 없을 때 초기화
                if name not in previous_hat_status:
                    previous_hat_status[name] = "No Hat"
                    
                if name not in no_hat_start_time:
                    no_hat_start_time[name] = None
                
                if hat_status == "No Hat":
                    # 모자 벗기 시작한 시간을 기록
                    if no_hat_start_time[name] is None:
                        no_hat_start_time[name] = time.time()
                    else:
                        elapsed = time.time() - no_hat_start_time[name]
                        if elapsed >= 3.0:  # ⏱️ 1초 이상 유지
                            no_hat_count[name] += 1
                            print(f"{name} 벌점 증가 ➕ {no_hat_count[name]}")
                            send_penalty()
                            no_hat_start_time[name] = None  # 벌점 추가 후 초기화
                            ISHAT = 1 #db에 저장용

                else:
                    # 모자를 쓰면 초기화
                    no_hat_start_time[name] = None
                    
                previous_hat_status[name] = hat_status
                
                # 상태 출력 (디버깅용)
                print(f"No Hat Count: {no_hat_count[name]},{name}")

                # 사람 박스 및 모자 상태 출력
                
                # 0.6, color, 2)

                p_base = box_base_center(person_box)

                for c_box in chair_boxes:
                    c_base = box_base_center(c_box)
                    chair_height_px = c_box[3] - c_box[1]
                    if chair_height_px <= 0:
                        continue

                    # 의자 높이 기준 거리 계산
                    estimated_distance_m = K_chair / chair_height_px
                    dist_px = euclidean_distance(p_base, c_base)
                    real_distance_m = (dist_px / chair_height_px) * estimated_distance_m * SCALE_FACTOR

                    # 거리 표시
                    mid_x = (p_base[0] + c_base[0]) // 2
                    mid_y = (p_base[1] + c_base[1]) // 2
                    
                    
                    # 200픽셀 기준(WARNING_DISTANCE) 거리에 따른 색상 변화
                    distance_color = (255, 0, 0) if dist_px < WARNING_DISTANCE else (255, 255, 0)
                    
                    
                    draw.text((x1, y1 - 10), label_text, font=font, fill=distance_color)

                    draw.line([tuple(p_base), tuple(c_base)], fill=(255, 255, 0), width=2)


                    if dist_px < WARNING_DISTANCE:
                        if danger_start_time == 0:
                            danger_start_time = time.time()
                        else:
                            elapsed = time.time() - danger_start_time
                            if elapsed > 3.0:
                                ISDANGER = 1 #db에 저장용
                        # 사람 박스 강조
                        draw.rectangle([ (x1, y1), (x2, y2) ], outline=(0, 255, 0), width=3)

                        # 의자 박스 강조
                        draw.rectangle([ (c_box[0], c_box[1]), (c_box[2], c_box[3]) ], outline=(0, 0, 255), width=3)
                        global trr
                        draw.rectangle([ (trr[0], trr[1]), (trr[2], trr[3]) ], outline=(0, 255, 255), width=3)
                    else: #멀어지면 초기화
                        danger_start_time = 0
            if is_fallen_current_frame:
                if fall_start_time == 0:
                        fall_start_time = time.time()
                else:
                    elapsed = time.time() - fall_start_time
                    if elapsed >= 3.0:  # ⏱️ 1초 이상 유지
                        ISFALL = 1 #db에 저장용
            else:
                fall_start_time = 0
        #기록 날짜 저장용
        now = datetime.now()
        now_date = now.strftime("%Y-%m-%d")
        output_folder = f'accident_{now_date}'
        os.makedirs(output_folder, exist_ok=True)
        if ISFALL:
            # 현재 폴더 안의 파일 개수 확인
            existing_files = os.listdir(output_folder)
            next_index = len(existing_files) + 1
            filename = f'fall_{next_index}.jpg'
            frame_filename = os.path.join(output_folder, filename)
            photopath = os.path.join(output_folder, filename)
            cv2.imwrite(frame_filename, frame)
            sql = f"INSERT INTO `pleaseworkcompany`.`accident_log` (`ACCIDENTID`, `ACCIDENTDATE`, `LOGISDELETE`, `LOG_UPLOAD_DATE`, `LOG_PHOTO_PATH`) VALUES ('1', '{now_date}', '0', '{now_date}', '{filename}');"
            cursor.execute(sql)
            db.commit()
        if ISHAT:
            # 현재 폴더 안의 파일 개수 확인
            existing_files = os.listdir(output_folder)
            next_index = len(existing_files) + 1
            filename = f'not_hat_{next_index}.jpg'
            frame_filename = os.path.join(output_folder, filename)
            photopath = os.path.join(output_folder, filename)
            cv2.imwrite(frame_filename, frame)
            sql = f"INSERT INTO `pleaseworkcompany`.`accident_log` (`ACCIDENTID`, `ACCIDENTDATE`, `LOGISDELETE`, `LOG_UPLOAD_DATE`, `LOG_PHOTO_PATH`) VALUES ('2', '{now_date}', '0', '{now_date}', '{filename}');"
            cursor.execute(sql)
            db.commit()
        if ISDANGER:
            # 현재 폴더 안의 파일 개수 확인
            existing_files = os.listdir(output_folder)
            next_index = len(existing_files) + 1
            filename = f'danger_{next_index}.jpg'
            frame_filename = os.path.join(output_folder, filename)
            photopath = os.path.join(output_folder, filename)
            cv2.imwrite(frame_filename, frame)
            sql = f"INSERT INTO `pleaseworkcompany`.`accident_log` (`ACCIDENTID`, `ACCIDENTDATE`, `LOGISDELETE`, `LOG_UPLOAD_DATE`, `LOG_PHOTO_PATH`) VALUES ('3', '{now_date}', '0', '{now_date}', '{filename}');"
            cursor.execute(sql)
            db.commit()
        #draw 이미지 처리
        frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        
        frame_resized = cv2.resize(frame, (output_width, output_height))
        ret, buffer = cv2.imencode('.jpg', frame_resized)
        frame_bytes = buffer.tobytes()

        # HTTP multipart 스트림 형식으로 프레임 전송
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')


# 메인 페이지 렌더링 (HTML 파일로 CCTV 화면 표시)
@app.route('/')
def index():
    return render_template('hyun.html')

@app.route('/get_penalty', methods=['GET'])
def get_penalty():
    return no_hat_count

# 비디오 스트리밍을 위한 엔드포인트
@app.route('/cctv_feed')
def cctv_feed():
    return Response(process_video(), mimetype='multipart/x-mixed-replace; boundary=frame')

# 사용자의 이름 목록을 업데이트하는 엔드포인트
@app.route('/save_users', methods=['POST'])
def save_users():
    global userd
    data = request.json  # 요청에서 JSON 데이터 받기
    userd = data.get('users', [])  # 사용자 리스트 업데이트
    return {"message": "User list updated."}  # 응답 반환

#---------------------------pose model-----------------------------------


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
def pose_video():
    # cap = cv2.VideoCapture(1)
    if not cap.isOpened():
        print("🚨 오류: 웹캠을 열 수 없습니다.")
        return
    
    classifier_model_path = 'yolo/xgb_yolo_model.joblib'
    pose_detector = initialize_yolo_model()
    fall_classifier = load_pose_model(classifier_model_path)

    if not all([pose_detector, fall_classifier]):
        print("⛔️ 모델 초기화에 실패하여 프로그램을 종료합니다.")
        return

    WINDOW_SIZE = 100  # 최근 100개 프레임을 기억
    FALL_THRESHOLD_RATIO = 0.85  # 윈도우의 70% 이상이 '넘어짐'일 때 최종 판단
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

        
        # 7. 최종 판단 결과에 따라 텍스트 표시
        if is_fall_confirmed:
            cv2.putText(annotated_frame, "FALL DETECTED", (50, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3, cv2.LINE_AA)
            winsound.Beep(1000, 10)
            
        
        # 8. 결과를 화면에 보여주기
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# @app.route('/pose')
# def pose():
#     return render_template('pose.html')

@app.route('/video_feed')
def video_feed():
    return Response(pose_video(), mimetype='multipart/x-mixed-replace; boundary=frame')


# Flask 애플리케이션 실행
if __name__ == '__main__':
    # 비디오 처리는 백그라운드에서 실행되므로, Flask는 메인 스레드에서 실행
    app.run(host='0.0.0.0', port=5001)
