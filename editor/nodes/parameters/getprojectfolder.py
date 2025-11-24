from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeGetProjectFolder(LogicNodeParameterType):
    bl_idname = "LogicNodeGetProjectFolder"
    bl_label = "Get Project Folder"
    bl_description = "Go up from this file's save location until in a folder with the given name"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "GetProjectFolderNode"

    def init(self, context):
        self.add_input(NodeSocketLogicString, 'Name', 'name', settings={'default_value': 'Data'})
        self.add_output(NodeSocketLogicString, "Path", 'PATH')
        LogicNodeParameterType.init(self, context)
