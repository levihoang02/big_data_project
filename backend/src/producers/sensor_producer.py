from config.config import Config
from kafka import KafkaProducer
import time
import random
from datetime import datetime
import json

class SensorProducer:
    def __init__(self):
        self.topics = [Config.TOPIC_TEMPERATURE, Config.TOPIC_HUMIDITY]
        self.producer = KafkaProducer(
            bootstrap_servers=Config.BOOTSTRAP_SERVERS,
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

    def generate_sensor_data(self):
        """Generate sample sensor data"""
        while True:
            try:
                timestamp = datetime.now().isoformat()
                print(f"Attempting to send message to topic '{Config.TOPIC_TEMPERATURE}': {timestamp}")
                # Generate temperature data
                self.producer.send(
                    Config.TOPIC_TEMPERATURE,
                    {
                        'topic': Config.TOPIC_TEMPERATURE,
                        'value': round(random.uniform(20, 30), 2),
                        'timestamp': timestamp
                    }
                )
                
                print(f"Attempting to send message to topic '{Config.TOPIC_HUMIDITY}': {timestamp}")
                # Generate humidity data
                self.producer.send(
                    Config.TOPIC_HUMIDITY,
                    {
                        'topic': Config.TOPIC_HUMIDITY,
                        'value': round(random.uniform(30, 70), 2),
                        'timestamp': timestamp
                    }
                )

                time.sleep(2)  # Wait 2 seconds between readings

            except Exception as e:
                print(f"Error generating sensor data: {e}")
                time.sleep(5)  # Wait before retrying

    def stop(self):
        """Stop the producer"""
        if self.producer:
            self.producer.close()

if __name__ == '__main__':
    producer = SensorProducer()
    try:
        producer.generate_sensor_data()
    except Exception as e:
        producer.stop()
        print(f"An error occurred: {e}")
