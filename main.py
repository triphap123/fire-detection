# main.py
import cv2
import time
import onnxruntime as ort
from random import randint
from packages import RTSP_URL, MODEL_PATH, SEND_INTERVAL
from packages import RTSPReader 
from packages import send_alarm, preprocess, process_detections
import minimalmodbus
from time import sleep

# Cấu hình cổng và thiết bị
instrument = minimalmodbus.Instrument('/dev/ttyUSB1', 1)  # Cổng serial và slave ID
instrument.serial.baudrate = 9600
instrument.serial.timeout = 1
instrument.mode = minimalmodbus.MODE_RTU

def read_temp():
    raw_temp = instrument.read_register(0x0000, functioncode=3)
    return raw_temp / 10.0

def main():
    session = ort.InferenceSession(MODEL_PATH, providers=["CPUExecutionProvider"])
    input_name = session.get_inputs()[0].name
    output_name = session.get_outputs()[0].name

    reader = RTSPReader(RTSP_URL)
    last_sent_time = 0
    fire_last_detected = False
    last_temp_sent_time = 0
    

    try:
        while True:
            temp = read_temp()
            frame = reader.read()
            if frame is None:
                continue

            input_tensor = preprocess(frame)
            outputs = session.run([output_name], {input_name: input_tensor})[0]
            detections, annotated = process_detections(outputs, frame)
            print(detections)

            has_fire_label = len(detections) > 0
            current_time = time.time()

            if current_time - last_temp_sent_time > SEND_INTERVAL:
                if has_fire_label:
                    send_alarm(temp, True)
                    print(f"🔥 CẢNH BÁO CHÁY! Gửi API với nhiệt độ {temp} ")
                    sleep(0.5)
                else:
                    send_alarm(temp, False)
                    print(f"Cập nhật nhiệt độ: {temp}")
                    sleep(0.5)
                last_temp_sent_time = current_time

            cv2.imshow("Fire Detection", annotated)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:
        reader.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
