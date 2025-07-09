from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class Directories:
    APP_DIR: Path = Path(__file__).parents[3]
    PATH_TO_BASE_FOLDER: Path = APP_DIR.parents[1]
    RESOURCES_FOLDER: Path = PATH_TO_BASE_FOLDER / "src" / "resources"
    PROVIDER_RESOURCES_FOLDER: Path = RESOURCES_FOLDER / "fake_provider_data"
    PROVIDER_A_DATA: Path = PROVIDER_RESOURCES_FOLDER / "provider_a.json"
    PROVIDER_B_DATA: Path = PROVIDER_RESOURCES_FOLDER / "provider_b.json"


@dataclass(slots=True, frozen=True)
class ApiPrefix:
    prefix: str = "/api/cloud-sell"
    healthcheck: str = "/healthcheck"
    liveness: str = "/liveness"
    readiness: str = "/readiness"
    v1_prefix: str = "/v1"
    pricing_plans: str = "/pricing-plans"
    orders: str = "/orders"


api_prefix = ApiPrefix()
