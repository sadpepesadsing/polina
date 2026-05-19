from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from models.entities import ScheduleItem


class ScheduleService(ABC):
    @abstractmethod
    def get_published_schedule(self, group_filter: str = "") -> List[ScheduleItem]:
        raise NotImplementedError
