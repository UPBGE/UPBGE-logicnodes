from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicStringItem


@node_type
class LogicNodeJoinPath(LogicNodeParameterType):
    bl_idname = "LogicNodeJoinPath"
    bl_label = "Join Path"
    bl_description = 'Joined path from a list of strings'
    nl_module = 'uplogic.nodes.parameters'
    nl_class = "JoinPathNode"

    def init(self, context):
        self.add_input(NodeSocketLogicStringItem, 'Path', 'item')
        self.add_input(NodeSocketLogicStringItem, 'Path', 'item')
        self.add_output(NodeSocketLogicString, 'Path', 'PATH')
        LogicNodeParameterType.init(self, context)

    def draw_buttons(self, context, layout):
        op = layout.operator('logic_nodes.add_socket')
        op.socket_type = 'NodeSocketLogicStringItem'

    def set_new_input_name(self):
        self.inputs[-1].name = 'Path'

    def setup(
        self,
        cell_varname,
        uids
    ):
        items = ''
        for socket in self.inputs:
            field_value = None
            if socket.linked_valid:
                field_value = self.get_linked_value(
                    socket,
                    uids
                )
            else:
                field_value = socket.get_default_value()
            items += f'{field_value}, '
        items = items[:-2]
        return f'        {cell_varname}.items = [{items}]\n'
