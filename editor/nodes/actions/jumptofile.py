from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFilePath


@node_type
class LogicNodeJumpToFile(LogicNodeActionType):
    bl_idname = "NLActionStartGame"
    bl_label = "Load Blender File"
    bl_description = 'Load up another .blend file'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULLoadBlendFile"

    search_tags = [
        ['Load Into File', {}],
        ['Jump to File', {}],
        ['Load File', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicFilePath, "File Name", 'file_name')
        self.add_output(NodeSocketLogicCondition, 'Done', 'OUT', {'enabled': False})
        LogicNodeActionType.init(self, context)

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["OUT"]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["condition", "file_name"]
