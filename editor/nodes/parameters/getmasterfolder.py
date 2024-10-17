from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicString


@node_type
class LogicNodeGetMasterFolder(LogicNodeParameterType):
    bl_idname = "LogicNodeGetMasterFolder"
    bl_label = "Get Master Folder"
    bl_description = "Go up from this file's save location until in a folder with the given name"
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "GetMasterFolderNode"

    def init(self, context):
        self.add_input(NodeSocketLogicString, 'Name', 'name', settings={'default_value': 'Data'})
        self.add_output(NodeSocketLogicString, "Path", 'PATH')
        LogicNodeParameterType.init(self, context)
