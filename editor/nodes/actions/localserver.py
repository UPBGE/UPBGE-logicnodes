from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicInteger
from ...sockets import NodeSocketLogicPython
from ...sockets import NodeSocketLogicDictionary
from bpy.props import BoolProperty
from socket import gethostbyname, gethostname


@node_type
class LogicNodeLocalServer(LogicNodeActionType):
    bl_idname = "LogicNodeLocalServer"
    bl_label = "LAN Server"
    nl_module = 'uplogic.nodes.actions'

    on_init: BoolProperty(
        name='Startup',
        description='Start the server on game start',
        default=True
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Start")
        self.add_input(NodeSocketLogicString, "IP", {'value': gethostbyname(gethostname())})
        self.add_input(NodeSocketLogicInteger, "Port", {'default_value': 8303})
        self.add_input(NodeSocketLogicCondition, "Stop")
        self.add_output(NodeSocketLogicCondition, "On Start")
        self.add_output(NodeSocketLogicCondition, "Running")
        self.add_output(NodeSocketLogicCondition, "On Stop")
        self.add_output(NodeSocketLogicPython, "Server")
        self.add_output(NodeSocketLogicCondition, "Received")
        self.add_output(NodeSocketLogicDictionary, "Message")
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'on_init', text='On Startup')

    nl_class = "ULLocalServer"

    def get_input_names(self):
        return [
            "start_cond",
            "ip_address",
            "port",
            "stop_cond",
        ]

    def get_attributes(self):
        return [
            ("on_init", f'{self.on_init}')
        ]

    def get_output_names(self):
        return ['STARTED', 'RUNNING', 'STOPPED', 'SERVER', 'RECEIVED', 'MSG']
