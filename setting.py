from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
import psycopg2

# postgresqlのDBの設定
DATABASE = "postgresql://postgres:chancy_anecdote_smear@118.27.26.119:5432/psemi?sslmode=require"

# Engineの作成
ENGINE = create_engine(
    DATABASE,
    encoding="utf-8",
    # TrueにするとSQLが実行される度に出力される
    echo=True
)

# Sessionの作成
session = scoped_session(
    # ORM実行時の設定。自動コミットするか、自動反映するなど。
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=ENGINE
    )
)

# modelで使用する
Base = declarative_base()
Base.query = session.query_property()