class Config:
    WEBSOCKET_URL = "ws://localhost:5000"

class ProductionConfig(Config):
    WEBSOCKET_URL = "wss://cec-events-604b31b937b9.herokuapp.com"
    
class DevelopmentConfig(Config):
    WEBSOCKET_URL = "ws://localhost:5000"