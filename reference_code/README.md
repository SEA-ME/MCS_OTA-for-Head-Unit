![ota drawio](https://github.com/SEA-ME/MCS_OTA-for-Head-Unit/assets/163559668/74f75887-6576-4ef7-83d3-480ac82b53ea)

# OTA Required Setting

## Used cluster model
    git clone https://github.com/aveeslab/sea-me-hackathon-2023
   
## Used py
    - OTA_publisher.py
    - OTA_subscriber.py
    - client_listner.py
    
## for broker server (in OTA Server)
    -	Download and install mosquitto from Windows and mac from Internet
    -	Use the command 'sudo apt install mosquitto mosquitto-clients' in Linux terminal for download mosquitto
    -	After installation is completed, go to the directory where mosquitto is installed and modify mosquitto.conf to open the port and set permission for external access
    -	Run broker server by applying the configuration file to mosuquitto -c mosquitto.conf -v
    
## for publisher (in OTA Server)
    -	Py file set sub_topic it selves with version json file
    -	Change the brokerIP equivalent to broker server ip for connecting to the broker server
    -	Assign the appropriate port value to the broker server configuration file
    -	Change file check path of check_new_firmware function as absolute path
    -	At this time, assign a directory separately for new firmware (use this path for function)
    -	Please make your update name of file 'target'(image/firmware)-'version'-'filename'(filename in vehicle)

## for subscriber(in Vehicle's Central Gateway )
    -	Py file set sub_topic it selves with version json file, so please write your all file in vehicle what is updated by OTA in version.json
    -	Change brokerIP to broker server ip for connecting to the broker server on subscirbe.py
    -	Assign the appropriate port value to the broker server configuration file
    -	File download path of on_massage function as absolute path
    -	Add internal version variable change code based on updated files or add internal version variable code for version from each ECU
    -	Modified code when sending a file to the ECU through socket communication after downloading, fo example client ip and port, or create a new process to send when checking the new firmware

## for Target ECU (in Vehicle)
    -	When receiving a file from the Central gate, it will remake process file you just need to turn off and on the cluster after complete update

 
