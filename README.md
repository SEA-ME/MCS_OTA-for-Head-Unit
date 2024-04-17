# MSC_OTA-for-Head-Unit

# **MCS Project 1 - OTA**

- [**MCS Project 1 - OTA**](#mcs-project-1---ota)
  - [Introduction](#introduction)
  - [Project Goals and Objectives](#project-goals-and-objectives)
  - [System Architecture](#system-architecture)
  - [Project Timeline](#project-timeline)
  - [Self-Assessment](#self-assessment)
  - [Submission](#submission)
  - [References](#references)

## Introduction

The modern vehicle is rapidly transforming into a "driving computer," necessitating frequent updates to its software and firmware to manage and process data efficiently. Over-the-air (OTA) updates emerge as a pivotal technology in this context, enabling the wireless transmission and installation of new software or firmware directly from a server to the vehicle's system.

This project focuses on implementing OTA by updating new firmware with MQTT. Understand how subscribers, or clients, are authenticated by broadcasting through MQTT in real life through this deployment process. It will also be an approach that will lay the foundation for the development of OTAs applicable to various devices and high utility by increasing the understanding of OTAs in the MQTT method.

"In the contemporary automotive industry, software acts as the vehicle's heartbeat. The challenge of OTA updates is to maintain software currency while safeguarding vehicles against nascent cyber threats." This initiative is crucial for enhancing vehicle and user protection by ensuring the secure deployment of software updates.

By undertaking this ambitious project, we aim to investigate the OTA update process's capacity to safely upgrade vehicle software and firmware, thereby effectively countering all pertinent security threats. This endeavor will offer valuable insights for vehicle manufacturers and software developers ultimately equipping the automotive industry to navigate future challenges more adeptly.
<br>


## Project Goals and Objectives
This project outlines a comprehensive approach to implementing OTA updates, crucial for modern vehicles that rely heavily on software for their functionality. By wirelessly updating vehicle software and firmware, OTA technology offers a seamless method for enhancing vehicle capabilities and security. Here's an improved structure for the project, focusing on a clear step-by-step approach, testing, and clarification of technical terms:

### 1) OTA Server

__Web Server Implementation:__
- A web server will be configured to manage new software updates through a notice board-like interface, enabling easy access and organization.
- The server will feature the ability to upload both full and differential images. Full image upload functionality is standard, with differential image upload as an advanced option to minimize data transmission.

__MQTT Server Configuration:__
- Utilizing the MQTT protocol, the server will broadcast the latest software version and type. This ensures that all connected vehicles are aware of new updates in real-time.

### 2) Virtual Vehicle

__MQTT Client:__
- As an MQTT client, the virtual vehicle will incorporate features to receive new software information and download updates from the web server. This simulates real-world interaction with the OTA update system.
- Optionally, the process to generate a full image from differential updates will be outlined, providing a method to reconstruct the latest software version efficiently.

__Target DES head unit development:__
- The project will include the development of a DES head unit, facilitating the monitoring for OTA updates.
<br>


## System Architecture
The architecture outlined below centers around the OTA Server, Central Gateway, and Update Target, forming the core of the OTA system. Presently, the reference code is optimized for ECUs designated as Update Targets. However, it's important to note that our architecture is versatile and can be applied to any module within the vehicle, including but not limited to the Cluster and IVI systems. This flexibility is a key aspect of our design, ensuring broad applicability across various vehicle components.

<img width="1153" alt="image" src="https://github.com/SEA-ME/MCS_Secure-OTA/assets/163559668/6c0fdcd8-e649-4a2a-b1bb-bd396b1c1b7e">
<br>
<br>


## Project Timeline
A tentative project timeline for the Secure OTA project would include the following phases:

Planning and Preparation (1 week)
System Architecture and Design (1 week)
Implementing (2 week)
Testing and Debugging (1 week)
Pilot / Proof of Concept Deployment (1 week)
Note that the timeline may vary depending on the complexity of the project, the availability of resources, and the expertise of the development team. However, the timeline provides a general idea of the phases and timeline involved in implementing an OTA project.

<br>


## Self-Assessment
You can self-assess the security of your OTA update system using the following points as a guide.

__1) Implement OTA server:__
	-Initial error check and restart upon error detection
	-Send error messages and attempt to restart the server when an error occurs during operation.
	-Check the file goes up with no problem on the server when updating new software

__2) Use MQTT for update with broadcast:__
	-Check the update file delivered perfectly to the MQTT broker
	-Use QoS 2 or 1 because clients must receive more than one times for the update

__3) Implement client and subscribe MQTT for update:__
	-Initial error check and restart upon error detection
	-Subscribe to MQTT and receive new files from the server
	-Use an algorithm for checking the firmware version
	

<br>


## Submission
Submit the following artifacts to GitHub:

__1. Documentations:__
- Entire system architecture, data structures, and algorithms used.
- A comprehensive report detailing the methodology, challenges faced, and solutions implemented.
  
__2. Proof of Concept:__
- The source code.
  
__3. Presentation:__
- A presentation summarizing the project, including an overview of the system architecture, technical specifications, user interface, and test results.
<br>


## References
Here are some open-source references that could be useful in developing a Secure OTA project:
1. MQTT (2022), MQTT, https://mqtt.org/
2. Shin, Y., & Jeon, S. (2024). MQTree: Secure OTA Protocol Using MQTT and MerkleTree. Sensors, 24(5), 1447.
