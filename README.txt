Name: Chrystabel Sunata
Email: csunata3@gatech.edu
Class Name: CS 3251 - Computer Networking I
Date: 26 November 2024
Assignment Title: Programming Assignment 2 - Chat

There are 3 files submitted:
- tchatcli.py
The client enables a user to connect to the server, input commands (such as subscribe, unsubscribe,
message, timeline, exit), and receive messages from the server. 

- tchatsrv.py
The server handles multiple clients simultaneously using multithreading. The server handles all logic
and execution of the user commands. It also maintains subscription and message records.

- README.txt
This file contains documentation of my learning and progress.

Key learnings, challenges and process of implementation:
- Learnt how to implement multithreaded architecture in both server and client
- Learnt how to design the client with the main thread to handle user input and secondary thread to
listen for messages from the server
- Initially confused on how to get the client to print statements when all the logic is in server, solved
by having the server send necessary print statements to the client
- Started implementing the server side by initializing dictionaries to store mapping between username,
client sockets, hashtags, messages
- Implemented a function to handle each user command in the server
- Implemented the core logic in the server's handle_client function where command is read from
the client and server calls the appropriate function based on the command

Known bugs or limitations:
- My program does not check for invalid hashtags
- Messages are limited to 150 characters
- My program does not handle missing arguments or incorrect user commands
- My program also does not handle the case where a user attempts to unsubscribe from a hashtag they weren't
previously subscribed to
- When the client exits the program, the >> prompt still appears even though the correct exit statement is
printed 

The protocol your client and server use to communicate (how do they understand what to do with each message
exchange?):
In my protocol, the client sends the username upon connection and all user commands. The server parses the
command, processes them, and sends back all appropriate results, which will be printed by the client. All
logic is handled in the server.