import paho.mqtt.client as mqtt
import json
import hashlib
import os, time

Sub_Topic = "updates"
userId = "Alice"
userPw = "mose"
brokerIp = "203.246.114.226"
port = 1883
target_list = []

global update_firmware_path, latest_version, file_list
update_firmware_path = 'C:/Users/mose/Volkswagen/api/updatefirmwares/'
latest_version = dict()
file_list = dict()

def check_new_firmware():
    diff = []
    remove_dict_list =[]
    remove_file_list=[]
    now_file_list = os.listdir(update_firmware_path)
    for firmware in now_file_list:
        if firmware not in file_list:
            diff.append(firmware)
            try:
                with open(update_firmware_path + firmware,'r',encoding='utf-8') as file:
                    if file.readline().strip() == '#####File Properties######':
                        filename=file.readline().strip().split(' ')[-1]
                        if firmware == filename:
                            file_list[firmware] = dict()
                            file_list[firmware]['target']= file.readline().strip().split(' ')[-1]
                            file_list[firmware]['version'] = file.readline().strip().split(' ')[-1]
                            try:    
                                if float(file_list[firmware]['version']) > float(latest_version[file_list[firmware]['target']]):
                                    latest_version[file_list[firmware]['target']] = file_list[firmware]['version']
                                else:
                                    diff.remove(firmware)
                            except:                               
                                latest_version[file_list[firmware]['target']] = file_list[firmware]['version']
                                target_list.append(file_list[firmware]['target'])
                        else:
                            print(f'{firmware} has wrong properties:remove file')
                            diff.remove(firmware)
                            remove_file_list.append(update_firmware_path+firmware)
                    else:
                        print(firmware,"doesn`t have properties:remove file")
                        diff.remove(firmware)
                        remove_file_list.append(update_firmware_path+firmware)
            except FileNotFoundError as e:
                print(e)

    for file in file_list:
        if file not in now_file_list:
            remove_dict_list.append(file)

    for file in remove_dict_list:
        del(file_list[file])

    if remove_file_list:
        for file in remove_file_list:
            os.remove(file)
            try:
                del(file_list[file.split('/')[-1]])
            except:
                pass
    
    if diff:
        remove_list=[]
        for firmware in diff:
            if float(file_list[firmware]['version']) >= float(latest_version[file_list[firmware]['target']]):
                latest_version[file_list[firmware]['target']] = file_list[firmware]['version']            
            else:
                remove_list.append(firmware)
        for firmware in remove_list:
            diff.remove(firmware)

    if diff:
        print('='*30)
        for target in target_list:
            print('latest', target,'version:',latest_version[target])
            print('='*30)
        print("need to update about: ", diff)
    return diff

def compute_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256_hash.update(chunk)
    return sha256_hash.hexdigest()

def make_json(FilePath):
    firmware = dict()
    try:
        with open(FilePath,'r',encoding='utf-8') as file:
            Content=file.readlines()
        Content = [line.strip() for line in Content]
        firmware['FileName'] = Content[1].split(' ')[-1]
        firmware['Target'] = Content[2].split(' ')[-1]
        firmware['Version'] = Content[3].split(' ')[-1]
        print("="*100)
        print(json.dumps(firmware,indent='\t'))
        print("="*100)
        with open(FilePath,'r',encoding='utf-8') as file:
            firmware['Content']=file.read()
        already_update_firmware_path = 'C:/Users/mose/Volkswagen/api/already update firmware/' + firmware['FileName']       
        try:
            with open(already_update_firmware_path, 'wb') as file:
                file.write(firmware['Content'].encode('utf-8'))
            time.sleep(1)
        except:
            pass

        firmware['FileHash'] = compute_file_hash(already_update_firmware_path)
        return json.dumps(firmware)

    except FileNotFoundError:
        pass

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Error: Connection fail, Return code =" ,rc)

def on_disconnect(client,userdata,flags,rc = 0):
    print(str(rc),end='/')

def on_publish(client,userdata,mid):
    print("In on_pub call back mid = ", mid,end='/')

client = mqtt.Client()

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish

count = 724000

while True:
     
    publish_list = []
    publish_list = check_new_firmware()

    if publish_list:
        for FileName in publish_list:
            client.connect(brokerIp, 1883)
            FilePath = update_firmware_path + FileName
            client.loop_start()

            client.publish(Sub_Topic, make_json(FilePath), 2, retain= True)
            client.loop_stop()
            print("Success sending file:",FileName)
            client.disconnect()
    
    time.sleep(1.0)
