import os
from dataclasses import dataclass
from functools import lru_cache
from typing import ClassVar, Optional


@dataclass
class Database:
    username: str
    password: str
    host: str
    port: str
    name: str

    @property
    def url(self):
        return f"{self.username}:{self.password}@{self.host}:{self.port}/{self.name}"


@dataclass
class Telegram:
    bot_token: str
    admin_ids: list[int]


@dataclass
class Config:
    database: Database | None = None
    telegram: Telegram | None = None
    base_url: str = None
    _config: ClassVar[Optional["Config"]] = None

    @classmethod
    @lru_cache(maxsize=1)
    def load(cls):
        if cls._config:
            return cls._config
        if os.path.exists("../.env"):
            from dotenv import load_dotenv

            load_dotenv(dotenv_path="../.env")
        try:
            cls._config = cls(
                database=Database(
                    username=os.environ["DB_USER"],
                    password=os.environ["DB_PASSWORD"],
                    host=os.environ["DB_HOST"],
                    port=os.environ["DB_PORT"],
                    name=os.environ["DB_NAME"],
                ),
                telegram=Telegram(
                    bot_token=os.environ["BOT_TOKEN"],
                    admin_ids=list(map(int, os.environ["ADMIN_IDS"].split(","))),
                ),
                base_url=os.environ["BASE_URL"],
            )
        except KeyError:
            raise Exception("Environment variables do not exist")
        return cls._config
