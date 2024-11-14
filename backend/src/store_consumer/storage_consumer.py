from datetime import datetime, timedelta
from config.config import Config
from services.database import DatabaseService
from kafka import KafkaConsumer
import json

class StorageConsumer():
    def __init__(self):
        self.topics = [Config.TOPIC_TEMPERATURE, Config.TOPIC_HUMIDITY]
        self.db_service = DatabaseService()
        self.consumer = KafkaConsumer(
            *self.topics,
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
            group_id=Config.CONSUMER_GROUP_STORAGE,
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        self.last_timestamp = None
        self.message_buffer = []
        self.interval = timedelta(seconds=Config.INTERVAL_SECONDS)  # Set interval to 30 seconds

    def process_message(self) -> None:
        """Process messages and store in database at intervals"""
        try:
            for message in self.consumer:
                current_time = datetime.now()
                self.message_buffer.append(message.value)

                # Check if it's time to insert the buffered data
                if (self.last_timestamp is None or 
                    current_time - self.last_timestamp >= self.interval):
                    
                    if self.message_buffer:
                        try:
                            # Bulk insert all buffered messages
                            inserted_count = self.db_service.bulk_insert_sensor_data(self.message_buffer)
                            print(f"Successfully stored {inserted_count} messages in database")
                            
                            # Clear the buffer and update timestamp
                            self.message_buffer = []
                            self.last_timestamp = current_time
                            
                        except Exception as e:
                            print(f"Error storing messages in database: {e}")
                            
        except Exception as e:
            print(f"Error processing message: {e}")
        finally:
            self.consumer.close()

    def stop_consuming(self) -> None:
        if self.message_buffer:
            try:
                # Attempt to save any remaining buffered messages before stopping
                self.db_service.bulk_insert_sensor_data(self.message_buffer)
            except Exception as e:
                print(f"Error storing final messages: {e}")
        self.consumer.close()
        print("Storage consumer stopped")

if __name__ == "__main__":
    storage_consumer = StorageConsumer()
    try:
        storage_consumer.process_message()
    except KeyboardInterrupt:
        print("Stopping storage consumer...")
        storage_consumer.stop_consuming()
