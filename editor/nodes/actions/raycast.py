from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCamera
from ...sockets import NodeSocketLogicFloatFactor
from ...sockets import NodeSocketLogicList
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicObject
from ...sockets import NodeSocketLogicVectorXYZ
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicString
from ...sockets import NodeSocketLogicMaterial
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicFloatPositive
from ...sockets import NodeSocketLogicBitMask
from mathutils import Vector
from bpy.props import EnumProperty
from bpy.props import BoolProperty


_modes = [
    ("0", "Simple", "Cast a straight ray from one point to another"),
    ("1", "Projectile", "Cast a ray that is affected by gravity"),
    None,
    ("2", "Mouse", "Cast a straight ray towards the mouse position"),
    ("3", "Screen", "Cast a straight ray towards a point on the screen")
]


@node_type
class LogicNodeRaycast(LogicNodeActionType):
    bl_idname = "LogicNodeRaycast"
    bl_label = "Raycast"
    bl_description = 'Perform a raycast'
    nl_class = "RaycastNode"
    nl_module = 'uplogic.nodes.actions'
    bl_width_default = 180

    def update_draw(self, context=None):
        if not self.ready:
            return
        mode = int(self.mode)
        face_data = self.face_data
        camera = self.inputs[2]
        origin = self.inputs[3]
        target = self.inputs[4]
        aim = self.inputs[5]
        power = self.inputs[6]
        resolution = self.inputs[7]
        local = self.inputs[8]
        custom_distance = self.inputs[12]
        distance = self.inputs[13]
        custom_gravity = self.inputs[14]
        gravity = self.inputs[15]
        visualize = self.inputs[17]

        camera.enabled = mode >= 2
        origin.enabled = mode <= 1
        target.enabled = mode <= 1
        aim.enabled = mode == 3
        power.enabled = mode == 1
        resolution.enabled = mode == 1
        local.enabled = mode <= 1
        custom_distance.enabled = mode == 0
        distance.enabled = mode > 0 or custom_distance.default_value
        custom_gravity.enabled = mode == 1
        gravity.enabled = mode == 1 and custom_gravity.default_value
        visualize.enabled = mode <= 1

        self.outputs[5].enabled = face_data
        self.outputs[6].enabled = face_data
        self.outputs[7].enabled = mode == 1

    mode: EnumProperty(items=_modes, name="Mode", description="Type of ray", update=update_draw)
    face_data: BoolProperty(name="Use Face Data", description="A", update=update_draw)

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", "condition")  # 0
        self.add_input(NodeSocketLogicObject, "Caster", 'caster', {'use_owner': True})  # 1
        self.add_input(NodeSocketLogicCamera, "Camera", 'camera', {'use_active': True})  # 2
        self.add_input(NodeSocketLogicVectorXYZ, "Origin", "origin")  # 3
        self.add_input(NodeSocketLogicVectorXYZ, "Target", "target")  # 4
        self.add_input(NodeSocketLogicVectorXY, "Aim", 'aim', {'default_value': (.5, .5)})  # 5
        self.add_input(NodeSocketLogicFloatPositive, "Power", 'power', {'default_value': 10.0})  # 6
        self.add_input(NodeSocketLogicFloatFactor, "Resolution", 'resolution', {'default_value': 0.9})  # 7
        self.add_input(NodeSocketLogicBoolean, "Local", 'local')  # 8
        self.add_input(NodeSocketLogicString, "Property", "property_name")  # 9
        self.add_input(NodeSocketLogicMaterial, "Material", "material")  # 10
        self.add_input(NodeSocketLogicBoolean, 'X-Ray', 'xray')  # 11
        self.add_input(NodeSocketLogicBoolean, "Custom Distance", 'use_custom_distance')  # 12
        self.add_input(NodeSocketLogicFloatPositive, "Distance", 'distance', {'default_value': 100.0})  # 13
        self.add_input(NodeSocketLogicBoolean, "Custom Gravity", 'use_custom_gravity')  # 14
        self.add_input(NodeSocketLogicVectorXYZ, "Gravity", "gravity", {'default_value': Vector((0, 0, -9.81))})  # 15
        self.add_input(NodeSocketLogicBitMask, "Mask", 'mask')  # 16
        self.add_input(NodeSocketLogicBoolean, 'Visualize', 'visualize')  # 17

        # OUTPUTS
        self.add_output(NodeSocketLogicCondition, "Has Result", 'RESULT')  # 0
        self.add_output(NodeSocketLogicObject, "Picked Object", 'PICKED_OBJECT')  # 1
        self.add_output(NodeSocketLogicVectorXYZ, "Picked Point", 'POINT')  # 2
        self.add_output(NodeSocketLogicVectorXYZ, "Picked Normal", 'NORMAL')  # 3
        self.add_output(NodeSocketLogicVectorXYZ, "Ray Direction", 'DIRECTION')  # 4
        self.add_output(NodeSocketLogicMaterial, "Face Material", 'MATERIAL')  # 5
        self.add_output(NodeSocketLogicVectorXY, "UV Coords", 'UV')  # 6
        self.add_output(NodeSocketLogicList, "Parabola Points", 'PARABOLA')  # 7

        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        layout.prop(self, 'mode', text='')
        layout.prop(self, 'face_data', text='Use Face Data')

    def get_attributes(self):
        return [
            ("mode", int(self.mode)),
            ("face_data", self.face_data),
        ]
