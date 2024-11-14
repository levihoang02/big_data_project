from dataclasses import dataclass
import os

@dataclass
class Config:
    BOOTSTRAP_SERVERS: str = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
    TOPIC_TEMPERATURE: str = 'sensor.temperature'
    TOPIC_HUMIDITY: str = 'sensor.humidity'
    CONSUMER_GROUP_STREAM: str = 'stream_group'
    CONSUMER_GROUP_STORAGE: str = 'storage_group'
    
    # Database configuration
    DB_HOST: str = os.getenv('DB_HOST', 'postgres')
    DB_PORT: str = os.getenv('DB_PORT', '5432')
    DB_NAME: str = os.getenv('DB_NAME', 'iot_db')
    DB_USER: str = os.getenv('DB_USER', 'iot_user')
    DB_PASSWORD: str = os.getenv('DB_PASSWORD', 'iot_password')
    
    #Storage consumer configuration
    INTERVAL_SECONDS: int = 600
