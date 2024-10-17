from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicMaterial
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicCondition
from ..node import LogicNodeConditionType
from ..node import node_type
from bpy.props import BoolProperty


@node_type
class LogicNodeCollision(LogicNodeConditionType):
    bl_idname = "NLConditionCollisionNode"
    bl_label = "Collision"
    bl_description = 'Register if a collision happens with an object'
    nl_module = 'uplogic.nodes.conditions'
    nl_class = "ULCollision"

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.inputs[2].enabled = not self.inputs[1].default_value
        self.inputs[3].enabled = self.inputs[1].default_value

    pulse: BoolProperty(name='Continuous', update=update_draw)

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object", 'game_object')
        self.add_input(NodeSocketLogicBoolean, 'Use Material', 'use_mat')
        self.add_input(NodeSocketLogicString, "Property", 'prop')
        self.add_input(NodeSocketLogicMaterial, 'Material', 'material')
        self.add_output(NodeSocketLogicCondition, "On Collision", 'COLLISION')
        self.add_output(NodeSocketLogicObject, "Colliding Object", 'TARGET')
        self.add_output(NodeSocketLogicList, "Colliding Objects", 'OBJECTS')
        self.add_output(NodeSocketLogicVectorXYZ, "Point", 'POINT')
        self.add_output(NodeSocketLogicVectorXYZ, "Normal", 'NORMAL')
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "pulse", text="Continuous")

    # XXX: Remove for 5.0
    def get_input_names(self):
        return ["game_object", 'use_mat', 'prop', 'material']

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ["COLLISION", "TARGET", "OBJECTS", "POINT", "NORMAL"]

    def get_attributes(self):
        return [("pulse", self.pulse)]
