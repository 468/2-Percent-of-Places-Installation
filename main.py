import bluetooth
import numpy as np
import cv2
import socket
import requests
import json

serverMACAddress = 'mac_address_here'
port = 3
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.connect((serverMACAddress, port))

cam = cv2.VideoCapture(0)
i = 0;

current_text = "Starting"

while(True):

	i = i+1;
	ret, frame = cam.read();
	if i%50==0:
		cv2.imwrite('latest_capture.jpg',frame)
		payload = {'image': open('latest_capture.jpg', 'rb') }
		r = requests.post("http://127.0.0.1:5000/model/predict", files=payload)
		json_data = r.json()
		print(json_data)
		print(json_data["predictions"][0]["label"])
		current_label = json_data["predictions"][0]["label"]
		s.send(str(current_label))
	
	cv2.namedWindow("Final", 0);
	cv2.resizeWindow("Final", 500,500);
	cv2.imshow("Final", frame)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break;

cam.release()
cv2.destroyAllWindows()
