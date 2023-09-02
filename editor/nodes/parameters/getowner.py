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
    nl_category = "Objects"
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_output(NodeSocketLogicObject, "Owner Object")

    def get_netlogic_class_name(self):
        return "ULGetOwner"
