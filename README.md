python-engineio
===============

[![Build Status](https://travis-ci.org/miguelgrinberg/python-engineio.png?branch=master)](https://travis-ci.org/miguelgrinberg/python-engineio)

Python implementation of the [Engine.IO](https://github.com/Automattic/engine.io) realtime server.

Features
--------

- Fully compatible with the Javascript
  [engine.io-client](https://github.com/Automattic/engine.io-client) library.
- Compatible with Python 2.7 and Python 3.3+.
- Based on [Eventlet](http://eventlet.net/), enabling large number of
  clients even on modest hardware.
- Includes a WSGI middleware that integrates Engine.IO traffic with standard
  WSGI applications.
- Uses an event-based architecture implemented with decorators that hides the
  details of the protocol.
- Implements HTTP long-polling and WebSocket transports.
- Supports XHR2 and XHR browsers as clients.
- Supports text and binary messages.
- Supports gzip and deflate HTTP compression.
- Configurable CORS responses to avoid cross-origin problems with browsers.

Example
-------

The following application uses Flask to serve the HTML/Javascript to the
client:

    import engineio
    import eventlet
    from flask import Flask, render_template

    eio = engineio.Server()
    app = Flask(__name__)

    @app.route('/')
    def index():
        """Serve the client-side application."""
        return render_template('index.html')

    @eio.on('connect')
    def connect(sid, environ):
        print("connect ", sid)

    @eio.on('message')
    def message(sid, data):
        print("message ", data)
        eio.send(sid, 'reply')

    @eio.on('disconnect')
    def disconnect(sid):
        print('disconnect ', sid)

    if __name__ == '__main__':
        # wrap Flask application with engineio's middleware
        app = engineio.Middleware(eio, app)

        # deploy as an eventlet WSGI server
        eventlet.wsgi.server(eventlet.listen(('', 8000)), app)

Resources
---------

- [Documentation](http://pythonhosted.org/python-engineio)
- [PyPI](https://pypi.python.org/pypi/python-engineio)
