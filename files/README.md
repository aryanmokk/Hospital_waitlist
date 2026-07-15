# Hospital Waiting Lists, Access Inequality & Regional Health Demographics in Ireland

A data-analytics project examining how hospital waiting times across Ireland relate to
regional population demographics, geographic access (travel time to the nearest facility),
and HSE service distribution — and which specialties show the greatest combined inequality
of **access** and **wait**.

> **Research question.** *How do hospital waiting times across Ireland correlate with regional
> population demographics, geographic access (travel time to nearest facility), and HSE service
> distribution — and which specialties show the greatest combined inequality of access and wait?*

Built for the **Analytics Programming & Data Visualisation** module.

---

## Highlights

- Three open Irish government datasets integrated end to end: NTPF waiting lists, CSO Census/health
  demographics (PxStat), and the HSE facilities directory.
- Polyglot persistence: **MongoDB** for the semi-structured HSE JSON, **PostgreSQL + PostGIS** for
  the relational and spatial layer.
- A reproducible **ETL pipeline** joining the three sources into a master analytical table.
- A **travel-time matrix** (county × facility × specialty) and **2SFCA** (Two-Step Floating Catchment
  Area) access scoring, following Luo & Wang (2003).
- Statistical modelling (OLS regression, with an optional mixed-effects extension) and an interactive
  **Dash** dashboard.

---

## Architecture

```
HSE JSON (semi-structured)  ─►  MongoDB  ──┐
NTPF CSV + scraped reports  ────────────┐  │
CSO PxStat API (demographics) ──────────┤  ├─► ETL (Python) ─► PostgreSQL / PostGIS
Eircode / county centroids  ────────────┘  │                        │
                                            │                        ▼
Travel-time matrix (OpenRouteService) ──────┘             Analysis + Dashboard
                                                          (Plotly / Folium / Dash)
```

---

## Repository structure

```
.
├── README.md                 # this file
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # MongoDB + PostgreSQL/PostGIS
├── .env.example              # copy to .env and fill in
├── .gitignore
├── LICENSE
├── data/
│   ├── raw/                  # NOT committed — see .gitignore
│   └── processed/            # small cleaned samples only
├── sql/                      # schema + views
├── member1_ntpf/             # NTPF scrapers, loaders, waiting-time analysis
├── member2_cso/              # PxStat client, demographics, regression
├── member3_hse/              # Mongo ETL, travel-time matrix, 2SFCA, maps
├── shared/
│   ├── etl/                  # joins + master view
│   └── dashboard/            # Dash app
├── notebooks/                # exploratory notebooks, per member
└── report/                   # IEEE report source
```

---

## Getting started

### 1. Prerequisites

- Python 3.11+
- Docker + Docker Compose (for the databases)
- A free [OpenRouteService](https://openrouteservice.org/dev/) API key (for the travel-time matrix)

### 2. Clone and set up the environment

```bash
git clone <your-repo-url>.git
cd <repo>

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # then edit .env and add your ORS_API_KEY
```

### 3. Start the databases

```bash
docker compose up -d
```

This launches MongoDB on `27017` and PostgreSQL/PostGIS on `5432`, and initialises the Postgres
schema from `sql/`.

### 4. Run the pipeline

```bash
# Ingest raw data (each member's loaders)
python member1_ntpf/load.py
python member2_cso/load.py
python member3_hse/load.py

# Build the master analytical table
python shared/etl/build_master.py

# Launch the dashboard
python shared/dashboard/app.py
```

---

## Data sources

| Dataset | Source | Access |
|---|---|---|
| NTPF national waiting lists | National Treatment Purchase Fund | https://data.gov.ie |
| Census 2022 & health demographics | Central Statistics Office (PxStat API) | https://data.cso.ie |
| HSE health facilities directory | Health Service Executive | https://data.gov.ie |

All datasets are **open government data** from the Irish State. Raw data is **not committed** to the
repository; only small cleaned samples live under `data/processed/`. Run the loaders to reproduce.

---

## Team

| Member | Owns dataset | Primary technical contribution |
|---|---|---|
| Member 1 | NTPF waiting lists (CSV) + scraped monthly reports | Time-series cleaning, hospital-name normalisation, Postgres schema |
| Member 2 | CSO population & health demographics (PxStat) | API client, demographic preprocessing, statistical modelling |
| Member 3 | HSE facilities directory (JSON) | MongoDB ETL, travel-time matrix, 2SFCA scoring, map visualisations |

Integration, dashboard build, report and presentation are shared across all three members.

---

## References

- Luo, W. & Wang, F. (2003). Measures of spatial accessibility to health care in a GIS environment:
  synthesis and a case study in the Chicago region. *Environment and Planning B: Planning and Design*,
  30(6), 865–884.
- NTPF (2025). National waiting list data. https://data.gov.ie
- Central Statistics Office (2022). Census 2022 via PxStat. https://data.cso.ie
- HSE (2025). Health facilities directory. https://data.gov.ie

---

## Academic integrity

All code in this repository was written by Aryan Mokkapati and team as part of the Analytics
Programming & Data Visualisation module. External references and code sources are cited inline in the
relevant files. Datasets are open government data from the Irish State; no pre-existing Kaggle or
notebook implementations were used.
