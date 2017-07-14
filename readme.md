# Chat Client

This application includes a server and a client. The server handles each client connection with a multi-threaded approach, and both the client and server are designed with Object Oriented design.
The client can use the following commands:

- login

    usage: login user pass
    
    If a valid username and password are supplied, the client is logged in to the server under that account. All remaining commands require logging in before they are accessible to the client.
    Upon logging in, all other currently connected and logged in clients see the new user has logged in.

- send

    usage: send target message
    
    If target is a valid Username, the message is sent to the server, and then directly to that user by the server.
    
    If target is 'all', the message is sent to the server and broadcasted to all users by the server.

- Who

    usage: who

    Returns list of all other logged in users in the chat server.

- logout

    usage: logout

    Logs the current user out, disconnects the client connection to the server, and server broadcasts that the user has left to others.
    
- newUser 

    usage: newUser <username> <password>

    creates a new user with username and password 
    
## To Do

- Refactor code and create functions to handle each command instead of coding it all out inside handle data
- Put check in place on server and client to receive the number of bytes to read so that it knows exactly 
  how much data to expect
