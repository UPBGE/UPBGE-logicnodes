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
    bl_description = 'Manage a Local Area Network (LAN) server'
    bl_width_default = 180
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULLocalServer"

    on_init: BoolProperty(
        name='Startup',
        description='Start the server on game start',
        default=True
    )

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Start", 'start_cond')
        self.add_input(NodeSocketLogicString, "IP", 'ip_address', {'default_value': gethostbyname(gethostname())})
        self.add_input(NodeSocketLogicInteger, "Port", 'port', {'default_value': 8303})
        self.add_input(NodeSocketLogicCondition, "Stop", 'stop_cond')
        self.add_output(NodeSocketLogicCondition, "On Start", 'STARTED')
        self.add_output(NodeSocketLogicCondition, "Running", 'RUNNING')
        self.add_output(NodeSocketLogicCondition, "On Stop", 'STOPPED')
        self.add_output(NodeSocketLogicPython, "Server", 'SERVER')
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
            "start_cond",
            "ip_address",
            "port",
            "stop_cond",
        ]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['STARTED', 'RUNNING', 'STOPPED', 'SERVER', 'RECEIVED', 'MSG']
