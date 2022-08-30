# **VNET BACKEND**
VNET is a video conferencing web application built in Python using Django. 
The main disticntion with VNET is that a client can share the incoming streams with another peer on their network ([Explained here](https://github.com/wild-times/vnet-frontend)). 

## Contents.
- [Overview](#overview).  
- [Abbreviations](#abbreviations).  
- [Function of VNET Backend](#the-function-of-the-backend).  
- [Using this repo](#using-this-repository).  


## Overview
To intergrate video conferencing, VNET uses Microsoft's **Azure Communication Services** for the video/audio backend. The official documentation describes Azure Communication Services as cloud-based services with REST APIs and client library SDKs available to help you integrate communication into your applications. It provides you with communication capabilities, including the ability to make and/or receive phone calls, sending and/or receiving text messages, making audio and video calls over IP and hosting group meetings and chat. It is a client-to-server model. It is the same backend service used by Microsoft Teams.

[![ACS getting started](https://i.ytimg.com/vi_webp/chMHVHLFcao/maxresdefault.webp)](https://www.youtube.com/watch?v=chMHVHLFcao 'Click to watch ✨')

**[✨ More information on Azure Communication Services](https://docs.microsoft.com/en-us/azure/communication-services/overview 'Overview of ACS')**

## **Abbreviations**
- ACS - Azure Communiction Services.
- UUID - Universally Unique Identifier.
- WebRTC - Web Real-Time Communication.

## **The function of the backend.**
The backend has five functions that it manages:
1. [Create users for VNET](#a-user-management).
2. [Get ACS identities and tokens](#a-user-management).
3. [Map VNET users and ACS identities](#a-user-management).
4. [Serving the front-end](#c-serving-the-frontend).
5. [Signalling for the peer-to-peer connections](#b-signalling-for-peer-to-peer-connection).


### **a). User management**
The first three functions listed above can be combined into user management.

In order for a client to access the ACS backend, they need to have an ACS identity and access token. This access token expires every 24 hours, therefore needs to be refreshed as much.

The backend thus creates users. After creating a user, it requests ACS to provide and identity and access tokens. When ACS issues these, the backend then maps our user to the provided ACS identity. It also periodically requests ACS to refresh the access token. A simple overview as shown by the image below;

![ACS user management](https://docs.microsoft.com/en-us/azure/communication-services/media/scenarios/architecture_v2_identity.svg 'Shows how the backend and ACS manage/interact with users')


**[✨ How the backend and ACS interact for identities and tokens](https://docs.microsoft.com/en-us/azure/communication-services/quickstarts/access-tokens?tabs=windows&pivots=programming-language-python 'ACS tokens and identities')**

When the front-end requries any information about a user or meeting, it is provided by the backend, either as HTML Response or JSON response if the endpoint is for REST.

To join a group meeting on ACS, a UUID that uniquely identifies the meeting is needed. This UUID is generated by VNET, without and need of ACS. UUID collisions are extremely unlikely, thus ACS allows the client to generate their own UUID for the meeting. Joining a meeting with the same UUID gets your into the same meeting as described [✨ here](https://docs.microsoft.com/en-us/azure/communication-services/how-tos/calling-sdk/manage-calls?pivots=platform-web#join-a-group-call 'ACS join a group call').


**[✨ VNET and ACS need to interact as described here](https://docs.microsoft.com/en-us/azure/communication-services/concepts/client-and-server-architecture 'Client and Server Architecture ACS')**

### b). Signalling for peer-to-peer connection.
For the peer-to-peer connection used by devices on the same network, a standard known as *Web Real-Time Communication* (WebRTC) is used. WebRTC enables peer-to-peer communication, but it still needs servers so that clients can exchange metadata to coordinate communication through a process called signaling. It however does not implement signalling in it's API, giving the developer freedom/doom of having to come up with the signalling mechanism. According to [✨ Sam Dutton on WebDev](https://web.dev/webrtc-infrastructure/ 'Build the backend services needed for a WebRTC app'), signaling is the process of coordinating communication. In order for a WebRTC app to set up a call, its clients need to exchange the following information:
- Session-control messages used to open or close communication.  
- Error messages.  
- Media metadata, such as codecs, codec settings, bandwidth, and media types.  
- Key data used to establish secure connections.  
- Network data, such as a host's IP address and port as seen by the outside world.  

More detail of how the VNET WebRTC connection happens is decribed [here](https://github.com/wild-times/vnet-frontend#how-the-peer-connection-happens-webrtc), this portion concentrates on the signalling section which is a responsibility of the backend.

The signal uses, [web sockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API 'The WebSocket API (WebSockets)'), to keep the connection open, allowing for messages to be passed. It's available at `ws://host/vnet/ps/{code}/`. `code` is a six digit number generated by client. Only two clients can be connected to the socket with a specific code. The clients also need to be authenticated.

Once a client is connected to the endpoint and it sends a message, the message is broadcast to all that are connected.

```
// Example endpoint

url = ws://localhost/vnet/ps/232445/
```

[✨ More information about signalling](https://web.dev/webrtc-infrastructure/ 'Build the backend services needed for a WebRTC app')

### **c). Serving the frontend.**
The entire frontend is served by VNET. The section used for meetings as `/meet/`, is built with *ReactJS* and *ACS SDKs*, the rest is plain HTML.


## **Using this repository.**
Before using this repo, you need an active Azure subscription, learn how [here](https://azure.microsoft.com/en-us/get-started/#explore-azure). You need to set up Azure Communication Services. Following the [official documentation on setting up ACS](https://docs.microsoft.com/en-us/azure/communication-services/quickstarts/create-communication-resource?tabs=windows&pivots=platform-azp&source=docs 'Create and manage Communication Services resources').

1. Clone this repository/get the repo in your prefereed way.
    ```commandline
    git clone https://github.com/wild-times/vnet-backend.git
    ```
2. Get the ACS connection string from your azure portal. [Here's how](https://docs.microsoft.com/en-us/azure/communication-services/quickstarts/create-communication-resource?tabs=windows&pivots=platform-azp&source=docs#access-your-connection-strings-and-service-endpoints 'Access your connection strings and service endpoints'). Store it in `vnet/acs.txt`
3. Get a django secret key and store it in `vnet/secret_key.txt`
   ```python
    from django.core.management.utils import get_random_secret_key

    secret_key = get_random_secret_key()
    ```
4. Install requirements, either globally but preferably in a virtual enviroment.
    ```commandline
    pip install -r requirements.txt
    ```
5. Make/run migrations.
    ```commandline
    python manage.py makemigrations core
    python manage.py makemigrations help
    python manage.py makemigrations meeting

    python manage.py migrate
    ```
6. Run server.


> Please read more on the links marked ✨
   
&copy; 2022 Wild Times
