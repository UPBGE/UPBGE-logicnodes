from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicFilePath


@node_type
class LogicNodeFilePath(LogicNodeParameterType):
    bl_idname = "NLParameterFileValue"
    bl_label = "File Path"
    nl_category = "Values"
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicFilePath, "")
        self.add_output(NodeSocketLogicFilePath, "Path")

    def get_netlogic_class_name(self):
        return "ULSimpleValue"

    def get_input_names(self):
        return ["value"]

    def get_output_names(self):
        return ["OUT"]
