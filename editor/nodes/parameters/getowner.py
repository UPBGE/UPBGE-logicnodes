from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicObject


@node_type
class LogicNodeGetOwner(LogicNodeParameterType):
    """The owner of this logic tree.
    Each Object that has this tree installed is
    the "owner" of a logic tree
    """
    bl_idname = "NLOwnerGameObjectParameterNode"
    bl_label = "Get Owner"
    bl_icon = 'USER'
    nl_module = 'parameters'

    def init(self, context):
        self.add_output(NodeSocketLogicObject, "Owner Object")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULGetOwner"
