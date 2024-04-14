from enum import Enum
import copy


class RouteType(Enum):
    LAND = "Суша"
    WATER = "Море"
    MIXED = "Смешанный"


class Route:
    def __init__(
        self,
        city_from_name: str,
        city_to_name: str,
        length: float,
        route_type: RouteType,
        *,
        disaster_risk: float | None = None,
        assault_risk: float | None = None,
        disaster_risk_per_unit: float | None = None,
        assault_risk_per_unit: float | None = None,
    ):
        assert length >= 0
        self.length = length
        if disaster_risk is None:
            assert disaster_risk_per_unit is not None, "disaster_risk or disaster_risk_per_unit should be defined"
            assert 0 <= disaster_risk_per_unit <= 1, "Disaster risk should be between 0 and 1"
            self.disaster_risk = min(self.length * disaster_risk_per_unit, 1)
        else:
            self.disaster_risk = disaster_risk
        if assault_risk is None:
            assert assault_risk_per_unit is not None, "assault_risk or assault_risk_per_unit should be defined"
            assert 0 <= assault_risk_per_unit <= 1, "Assault risk should be between 0 and 1"
            self.assault_risk = min(self.length * assault_risk_per_unit, 1)
        else:
            self.assault_risk = assault_risk
        self.city_from: str = city_from_name
        self.city_to: str = city_to_name
        self.length: float = length
        self.route_type: RouteType = route_type

    def get_reverse(self):
        copy_root = copy.copy(self)
        copy_root.city_from = self.city_to
        copy_root.city_to = self.city_from
        return copy_root

    def get_cumulative_risk(self, with_disaster: bool = True, with_assault: bool = True):
        return 1 - (1 - (self.disaster_risk if with_disaster else 0)) * (1 - (self.assault_risk if with_assault else 0))


def join_route_type(first: RouteType, second: RouteType):
    if first == second:
        return first
    else:
        return RouteType.MIXED


def connect_routes(first: Route, second: Route) -> Route:
    assert first.city_to == second.city_from
    return Route(
        city_from_name=first.city_from,
        city_to_name=second.city_to,
        length=first.length + second.length,
        route_type=join_route_type(first.route_type, second.route_type),
        disaster_risk=1 - (1 - first.disaster_risk) * (1 - second.disaster_risk),
        assault_risk=1 - (1 - first.assault_risk) * (1 - second.assault_risk),
    )
