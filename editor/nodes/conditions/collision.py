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
    nl_module = 'conditions'

    def update_draw(self, context=None):
        if not self.ready:
            return
        self.inputs[2].enabled = not self.inputs[1].value
        self.inputs[3].enabled = self.inputs[1].value

    pulse: BoolProperty(name='Continuous', update=update_draw)

    def init(self, context):
        self.add_input(NodeSocketLogicObject, "Object")
        self.add_input(NodeSocketLogicBoolean, 'Use Material')
        self.add_input(NodeSocketLogicString, "Property")
        self.add_input(NodeSocketLogicMaterial, 'Material')
        self.add_output(NodeSocketLogicCondition, "On Collision")
        self.add_output(NodeSocketLogicObject, "Colliding Object")
        self.add_output(NodeSocketLogicList, "Colliding Objects")
        self.add_output(NodeSocketLogicVectorXYZ, "Point")
        self.add_output(NodeSocketLogicVectorXYZ, "Normal")
        LogicNodeConditionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, "pulse", text="Continuous")

    nl_class = "ULCollision"

    def get_input_names(self):
        return ["game_object", 'use_mat', 'prop', 'material']

    def get_output_names(self):
        return ["COLLISION", "TARGET", "OBJECTS", "POINT", "NORMAL"]

    def get_attributes(self):
        return [("pulse", self.pulse)]
