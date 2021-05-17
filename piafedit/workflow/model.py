import uuid
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Slot:
    _id: str = str(uuid.uuid4())
    connection = None

    def connect(self, other: 'Slot'):
        self.connection = other

    def disconnect(self):
        self.connection = None

    def clone(self):
        return Slot()


@dataclass
class Func:
    name: str
    inputs: List[Slot]
    out: Optional[Slot] = Slot()

    def clone(self):
        return Func(
            self.name,
            inputs=[s.clone() for s in self.inputs],
            out=self.out.clone()
        )


class Workflow:
    items: List[Func] = []

    def source(self, name: str):
        x = Func(name, inputs=[])
        self.items.append(x)
        return x

    def sink(self, name: str):
        x = Func(
            name,
            inputs=[Slot()],
            out=None
        )
        self.items.append(x)
        return x
