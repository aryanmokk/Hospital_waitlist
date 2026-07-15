"""Database resources for the hospital project Dagster pipeline."""
import os
from contextlib import contextmanager

from dagster import ConfigurableResource
from pymongo import MongoClient
from sqlalchemy import create_engine


class MongoResource(ConfigurableResource):
    uri: str
    database: str = "hospital_project"

    @contextmanager
    def get_client(self):
        client = MongoClient(self.uri, serverSelectionTimeoutMS=5000)
        try:
            client.admin.command("ping")
            yield client[self.database]
        finally:
            client.close()


class PostgresResource(ConfigurableResource):
    uri: str

    def get_engine(self):
        return create_engine(self.uri, echo=False)


def build_resources():
    return {
        "mongo": MongoResource(uri=os.environ["MONGO_URI"]),
        "postgres": PostgresResource(uri=os.environ["PG_URI"]),
    }
