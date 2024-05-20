# Required Setting

## for broker server (in OTA Server)
    -	Download and install mosquitto from Windows and mac from Internet
    -	Use the command 'sudo apt install mosquitto mosquitto-clients' in Linux terminal for download mosquitto
    -	After installation is complete, go to the directory where mosquitto is installed and modify mosquitto.conf to open the port and set permission for external access
    -	Run broker server by applying the configuration file to mosuquitto -c mosquitto.conf -v
    
## for publisher (in OTA Server)
    -	Change the sup_topic equivalent to subscriber
    -	Change the brokerIP equivalent to broker server ip for connecting to the broker server
    -	Assign the appropriate port value to the broker server configuration file
    -	Change file check path of check_new_firmware function as absolute path
    -	At this time, assign a directory separately for new firmware (use this path for function)
    -	File Type - Changeable (but required to modify file characteristics check code when changing)
        #####File Properties#####
        #file name: name
        #target: target
        #version: version
        ######################
        ~content
    -	Specify absolute path from make_json function to already_update_firmware_path - Occasionally, one hash for determining the integrity of the same file may be determined to be a 
        different file based on the subscription

## for subscriber(in Vehicle's Central Gateway )
    -	Change the sup_topic equivalent to publish.py 
    -	Change brokerIP to broker server ip for connecting to the broker server on subscirbe.py
    -	Assign the appropriate port value to the broker server configuration file
    -	File download path of on_massage function as absolute path
    -	Add internal version variable change code based on updated files or add internal version variable code for version from each ECU
    -	Write additional code when sending a file to the ECU through serial communication after downloading the file or create a new python file to send when checking the new firmware
    -	When transmitting to the ECU as mqtt (assuming wireless communication inside the vehicle), subtopic assignment to each ECU, change the topic and publish the code in accordance with    
        the file target

## for Target ECU (in Vehicle)
    -	When receiving a file from the Central gate, the code that causes the file to run on boot-set to automatically enforce it
    -	When running using rc.local, the code location must exist before exit 0, so check directly and modify the text list
        for example.
        ##########################################
        sudo python /home/usr/firmware/newfirmware.py &

        exit 0
        ##########################################
    -	If you use .bb file, write new code for automatically updating new firmware

 
