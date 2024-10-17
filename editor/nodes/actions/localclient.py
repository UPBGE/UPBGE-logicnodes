from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicIntegerPositive
from ...sockets import NodeSocketLogicPython
from ...sockets import NodeSocketLogicDictionary
from bpy.props import BoolProperty


@node_type
class LogicNodeLocalClient(LogicNodeActionType):
    bl_idname = "LogicNodeLocalClient"
    bl_label = "LAN Client"
    bl_description = 'Manage a Local Area Network (LAN) client'
    bl_width_default = 180
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULLocalClient"

    on_init: BoolProperty(
        name='Startup',
        description='Connect the client on game start',
        default=False
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Connect", 'connect_cond')
        self.add_input(NodeSocketLogicString, "Server", 'ip_address')
        self.add_input(NodeSocketLogicIntegerPositive, "Port", 'port', {'default_value': 8303})
        self.add_input(NodeSocketLogicCondition, "Disconnect", 'disconnect_cond')
        self.add_output(NodeSocketLogicCondition, "On Connect", 'CONNECT')
        self.add_output(NodeSocketLogicCondition, "Connected", 'CONNECTED')
        self.add_output(NodeSocketLogicCondition, "On Disconnect", 'DISCONNECT')
        self.add_output(NodeSocketLogicPython, "Client", 'CLIENT')
        self.add_output(NodeSocketLogicCondition, "Received", 'RECEIVED')
        self.add_output(NodeSocketLogicDictionary, "Data", 'MSG')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'on_init', text='On Startup')

    def get_attributes(self):
        return [
            ("on_init", f'{self.on_init}')
        ]

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "connect_cond",
            "ip_address",
            "port",
            "disconnect_cond",
        ]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['CONNECT', 'CONNECTED', 'DISCONNECT', 'CLIENT', 'RECEIVED', 'MSG']
