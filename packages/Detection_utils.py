# detection_utils.py
import cv2
import numpy as np

def preprocess(frame):
    img = cv2.resize(frame, (640, 640))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = img.transpose(2, 0, 1) / 255.0
    return img.astype(np.float32)[None]

def filter_detections(x1, y1, x2, y2, class_ids, confidences, distance_threshold=50):
    if len(x1) == 0:
        return x1, y1, x2, y2, class_ids, confidences

    detections = []
    for i in range(len(x1)):
        center_x = (x1[i] + x2[i]) / 2
        center_y = (y1[i] + y2[i]) / 2
        detections.append((center_x, center_y, class_ids[i], confidences[i], (x1[i], y1[i], x2[i], y2[i])))

    grouped = {}
    for det in detections:
        class_id = det[2]
        if class_id not in grouped:
            grouped[class_id] = []
        grouped[class_id].append(det)

    filtered_dets = []
    for class_id, dets in grouped.items():
        while dets:
            dets.sort(key=lambda x: x[3], reverse=True)
            best_det = dets.pop(0)
            filtered_dets.append(best_det)
            cx, cy = best_det[0], best_det[1]
            dets = [d for d in dets if np.sqrt((d[0] - cx) ** 2 + (d[1] - cy) ** 2) > distance_threshold]

    x1_new, y1_new, x2_new, y2_new, class_ids_new, confidences_new = [], [], [], [], [], []
    for det in filtered_dets:
        x1_new.append(det[4][0])
        y1_new.append(det[4][1])
        x2_new.append(det[4][2])
        y2_new.append(det[4][3])
        class_ids_new.append(det[2])
        confidences_new.append(det[3])

    return (
        np.array(x1_new), np.array(y1_new), np.array(x2_new),
        np.array(y2_new), np.array(class_ids_new), np.array(confidences_new)
    )

def process_detections(outputs, frame, conf_thresh=0.4):
    outputs = np.transpose(outputs, (0, 2, 1))[0]
    boxes = outputs[:, :4]
    scores = outputs[:, 4:]

    confidences = np.max(scores, axis=1)
    class_ids = np.argmax(scores, axis=1)

    mask = confidences > conf_thresh
    boxes, class_ids, confidences = boxes[mask], class_ids[mask], confidences[mask]

    if len(boxes) == 0:
        return [], frame

    h, w = frame.shape[:2]
    cx, cy, bw, bh = boxes[:, 0], boxes[:, 1], boxes[:, 2], boxes[:, 3]
    x1 = (cx - bw / 2) * w / 640
    y1 = (cy - bh / 2) * h / 640
    x2 = (cx + bw / 2) * w / 640
    y2 = (cy + bh / 2) * h / 640

    x1, y1, x2, y2, class_ids, confidences = filter_detections(
        x1, y1, x2, y2, class_ids, confidences
    )

    detections = []
    for cls, conf, x1i, y1i, x2i, y2i in zip(class_ids, confidences, x1, y1, x2, y2):
        label = f"{['fire', 'smoke'][cls]} {conf:.2f}"
        color = (0, 0, 255) if cls == 1 else (0, 255, 255)
        cv2.rectangle(frame, (int(x1i), int(y1i)), (int(x2i), int(y2i)), color, 2)
        cv2.putText(frame, label, (int(x1i), int(y1i) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        detections.append((cls, conf, (int(x1i), int(y1i), int(x2i), int(y2i))))

    return detections, frame
