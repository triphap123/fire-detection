# main.py
import cv2
import time
import onnxruntime as ort
from random import randint
from packages import RTSP_URL, MODEL_PATH, SEND_INTERVAL
from packages import RTSPReader 
from packages import send_alarm, preprocess, process_detections

def main():
    session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    reader = RTSPReader(RTSP_URL)
    last_sent_time = 0
    fire_last_detected = False
    

    try:
        while True:
            temp = randint(10,20)
            frame = reader.read()
            if frame is None:
                continue

            input_tensor = preprocess(frame)
            outputs = session.run([output_name], {input_name: input_tensor})[0]
            detections, annotated = process_detections(outputs, frame)

            has_fire = len(detections) > 0
            current_time = time.time()

            if has_fire and (not fire_last_detected or current_time - last_sent_time > SEND_INTERVAL):
                send_alarm(temp, True)
                fire_last_detected = True
                last_sent_time = current_time

            elif not has_fire and (fire_last_detected and current_time - last_sent_time > SEND_INTERVAL):
                send_alarm(temp, False)
                fire_last_detected = False
                last_sent_time = current_time

            cv2.imshow("Fire Detection", annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        reader.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
