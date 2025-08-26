import cv2
import numpy as np
from ultralytics import YOLO
from sort import Sort  # SORT 알고리즘 사용

def xywh2xyxy(x, y, w, h):
    return [int(x - w/2), int(y - h/2), int(x + w/2), int(y + h/2)]

# 모델 불러오기
person_model = YOLO('person_model_yolov8m.pt')
hat_model = YOLO('hat_model_cap.pt')

# SORT 추적기 초기화
tracker = Sort()

# 비디오 불러오기
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # 사람 감지 (COCO)
    person_results = person_model(frame, verbose=False)[0]
    person_boxes = []
    for det in person_results.boxes:
        if int(det.cls[0]) == 0:  # class 0: person
            x1, y1, x2, y2 = map(int, det.xyxy[0])
            conf = float(det.conf[0])
            person_boxes.append([x1, y1, x2, y2, conf])

    person_boxes_np = np.array(person_boxes)
    tracks = tracker.update(person_boxes_np)

    # 모자 감지 (Custom)
    hat_results = hat_model(frame, verbose=False)[0]
    hat_boxes = []
    for det in hat_results.boxes:
        x1, y1, x2, y2 = map(int, det.xyxy[0])
        hat_boxes.append([x1, y1, x2, y2])

    # 추적된 사람에 대해 Hat 여부 확인
    for track in tracks:
        x1, y1, x2, y2, track_id = map(int, track)
        label = f"ID{track_id}"
        color = (0, 255, 0)  # Green for person

        # 기본값: No Hat
        hat_status = "No Hat"
        for hat in hat_boxes:
            hx1, hy1, hx2, hy2 = hat
            # IoU 기반으로 모자 착용 판단
            iou_x1 = max(x1, hx1)
            iou_y1 = max(y1, hy1)
            iou_x2 = min(x2, hx2)
            iou_y2 = min(y2, hy2)
            inter_area = max(0, iou_x2 - iou_x1) * max(0, iou_y2 - iou_y1)
            person_area = (x2 - x1) * (y2 - y1)
            hat_area = (hx2 - hx1) * (hy2 - hy1)
            union_area = person_area + hat_area - inter_area
            iou = inter_area / union_area if union_area > 0 else 0

            if iou > 0.1:
                hat_status = "Hat"
                break

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(frame, f"{label}:{hat_status}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

    cv2.imshow('Hat Detection + Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
