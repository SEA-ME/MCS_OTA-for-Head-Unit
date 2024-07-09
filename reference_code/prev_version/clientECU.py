import paho.mqtt.client as mqtt
import hashlib
import json
import requests
import os
import time

Sub_Topic = "UI"

userId = "Alice"
userPw = "mose"
brokerIp = "203.246.114.226"
port = 1883


version = 0.0
Target = 'UI'

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(Sub_Topic)

def compute_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)
    
    return sha256_hash.hexdigest()

def on_message(client, userdata, msg):
    
    payload = json.loads(msg.payload)
    print('='*30)
    print('file name: ',payload['FileName'])
    print('target: ',payload['Target'])
    print('version: ',payload['Version'])
    print('hash: ',payload['FileHash'])
    print('='*30,end='\n\n')
    target = payload['Target']
    if((float(payload['Version']) > version) & (target == Target)):        
        print(f"Proceeding with {target} firmware update...")
        time.sleep(1) 
        content = payload['Content'].encode('utf-8')
        try:
            firmwareDirectory = '/home/khs/OTA/firmware/'
            firmwarePath = os.path.join(firmwareDirectory, payload['FileName'])
            with open(firmwarePath, 'wb') as file:
                file.write(content)
            time.sleep(1)
            print(f"Firmware downloaded and saved to {firmwarePath}")
            
            downloaded_file_hash = compute_file_hash(firmwarePath)
            
            if(payload['FileHash'] == downloaded_file_hash):   
                time.sleep(1)               
                print("FileHash match. Firmware is verified.")
                print('='*30,end='\n\n')
            
            else:          
                print("FileHash do not match. Firmware might be tampered or updated.")
                os.remove(firmwarePath)
                time.sleep(1)
                print(f"Firmware removed")            
                print('='*30,end='\n\n')
        
        except requests.RequestException as e:
            print(f"Error downloading the firmware: {e}")    
        Version = float(payload['Version'])
    else:
        print("No new firmware update required.")
    
    with open('/etc/rc.local',"r") as file:
        text = file.readlines()
    text[3] = 'sudo python3 ' + firmwarePath +' &\n'
    with open('/etc/rc.local',"w") as file:
        for line in text:
            file.write(line)          

    
    
    
client = mqtt.Client()
client.username_pw_set(userId, userPw)
client.on_connect = on_connect
client.on_message = on_message

client.connect(brokerIp, port, 60)

client.loop_forever()
