from sqlalchemy import Column, Integer, Float, String, DateTime
from sqlalchemy.sql import func
from services.database import Base

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "topic": self.topic,
            "value": self.value,
            "timestamp": self.timestamp.isoformat(),
            "created_at": self.created_at.isoformat()
        }