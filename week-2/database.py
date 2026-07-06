from sqlmodel import SQLModel, Field, create_engine, Session

DATABASE_URL = "postgresql://neondb_owner:npg_zT23XJbdFyio@ep-shy-wave-ategojuy-pooler.c-9.us-east-1.aws.neon.tech/Tasks?sslmode=require&channel_binding=require"

engine = create_engine(
    DATABASE_URL,
    echo=True
)

def create_db_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
