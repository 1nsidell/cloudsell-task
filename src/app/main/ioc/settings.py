"""
Реализация DI на основе FastAPI Depends,
я бы выбрал что-то более примемлемое для ioc контейнера.
Но такая реализация Depends помогает соблюдать dependency rule
и прикладной слой с инфрой не знают про FastAPI
"""

from pathlib import Path
from typing import Annotated

from fastapi import Depends

from app.infrastructure.common.config.config import (
    get_configs,
)
from app.infrastructure.common.config.constants import Directories


# ----Directories----
def get_directories() -> Directories:
    return Directories()


DirectoriesDep = Annotated[Directories, Depends(get_directories)]


def get_provider_a_directory(directories: DirectoriesDep) -> Path:
    return directories.PROVIDER_A_DATA


ProviderADataDep = Annotated[Path, Depends(get_provider_a_directory)]


def get_provider_b_directory(directories: DirectoriesDep) -> Path:
    return directories.PROVIDER_B_DATA


ProviderBDataDep = Annotated[Path, Depends(get_provider_b_directory)]


# ---- Configs ----

configs = get_configs()
