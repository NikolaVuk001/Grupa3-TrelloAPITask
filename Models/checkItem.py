from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class CheckItem:
    id: str
    name: str
    state: str
