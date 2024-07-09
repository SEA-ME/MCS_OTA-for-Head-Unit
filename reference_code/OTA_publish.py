import paho.mqtt.client as mqtt
import json
import hashlib
import os, time
import hashlib
import base64

Sub_Topic = "updates/"
userId = "Alice"
userPw = "mose"
brokerIp = "brokerIP"
port = 1883

path = "update_file/folder path"
versionPath = "version.json path"

global file_list
file_list = dict()

def check_new_firmware():
    try:
        with open(versionPath,"r") as json_json:
            version = json.load(json_json)
    except FileNotFoundError as e:
        print(e)

    diff = []
    remove_dict_list =[]
    remove_list=[]
    now_file_list = os.listdir(path)

    for firmware in now_file_list:
        if firmware not in file_list.keys():
            diff.append(firmware)
            file_list[firmware] = dict()
            firmware_split = firmware.split('-')
            FileTarget = firmware_split[0]
            FileVersion = firmware_split[1]
            FileName = firmware_split[-1]
            file_list[firmware]['Target'] = FileTarget
            file_list[firmware]['FileName'] = FileName
            file_list[firmware]['Version'] = FileVersion

            
            try:
                if float(file_list[firmware]['Version']) >= float(version[file_list[firmware]['FileName']]):
                    version[file_list[firmware]['FileName']] = file_list[firmware]['Version']  
                else:
                    remove_list.append(firmware)
            except:
                version[file_list[firmware]['FileName']] = file_list[firmware]['Version']

    for file in file_list:
        if file not in now_file_list:
            remove_dict_list.append(file)
    
    for file in remove_list:
        diff.remove(file)

    for file in remove_dict_list:
        del file_list[file]
    
    if diff:
        remove_list=[]
        for firmware in diff:
            try:
                if float(file_list[firmware]['Version']) >= float(version[file_list[firmware]['FileName']]):
                    version[file_list[firmware]['FileName']] = file_list[firmware]['Version']            
                else:
                    remove_list.append(firmware)
            except:
                version[file_list[firmware]['FileName']] = file_list[firmware]['Version']
        for firmware in remove_list:
            diff.remove(firmware)

    print('='*100)
    print("Latest version")
    print('='*100)
    for key in version.keys():
        print(key + ": " + version[key])
    print('='*100)

    if diff:
        print("need to update about: ", diff)
        with open(versionPath,"w") as version_json:
            version_json.write(json.dumps(version))

    return diff

def compute_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def make_message(FilePath):
    
    try:
        with open (FilePath ,"rb") as file:
            message = base64.b64encode(file.read())      
        return message

    except FileNotFoundError as e:
        print("Error:" + e)

def make_update_list(publish_list):
    message = dict()
    for publish_file in publish_list:
        
        FilePath = path + publish_file
        with open(FilePath, "rb") as file:
            content = file.read()
        with open(FilePath, "wb") as file:
            file.write(content)

        message[publish_file] = compute_file_hash(FilePath)

        print('='*100)
        print("File name: " + publish_file)
        print("File hash: " + message[publish_file])
        print('='*100)
    return message

def on_connect(client, userdata, flags, reasonCode):
    if reasonCode == 0:
        print("connected OK")
    else:
        print("Error: Connection fail, Return code =" ,reasonCode)

def on_disconnect(client,userdata,flags,rc = 0):
    print(str(rc),end='\n')

def on_publish(client,userdata,mid):
    print("In on_pub call back mid = ", mid,end='\n')

client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

while True:

    os.system('cls')
    print("="*100)
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print("Time:", current_time)

    publish_list = []
    publish_list = check_new_firmware()
    
    if publish_list:
        for FileName in publish_list:
            client.connect(brokerIp, 1883)
            FilePath = path + FileName
            message = make_message(FilePath)
            client.loop_start()
            client.publish(Sub_Topic + FileName.split('-')[-1], message, 2, retain= True)
            client.loop_stop()
            print("Success sending file(updates/" + FileName.split('-')[-1]+ "):", FileName)
            client.disconnect()

        client.connect(brokerIp, 1883)
        UpdateList = make_update_list(publish_list)
        client.loop_start()
        client.publish(Sub_Topic + 'UpdateList', json.dumps(UpdateList), 2, retain= True)
        client.loop_stop()
        print("Success sending file(updates/UpdateList): UpdateList")
        client.disconnect()
    else:
        print(f"There's no need to update because there are no new files in the update folder in folder!")       
    
    time.sleep(1.0)
    print("="*100)
    time.sleep(10)