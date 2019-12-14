from abc import ABC, abstractmethod

from dash import Dash
from dash.development.base_component import Component


class Widget(ABC):
    @abstractmethod
    def get_layout(self) -> Component:
        pass

    @abstractmethod
    def assign_callbacks(self, app: Dash) -> None:
        pass
