from mathutils import Vector
from uplogic.nodes import ULOutSocket
from uplogic.nodes import ULParameterNode
from uplogic.utils import STATUS_WAITING
from uplogic.utils import is_invalid


class ULObjectDataVertices(ULParameterNode):
    def __init__(self):
        ULParameterNode.__init__(self)
        self.game_object = None
        self.OUT = ULOutSocket(self, self.get_data)

    def get_data(self):
        obj = self.get_socket_value(self.game_object)
        if is_invalid(obj):
            return STATUS_WAITING
        offset = obj.worldPosition
        return (
            sorted(
                [Vector(v.co) + offset for v in (
                    obj
                    .blenderObject
                    .data
                    .vertices
                )]
            )
        )

    def evaluate(self):
        self._set_ready()
