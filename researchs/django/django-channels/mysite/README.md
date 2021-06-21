# Django Channels Tutorial
For this project I will be following the tutorial offered by the [official documentation site](https://channels.readthedocs.io/en/stable/tutorial/).

## Tutorial part 1: Basic Setup
Here I have just created the paths for the urls, the views and also the index.html template, just the basics of a Django project.

After all the basic setup, I started creating the chat lobby template, in order that when the user types a lobby name and gets redirected to the lobby url it doesnt get an error message, and a template is rendered.

Finally, I set up Django Channels.

## Tutorial part 2: Sincronous chat server
When you create a socket connection with JavaScript listening on an URL, after that, your need to create a consumer that accepts that WebSocket connection, if not, JavaScript will show in the console an error.

I wrote my first consumer. Consumers are written at "consumers.py" file. After writing a consumer, you need to create a new file called "routing.py" in order to create a routing configuration for the app that has the route to the consumer (at app_name/routing.py).

Finally, at "asgi.py", just need to insert a websocket key. Not needed on Django 2.2 as ProtocolTypeRouter uses Channel's AsgiHandler. 

- asgy.py works as follows:

This root routing configuration specifies that when a connection is made to the Channels development server, the ProtocolTypeRouter will first inspect the type of connection. If it is a WebSocket connection (ws:// or wss://), the connection will be given to the AuthMiddlewareStack.

The AuthMiddlewareStack will populate the connection’s scope with a reference to the currently authenticated user, similar to how Django’s AuthenticationMiddleware populates the request object of a view function with the currently authenticated user. (Scopes will be discussed later in this tutorial.) Then the connection will be given to the URLRouter.

The URLRouter will examine the HTTP path of the connection to route it to a particular consumer, based on the provided url patterns.

## Tutorial part 3: Asincronous chat server

## Theory
- ASGI (Asynchronous Server Gateway Interface): provide a standard interface between async-capable Python web servers, frameworks and aplications.

- ProtocolTypeRouter as the root application of your project - the one that you pass to protocol servers - and nest other, more protocol-specific routing underneath there.