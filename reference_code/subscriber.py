import paho.mqtt.client as mqtt
import hashlib
import json
import requests
import os
import time

Sub_Topic = "updates" 
userId = "Alice"
userPw = "mose"
brokerIp = "203.246.114.226"
port = 1883

global Version
Version = dict()
Version['motor'] = 0.0
Version['light'] = 0.0
Version['UI'] = 0.0

def on_connect(client, userdata, flags, rc):
	print("Connected with result code " + str(rc))
	client.subscribe(Sub_Topic)

def compute_file_hash(file_path):
	sha256_hash = hashlib.sha256()
	with open(file_path, "rb") as file:
		for chunk in iter(lambda: file.read(4096), b""):
			sha256_hash.update(chunk)
	return sha256_hash.hexdigest()

# subscriber callback
def on_message(client, userdata, msg):
	payload = json.loads(msg.payload)
	print('file name : ',payload['FileName'])
	print('target: ',payload['Target'])
	print('version: ',payload['Version'])
	print('hash: ', payload['FileHash'])
	print('='*30)
	target = payload['Target']
	try:
		if float(payload['Version']) > Version[target]:
			print(f"Proceeding with {target} firmware update...")
			time.sleep(1)
			content = payload['Content'].encode('utf-8')
			try:
				tempDirectory = '/home/avees/OTA/'
				tempPath = os.path.join(tempDirectory, payload['FileName'])
				with open(tempPath, 'wb') as file:
					file.write(content)
				time.sleep(1)
				print(f"Firmware downloaded and saved to {tempPath}")

				downloaded_file_hash = compute_file_hash(tempPath)

				if payload['FileHash'] == downloaded_file_hash:
					time.sleep(1)
					print("FileHash match. Firmware is verified.")
					print('='*30,end='\n\n')
					if (input("do you dowload new firmware?[y/n]:") == 'y'):
						try:
							firmwareDirectory = '/home/avees/OTA/firmware/'
							firmwarePath = os.path.join(firmwareDirectory, payload['FileName'])
							with open(firmwarePath, 'wb') as file:
								file.write(content)
							time.sleep(1)
							print(f"Firmware downloaded and saved to {firmwarePath}")
							Version[target] = float(payload['Version'])
						except requests.RequestException as e:
							print(f"Error downloading the firmware: {e}")
					else:
						print("deny download new firmware")
						
				else:
					print(payload['FileHash'])
					print(downloaded_file_hash)
					print("FileHash do not match. Firmware might be tampered or updated.")
					time.sleep(1)
					
				os.remove(tempPath)
				
			except requests.RequestException as e:
				print(f"Error downloading the firmware: {e}")
			
		else:
			print("No new firmware update required.")
			
	except requests.RequestException:
		print(f"{target} is not exist")
	
	print("ready for a new update")

client = mqtt.Client()
client.username_pw_set(userId, userPw)
client.on_connect = on_connect
client.on_message = on_message

client.connect(brokerIp, port, 60)

client.loop_forever()
