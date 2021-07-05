from time import sleep
from typing import Dict, Any
from uuid import UUID

from unipipeline.modules.uni_definition import UniDefinition
from unipipeline.modules.uni_echo import UniEcho
from unipipeline.modules.uni_module_definition import UniModuleDefinition
from unipipeline.modules.uni_wating import UniWaiting


class UniWaitingDefinition(UniDefinition):
    id: UUID
    name: str
    retry_max_count: int
    retry_delay_s: int
    type: UniModuleDefinition

    _dynamic_props_: Dict[str, Any]

    def __hash__(self) -> int:
        return hash(self.id)

    def wait(self, echo: UniEcho) -> None:
        waiting_type = self.type.import_class(UniWaiting, echo)
        for try_count in range(self.retry_max_count):
            try:
                w = waiting_type()
                w.try_to_connect()
                echo.log_info(f'access to {self.name} was reached')
                return
            except ConnectionError:
                echo.log_debug(f'retry wait for {self.name} [{try_count}/{self.retry_max_count}]')
                sleep(self.retry_delay_s)
                continue
        raise ConnectionError('unavailable connection to %s', waiting_type.__name__)
