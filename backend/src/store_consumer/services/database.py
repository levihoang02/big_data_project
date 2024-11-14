from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.sensor_data import SensorData
from datetime import datetime
from config.config import Config

db_config = Config()
DATABASE_URL = f"postgresql+psycopg2://{db_config.DB_USER}:{db_config.DB_PASSWORD}@{db_config.DB_HOST}:{db_config.DB_PORT}/{db_config.DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
class DatabaseService:
    def __init__(self):
        # Create tables if they don't exist
        Base.metadata.create_all(bind=engine)

    def insert_sensor_data(self, topic: str, value: float, timestamp: datetime):
        db = next(get_db())
        try:
            sensor_data = SensorData(
                topic=topic,
                value=value,
                timestamp=timestamp
            )
            db.add(sensor_data)
            db.commit()
            db.refresh(sensor_data)
            return sensor_data
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()

    def get_sensor_data(self, topic: str, limit: int = 100):
        db = next(get_db())
        try:
            return db.query(SensorData)\
                     .filter(SensorData.topic == topic)\
                     .order_by(SensorData.timestamp.desc())\
                     .limit(limit)\
                     .all()
        finally:
            db.close()

    def bulk_insert_sensor_data(self, data_list):
        db = next(get_db())
        try:
            sensor_data_objects = [
                SensorData(
                    topic=data['topic'],
                    value=float(data['value']),
                    timestamp=datetime.fromisoformat(data['timestamp'])
                )
                for data in data_list
            ]
            db.bulk_save_objects(sensor_data_objects)
            db.commit()
            return len(sensor_data_objects)
        except Exception as e:
            db.rollback()
            raise e
        finally:
            db.close()