from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sync.handlers.config_handler import ConfigHandler

Base = declarative_base()

class FilePosition(Base):
    __tablename__ = 'file_positions'
    id = Column(Integer, Sequence('file_id_seq'), primary_key=True)
    file = Column(String(255), unique=True)
    position = Column(Integer)

    def __init__(self, file, position):
        self.file = file
        self.position = position

class Database:
    def __init__(self):
        config = ConfigHandler()
        db_url = config.get_value('DATABASE', 'DB_URL')
        self.engine = create_engine(db_url)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Crea las tablas si no existen
        Base.metadata.create_all(self.engine)

    def get_last_position(self, file):
        file_position = self.session.query(FilePosition).filter_by(file=file).first()
        if file_position:
            return file_position.position
        else:
            return 0

    def set_last_position(self, file, position):
        file_position = self.session.query(FilePosition).filter_by(file=file).first()
        if not file_position:
            file_position = FilePosition(file, position)
            self.session.add(file_position)
        else:
            file_position.position = position
        self.session.commit()

    def close(self):
        self.session.close()
