import paho.mqtt.client as mqtt
import json
import os, base64
import time
from tkinter import *
from tkinter import messagebox
import socket
import hashlib

timelist = {'Now':0,'10min':600,'1hour':3600,'1day':86400,'1week':604800}
MainTopic = "updates/"
SubTopic = "UpdateList" 
userId = "Alice"
userPw = "mose"
brokerIp = "broker ip"
port = 1883
server_host = "socket server ip"
server_port = 12345
tmpDirectory = "tmp path"
versionPath = "version.json path"

def compute_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def on_connect(client, userdata, flags, reasonCode):
    if reasonCode == 0:
        print("Connected successfully.")
        with open(versionPath,"r") as TargetJson:
            TargetList =  json.load(TargetJson)
            for Target in TargetList.keys():
                client.subscribe(MainTopic + Target)
        client.subscribe(MainTopic + SubTopic)
    else:
        print(f"Failed to connect, return code {reasonCode}")

def on_disconnect(client,userdata,flags,rc = 0):
    print(str(rc)+'/')

def update_choice():
    OTA_UI = Tk()
    later_time = StringVar()
    OTA_UI.title("Choice update")
    window_width = OTA_UI.winfo_screenwidth()
    window_height = OTA_UI.winfo_screenheight()
    app_width = 500
    app_height = 300
    width_center = int((window_width - app_width)/2)
    height_center = int((window_height - app_height)/2)
    OTA_UI.geometry(f"{app_width}x{app_height}+{width_center}+{height_center}")
    information = Label(OTA_UI,text = 'Notification!\nDo you want to update new firmware?\nclick the button when you want',font = ('bold'))
    
    def event_PB():
        if later_time.get() == 'Now':
            messagebox.showinfo("Notice","You choice Now, Start install firmware!")
            OTA_UI.destroy()

        elif later_time.get() == '':
            messagebox.showinfo("Notice","You choice Now, Start install firmware!")
        else:
            messagebox.showinfo("Notice",f"You choice Later, Notice update after {later_time.get()} later!")
            OTA_UI.destroy()
            
    button_Submit = Button(OTA_UI,text = 'Submit',command = event_PB)
    Later_time0 = Radiobutton(OTA_UI, text = 'Now', value = 'Now', variable = later_time)
    Later_time1 = Radiobutton(OTA_UI, text = '10min', value = '10min', variable = later_time)
    Later_time2 = Radiobutton(OTA_UI, text = '1hour', value = '1hour', variable = later_time)
    Later_time3 = Radiobutton(OTA_UI, text = '1day', value = '1day', variable = later_time)
    Later_time4 = Radiobutton(OTA_UI, text = '1week', value = '1week', variable = later_time)
    information.pack()
    button_Submit.pack()
    Later_time0.pack()
    Later_time1.pack()
    Later_time2.pack()
    Later_time3.pack()
    Later_time4.pack()
    OTA_UI.mainloop()
    return timelist.get(later_time.get())

def send_file(server_host, server_port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((server_host, server_port))
        print(f"Connected to server {server_host}:{server_port}")       
        client_socket.sendall(message)
        print("File sent successfully.")

def on_message(client, userdata, msg):
    try:
        with open(versionPath,"r") as versionlist:
            version = json.load(versionlist) 
    except:
        version = dict()
    
    
    try:
        payload = json.loads(msg.payload)
        UpdateList = payload.keys()
        print(UpdateList)
        flag = 1
        while(flag):
            flag = update_choice()
            time.sleep(flag)

        for file in UpdateList:
            FileSplit = file.split('-')
            FileName = FileSplit[-1]
            FileVersion = FileSplit[1]
            FileTarget = FileSplit[0]
            FileHash = payload[file]

            firmwarePath = tmpDirectory + FileName

            print(f"Varify file hash!:{file}")
            if FileHash == compute_file_hash(firmwarePath):
                flag = 1
                print("File has valid!!")
                try:
                    with open(tmpDirectory + FileName,"rb") as SendFile:
                        content = SendFile.read()
                except FileNotFoundError as e:
                    print(e)

                try:
                    if FileTarget == 'image':
                        message = b'image/' + FileName.encode('utf-8') + b':' + content
                    else:
                        message = FileName.encode('utf-8') + b':' + content
                except:
                    print("Fail Make message")

                while(flag):  
                    try:
                        send_file(server_host, server_port,message)
                        flag = 0
                    except:
                        print("Cluster and Controller are not conected! \nRetry send file")
                        time.sleep(10)

                version[FileName] = FileVersion
                with open(versionPath,"w") as version_file:
                    version_file.write(json.dumps(version))

            else:
                print("FileHash do not match. Firmware might be tampered or updated.")

        print("Ready for new update")

    except:
        firmwarePath = os.path.join(tmpDirectory + msg.topic.split("/")[-1])
        try:
            print("start download")
            with open(firmwarePath,'wb') as file:
                file.write(base64.b64decode(msg.payload))
            print("end download")
            time.sleep(1)
            print(f"Firmware downloaded and saved to {tmpDirectory}")
            print(f"firmwareDirectory: {tmpDirectory}")
            print(f"firmwarePath: {firmwarePath}")
        except Exception as e:
                print(f"Error downloading the firmware: {e}")

                           
client = mqtt.Client()
client.username_pw_set(userId, userPw)
client.on_connect = on_connect
client.on_message = on_message
client.connect(brokerIp,port, keepalive=60)

client.loop_forever()