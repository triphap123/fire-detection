RTSP_URL = "rtsp://192.168.1.135:8554/mystream"
MODEL_PATH = "/home/triphap/Documents/TriPhap/tttt/TT_ACuong/Navis_Data/model/best_90.onnx"

API_URL = "https://iot-api-vercel.vercel.app/api/setvaluev2"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoiZGV2aWNlX3VzZXIiLCJhY2Nlc3MiOiJyZWFkX3ZhbHVlIiwiZGV2aWNlX2lkIjoiQS1JVUgtVEVTVCIsImlhdCI6MTc1MzM0ODU1OCwiZXhwIjoxODE2NDIwNTU4fQ.A4PTCzEZIvitvz98qczYpsMDAbgtSmj4-63PazdNH8I"  # thay token thật


HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN}"
}

SEND_INTERVAL = 3
temp = 0
status_alarm = False

DATA = {
    "data": [
        {
            "GroupName": "Sensor",
            "Name": "Temp",
            "Unit": "oC",
            "Value": temp
        },
        {
            "GroupName": "STATUS",
            "Name": "CẢNH BÁO CÓ LỬA",
            "Alarm": True,
            "ValueBool": status_alarm 
        }
    ]
}
