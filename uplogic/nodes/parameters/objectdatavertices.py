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
        socket = self.get_output('data')
        if socket is None:
            obj = self.get_input(self.game_object)
            if is_invalid(obj):
                return STATUS_WAITING
            offset = obj.worldPosition
            return self.set_output(
                'data',
                (
                    sorted(
                        [Vector(v.co) + offset for v in (
                            obj
                            .blenderObject
                            .data
                            .vertices
                        )]
                    )
                )
            )
        return socket

    def evaluate(self):
        self._set_ready()
