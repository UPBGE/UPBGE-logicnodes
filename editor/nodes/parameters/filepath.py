from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFilePath


@node_type
class LogicNodeFilePath(LogicNodeParameterType):
    bl_idname = "NLParameterFileValue"
    bl_label = "File Path"
    nl_module = 'uplogic.nodes.parameters'

    def init(self, context):
        self.add_input(NodeSocketLogicFilePath, "")
        self.add_output(NodeSocketLogicFilePath, "Path")
        LogicNodeParameterType.init(self, context)

    nl_class = "ULSimpleValue"

    def get_input_names(self):
        return ["value"]

    def get_output_names(self):
        return ["OUT"]
