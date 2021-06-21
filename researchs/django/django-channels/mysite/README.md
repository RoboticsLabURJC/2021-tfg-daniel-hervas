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

If we have 2 tabs opened in the same lobby, the message sent in one tab wont appear in the other tab, for this to work, we need to have multiple instances of the same ChatConsumer. So we need to create a chat group in order to send messages to the group instead of resending them to the same client. We will need to configure channel layers in order to allow us to talk between different instances of an application. On this tutorial we will use Redis as backend storage for groups. We will run redis on docker at port 6379 as follows:

    docker run -p 6379:6379 -d redis:5

## Tutorial part 3: Asincronous chat server
Addapted ChatConsumer functions to AsyncWebsocketConsumer.

## Theory
- ASGI (Asynchronous Server Gateway Interface): provide a standard interface between async-capable Python web servers, frameworks and aplications.

- ProtocolTypeRouter as the root application of your project - the one that you pass to protocol servers - and nest other, more protocol-specific routing underneath there. It checks the connection type.