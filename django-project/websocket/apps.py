from django.apps import AppConfig

class WebsocketConfig(AppConfig):
    name = 'websocket'

    def ready(self):
        import websocket.signals