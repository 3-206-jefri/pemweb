from sqlalchemy import Column, Integer, Text, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import json

Base = declarative_base()

class Review(Base):
    __tablename__ = "reviews"
    id = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    sentiment = Column(String(50))
    key_points = Column(Text)  # simpan JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    def to_dict(self):
        kp = None
        try:
            kp = json.loads(self.key_points) if self.key_points else None
        except:
            kp = self.key_points
        return {
            "id": self.id,
            "text": self.text,
            "sentiment": self.sentiment,
            "key_points": kp,
            "created_at": self.created_at.isoformat()
        }
