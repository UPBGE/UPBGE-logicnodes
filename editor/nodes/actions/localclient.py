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
    nl_module = 'uplogic.nodes.actions'

    on_init: BoolProperty(
        name='Startup',
        description='Connect the client on game start',
        default=False
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Connect")
        self.add_input(NodeSocketLogicString, "IP")
        self.add_input(NodeSocketLogicIntegerPositive, "Port", {'value': 8303})
        self.add_input(NodeSocketLogicCondition, "Disconnect")
        self.add_output(NodeSocketLogicCondition, "On Connect")
        self.add_output(NodeSocketLogicCondition, "Connected")
        self.add_output(NodeSocketLogicCondition, "On Disconnect")
        self.add_output(NodeSocketLogicPython, "Client")
        self.add_output(NodeSocketLogicCondition, "Received")
        self.add_output(NodeSocketLogicDictionary, "Message")
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'on_init', text='On Startup')

    nl_class = "ULLocalClient"

    def get_input_names(self):
        return [
            "connect_cond",
            "ip_address",
            "port",
            "disconnect_cond",
        ]

    def get_attributes(self):
        return [
            ("on_init", f'{self.on_init}')
        ]

    def get_output_names(self):
        return ['CONNECT', 'CONNECTED', 'DISCONNECT', 'CLIENT', 'RECEIVED', 'MSG']
