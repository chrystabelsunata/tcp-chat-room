## TCP Client-Server Chatroom
This project is my implementation of a **TCP chatroom** using **Python socket programming** for CS 3251 - Computer Networking (Fall 2024) at Georgia Tech. TCP (Transmission Control Protocol) is a communication protocol that ensures the reliable transmission of data between devices on a network. 

## Overview
The chatroom follows a **client-server archictecture**. The server handles multiple concurrent client connections, and routes messages between clients. Clients connect to the server and handle user commands until the user exits. Clients can subscribe to a hashtag and send and receive messages to those hashtags. The client supports the following user commands:
- `subscribe <hashtag>`: 
- `message <hashtag> <message>`
- `unsubscribe <hashtag>`
- `timeline`
