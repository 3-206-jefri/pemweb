from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
import os
from dotenv import load_dotenv
load_dotenv()

engine = create_engine(os.environ['DATABASE_URL'])
Base.metadata.create_all(engine)
print("Tables created")
