from bloom.domain.port import Port
from bloom.infra.database.sql_model import Port as SqlPort
from dependency_injector.providers import Callable
from geoalchemy2.shape import to_shape, from_shape
import shapely


class PortRepository:
    def __init__(self, session_factory: Callable) -> None:
        self.session_factory = session_factory

    def get_port_by_id(self, port_id: int) -> Port | None:
        with self.session_factory() as session:
            entity = session.get(SqlPort, port_id)
            if entity is not None:
                return self.map_to_domain(entity)
            else:
                return None

    def create_port(self, port: Port) -> Port:
        sql_port = self.map_to_sql(port)
        with self.session_factory() as session:
            session.add(sql_port)
            session.commit()
            return self.map_to_domain(sql_port)

    @staticmethod
    def map_to_domain(sql_port: SqlPort) -> Port:
        return Port(
            id=sql_port.id,
            port_name=sql_port.port_name,
            locode=sql_port.locode,
            geometry=to_shape(sql_port.geometry),
            latitude=sql_port.latitude,
            longitude=sql_port.longitude,
            country_iso3=sql_port.country_iso3,
            has_excursion=sql_port.has_excursion,
            created_at=sql_port.created_at,
            updated_at=sql_port.updated_at,
        )

    @staticmethod
    def map_to_sql(port: Port) -> SqlPort:
        return SqlPort(
            port_name=port.port_name,
            locode=port.locode,
            geometry=from_shape(port.geometry),
            latitude=port.latitude,
            longitude=port.longitude,
            country_iso3=port.country_iso3,
            has_excursion=port.has_excursion,
            created_at=port.created_at,
            updated_at=port.updated_at,
        )
