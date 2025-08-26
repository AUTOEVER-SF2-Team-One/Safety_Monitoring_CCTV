from ultralytics import YOLO
import numpy as np
from typing import List, Tuple

def initialize_yolo_model(model_path: str = "pose_model_yolov8n.pt") -> YOLO:
    """
    YOLOv8-Pose 모델을 초기화하고 객체를 반환합니다.
    모델은 처음 실행 시 자동으로 다운로드됩니다.

    Args:
        model_path (str): .pt 모델 파일의 경로 또는 이름.

    Returns:
        YOLO: 생성된 YOLO 모델 객체.
    """
    print("✅ YOLOv8-Pose 모델을 초기화합니다...")
    model = YOLO(model_path)
    print("✨ 모델 초기화 완료!")
    return model

def get_yolo_landmarks_from_image(model: YOLO, image: np.ndarray) -> List[List[Tuple[float, float, float]]]:
    """
    미리 초기화된 YOLO 모델을 사용하여 이미지에서 포즈 랜드마크를 추출합니다.

    Args:
        model (YOLO): 초기화된 YOLO 모델 객체.
        image (np.ndarray): 포즈를 감지할 이미지 (OpenCV 형식의 NumPy 배열).

    Returns:
        List[List[Tuple[float, float, float]]]:
        감지된 각 사람의 포즈 랜드마크 리스트.
        각 랜드마크는 (x, y, confidence) 튜플입니다.
    """
    pose_landmarks_list = []
    
    # YOLO 모델로 추론 실행
    results = model(image, verbose=False, conf = 0.6) # verbose=False로 로그 출력 끔

    # 결과가 하나라도 있는지 확인
    if not results:
        return pose_landmarks_list

    # 첫 번째 결과에서 keypoints 정보 추출
    res = results[0]
    if res.keypoints and len(res.keypoints.xy) > 0:
        # 감지된 모든 사람에 대해 반복
        for kps in res.keypoints:
            person_landmarks = []
            
            # 정규화된 좌표(xyn)와 신뢰도(conf)를 사용
            coords = kps.xyn[0]
            confs = kps.conf[0]
            
            for i in range(len(coords)):
                x = coords[i][0].item()
                y = coords[i][1].item()
                conf = confs[i].item()
                person_landmarks.append((x, y, conf))
            
            pose_landmarks_list.append(person_landmarks)

    return pose_landmarks_list