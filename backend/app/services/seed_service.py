import csv
from pathlib import Path

from sqlmodel import Session, select

from app.database import engine
from app.models import Destination

SEED_DIR = Path(__file__).resolve().parent.parent.parent / "seed_data"

REGION_MAP = {
    "AF": "Afrika", "DZ": "Afrika", "AO": "Afrika", "BJ": "Afrika", "BW": "Afrika",
    "BF": "Afrika", "BI": "Afrika", "CM": "Afrika", "CV": "Afrika", "CF": "Afrika",
    "TD": "Afrika", "KM": "Afrika", "CG": "Afrika", "CD": "Afrika", "CI": "Afrika",
    "DJ": "Afrika", "EG": "Afrika", "GQ": "Afrika", "ER": "Afrika", "SZ": "Afrika",
    "ET": "Afrika", "GA": "Afrika", "GM": "Afrika", "GH": "Afrika", "GN": "Afrika",
    "GW": "Afrika", "KE": "Afrika", "LS": "Afrika", "LR": "Afrika", "LY": "Afrika",
    "MG": "Afrika", "MW": "Afrika", "ML": "Afrika", "MR": "Afrika", "MU": "Afrika",
    "MA": "Afrika", "MZ": "Afrika", "NA": "Afrika", "NE": "Afrika", "NG": "Afrika",
    "RW": "Afrika", "ST": "Afrika", "SN": "Afrika", "SC": "Afrika", "SL": "Afrika",
    "SO": "Afrika", "ZA": "Afrika", "SS": "Afrika", "SD": "Afrika", "TZ": "Afrika",
    "TG": "Afrika", "TN": "Afrika", "UG": "Afrika", "ZM": "Afrika", "ZW": "Afrika",
    "DE": "Europa", "FR": "Europa", "GB": "Europa", "IT": "Europa", "ES": "Europa",
    "PT": "Europa", "NL": "Europa", "BE": "Europa", "AT": "Europa", "CH": "Europa",
    "SE": "Europa", "NO": "Europa", "DK": "Europa", "FI": "Europa", "IE": "Europa",
    "PL": "Europa", "CZ": "Europa", "SK": "Europa", "HU": "Europa", "RO": "Europa",
    "BG": "Europa", "HR": "Europa", "SI": "Europa", "RS": "Europa", "BA": "Europa",
    "ME": "Europa", "MK": "Europa", "AL": "Europa", "GR": "Europa", "TR": "Europa",
    "CY": "Europa", "MT": "Europa", "LU": "Europa", "IS": "Europa", "LT": "Europa",
    "LV": "Europa", "EE": "Europa", "UA": "Europa", "BY": "Europa", "MD": "Europa",
    "GE": "Europa", "AM": "Europa", "AZ": "Europa",
    "CN": "Asien", "JP": "Asien", "KR": "Asien", "IN": "Asien", "ID": "Asien",
    "TH": "Asien", "VN": "Asien", "PH": "Asien", "MY": "Asien", "SG": "Asien",
    "MM": "Asien", "KH": "Asien", "LA": "Asien", "BD": "Asien", "LK": "Asien",
    "NP": "Asien", "PK": "Asien", "AF": "Asien", "UZ": "Asien", "KZ": "Asien",
    "TM": "Asien", "KG": "Asien", "TJ": "Asien", "MN": "Asien", "TW": "Asien",
    "HK": "Asien", "MO": "Asien", "BN": "Asien", "TL": "Asien", "MV": "Asien",
    "BT": "Asien",
    "SA": "Naher Osten", "AE": "Naher Osten", "IL": "Naher Osten",
    "JO": "Naher Osten", "LB": "Naher Osten", "IQ": "Naher Osten",
    "IR": "Naher Osten", "SY": "Naher Osten", "YE": "Naher Osten",
    "OM": "Naher Osten", "QA": "Naher Osten", "BH": "Naher Osten",
    "KW": "Naher Osten",
    "US": "Nordamerika", "CA": "Nordamerika", "MX": "Nordamerika",
    "GT": "Nordamerika", "BZ": "Nordamerika", "SV": "Nordamerika",
    "HN": "Nordamerika", "NI": "Nordamerika", "CR": "Nordamerika",
    "PA": "Nordamerika", "CU": "Nordamerika", "JM": "Nordamerika",
    "HT": "Nordamerika", "DO": "Nordamerika", "TT": "Nordamerika",
    "BB": "Nordamerika", "BS": "Nordamerika",
    "BR": "Suedamerika", "AR": "Suedamerika", "CL": "Suedamerika",
    "CO": "Suedamerika", "PE": "Suedamerika", "VE": "Suedamerika",
    "EC": "Suedamerika", "BO": "Suedamerika", "PY": "Suedamerika",
    "UY": "Suedamerika", "GY": "Suedamerika", "SR": "Suedamerika",
    "AU": "Ozeanien", "NZ": "Ozeanien", "FJ": "Ozeanien", "PG": "Ozeanien",
    "WS": "Ozeanien", "TO": "Ozeanien", "VU": "Ozeanien",
    "RU": "Europa",
}


def _country_to_region(iso2: str) -> str:
    return REGION_MAP.get(iso2, "Sonstige")


def seed_if_empty():
    with Session(engine) as session:
        existing = session.exec(select(Destination).limit(1)).first()
        if existing is not None:
            return

        _seed_cities(session)
        _seed_landmarks(session)
        session.commit()
        print("Database seeded successfully.")


def _seed_cities(session: Session):
    cities_file = SEED_DIR / "worldcities.csv"
    if not cities_file.exists():
        print(f"Warning: {cities_file} not found. Skipping city seed.")
        return

    batch = []
    with open(cities_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pop_str = row.get("population", "")
            try:
                population = int(float(pop_str)) if pop_str else None
            except (ValueError, TypeError):
                population = None

            if population is None or population < 50000:
                continue

            iso2 = row.get("iso2", "")
            batch.append(
                Destination(
                    name=row.get("city", row.get("city_ascii", "")),
                    category="city",
                    country=row.get("country", ""),
                    country_code=iso2,
                    latitude=float(row.get("lat", 0)),
                    longitude=float(row.get("lng", 0)),
                    population=population,
                    region=_country_to_region(iso2),
                )
            )

    session.add_all(batch)
    print(f"Seeded {len(batch)} cities.")


def _seed_landmarks(session: Session):
    landmarks_file = SEED_DIR / "landmarks.csv"
    if not landmarks_file.exists():
        print(f"Warning: {landmarks_file} not found. Skipping landmark seed.")
        return

    batch = []
    with open(landmarks_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            batch.append(
                Destination(
                    name=row.get("name", ""),
                    category="landmark",
                    country=row.get("country", ""),
                    country_code=row.get("country_code", ""),
                    latitude=float(row.get("latitude", 0)),
                    longitude=float(row.get("longitude", 0)),
                    description=row.get("description", ""),
                    region=row.get("region", ""),
                )
            )

    session.add_all(batch)
    print(f"Seeded {len(batch)} landmarks.")
