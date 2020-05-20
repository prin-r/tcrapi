import eventlet

# Monkey patch all blocking operations to use green threads.
eventlet.monkey_patch()

# Export application
from app.core import app, socketio
