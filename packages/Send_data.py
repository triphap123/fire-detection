import requests
from .Config import API_URL, HEADERS, DATA

def update_data_value(data_dict, name, value_key, new_value):
    for item in data_dict["data"]:
        if item.get("Name") == name:
            item[value_key] = new_value

def send_alarm(temp, status_alarm):
    update_data_value(DATA, "Temp", "Value", temp)
    update_data_value(DATA, "CẢNH BÁO CÓ LỬA", "ValueBool", status_alarm)

    try:
        response = requests.post(API_URL, json=DATA, headers=HEADERS)
        print(f"Đã gửi API: {DATA} - Mã phản hồi: {response.status_code}")
    except Exception as e:
        print("Lỗi khi gửi API:", e)
