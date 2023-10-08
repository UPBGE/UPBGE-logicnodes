from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicFilePath


@node_type
class LogicNodeJumpToFile(LogicNodeActionType):
    bl_idname = "NLActionStartGame"
    bl_label = "Jump To File"
    nl_category = "Game"
    nl_module = 'actions'
    nl_class = "ULLoadBlendFile"

    search_tags = [
        ['Load Into File', {}],
        ['Jump to File', {}],
        ['Load File', {}]
    ]

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition")
        self.add_input(NodeSocketLogicFilePath, "File name")
        self.add_output(NodeSocketLogicCondition, 'Done')
        LogicNodeActionType.init(self, context)

    def get_output_names(self):
        return ["OUT"]

    def get_input_names(self):
        return ["condition", "file_name"]
