from kafka import KafkaConsumer
from config.config import Config
import json
import time
from datetime import datetime
from services.socket_service import SocketService

socket_service = SocketService(Config.SOCKET_URL)

class StreamConsumer():
    def __init__(self):
        self.topics = [Config.TOPIC_TEMPERATURE, Config.TOPIC_HUMIDITY]
        print(f"Initializing consumer for topics: {self.topics}")
        print(f"Bootstrap servers: {Config.BOOTSTRAP_SERVERS}")
        
        self.consumer = KafkaConsumer(
            *self.topics,
            bootstrap_servers=Config.BOOTSTRAP_SERVERS,
            auto_offset_reset='latest',
            enable_auto_commit=True,
            group_id=Config.CONSUMER_GROUP_STREAM,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        print("Consumer initialized")
        print(f"Consumer subscription: {self.consumer.subscription()}")

    def process_message(self):
        try:
            print("Starting to consume messages...")
            while True:
                for message in self.consumer:
                    data = {
                        'topic': message.topic,
                        'value': message.value,
                        'timestamp': datetime.now().isoformat()
                    }
                    # Emit to socket server
                    socket_service.emit_data('kafka_data', {'data': data})
                    
        except Exception as e:
            print(f"Error processing message: {e}")
            raise e

    def stop_consuming(self) -> None:
        self.consumer.close()
        socket_service.close_connection()
        print("Stream consumer stopped")
        
if __name__ == "__main__":
    
    print("Starting stream consumer...")
    try:
        stream_consumer = StreamConsumer()
        # Convert the generator to a list to actually consume messages
        stream_consumer.process_message()
    except Exception as e:
        print(f"Error in stream consumer: {e}")
        stream_consumer.stop_consuming()
        raise e
   