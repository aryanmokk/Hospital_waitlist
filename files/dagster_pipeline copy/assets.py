"""
Dagster assets for the Irish Healthcare Access pipeline.

Three assets, one per team member's notebook. Dependencies are inferred
from function arguments — Dagster builds the DAG automatically.

DAG:
    ntpf_data ─┐
               ├─→ hse_access_and_integration
    cso_data ──┘
"""
from pathlib import Path

import papermill as pm
from dagster import AssetExecutionContext, asset

from .resources import MongoResource, PostgresResource

PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXECUTED_DIR = PROJECT_ROOT / "outputs_dagster"

NOTEBOOKS = {
    "ntpf": PROJECT_ROOT / "member1_ntpf.ipynb",
    "cso":  PROJECT_ROOT / "member2_cso.ipynb",
    "hse":  PROJECT_ROOT / "member3_hse.ipynb",
}


def _run_notebook(context: AssetExecutionContext, key: str) -> str:
    src = NOTEBOOKS[key]
    dst = EXECUTED_DIR / f"{key}_executed.ipynb"
    if not src.exists():
        raise FileNotFoundError(f"Notebook not found: {src}")
    EXECUTED_DIR.mkdir(parents=True, exist_ok=True)
    context.log.info(f"Executing notebook: {src.name}")
    pm.execute_notebook(
        input_path=str(src),
        output_path=str(dst),
        kernel_name="python3",
        log_output=True,
        progress_bar=False,
    )
    context.log.info(f"Notebook executed successfully: {dst.name}")
    return str(dst)


@asset(
    group_name="member_1_ntpf",
    description="NTPF waiting list data scraped from ntpf.ie open data, stored raw in MongoDB and cleaned tables in ntpf.* schema in Postgres.",
)
def ntpf_data(context: AssetExecutionContext,
              mongo: MongoResource, postgres: PostgresResource) -> str:
    return _run_notebook(context, "ntpf")


@asset(
    group_name="member_2_cso",
    description="CSO Census 2022 demographics fetched from PxStat JSON-RPC API, cached in MongoDB, joined with NTPF and loaded to cso.* schema in Postgres.",
)
def cso_data(context: AssetExecutionContext,
             ntpf_data: str,
             mongo: MongoResource, postgres: PostgresResource) -> str:
    return _run_notebook(context, "cso")


@asset(
    group_name="member_3_hse",
    description="HSE hospital geospatial access scores. Joins NTPF + CSO data with computed Haversine distances to produce cso.final_integrated, the headline 26-county dashboard table.",
)
def hse_access_and_integration(context: AssetExecutionContext,
                               ntpf_data: str, cso_data: str,
                               mongo: MongoResource, postgres: PostgresResource) -> str:
    return _run_notebook(context, "hse")
