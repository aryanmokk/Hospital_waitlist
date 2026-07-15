"""Dagster project entry point."""
from dotenv import load_dotenv

load_dotenv()

from dagster import Definitions, load_assets_from_modules

from . import assets
from .resources import build_resources

defs = Definitions(
    assets=load_assets_from_modules([assets]),
    resources=build_resources(),
)
