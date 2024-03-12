from datetime import datetime

from pydantic import BaseModel, ConfigDict
from shapely import Geometry


class Port(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: int | None = None
    port_name: str | None = None
    locode: str | None = None
    geometry: Geometry
    latitude: float | None = None
    longitude: float | None = None
    country_iso3: str | None = None
    has_excursion: bool = False
    created_at: datetime | None = None
    updated_at: datetime | None = None
