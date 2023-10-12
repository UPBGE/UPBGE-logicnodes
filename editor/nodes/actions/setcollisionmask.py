from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBitMask


@node_type
class LogicNodeSetCollisionMask(LogicNodeActionType):
    bl_idname = "NLSetCollisionMask"
    bl_label = "Set Collision Mask"
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULSetCollisionMask"
    deprecated = True
    deprecation_message = 'Replaced by "Set Collision" Node'

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, 'Condition')
        self.add_input(NodeSocketLogicObject, 'Object')
        self.add_input(NodeSocketLogicBitMask, 'Mask')
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]


    def get_input_names(self):
        return ["condition", "game_object", 'slots']
