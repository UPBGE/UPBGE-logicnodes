from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicVectorXYZ
from bpy.props import FloatVectorProperty
from bpy.props import EnumProperty


vector_dimensions = [
    ('0', '2D Vector', ''),
    ('1', '3D Vector', ''),
    ('2', '4D Vector', '')
]


@node_type
class LogicNodeVector(LogicNodeParameterType):
    bl_idname = "LogicNodeVector"
    bl_label = "Vector"
    nl_module = 'uplogic.nodes.parameters'
    bl_description = 'Define a constant vector'
    nl_class = "VectorNode"

    vector_xy: FloatVectorProperty(name='2D Vector', size=2, subtype='XYZ')
    vector_xyz: FloatVectorProperty(name='3D Vector', subtype='XYZ')
    vector_xyzw: FloatVectorProperty(name='4D Vector', size=4, subtype='XYZ')

    mode: EnumProperty(name='Mode', items=vector_dimensions, description='Select a type of vector')

    def draw_buttons(self, context, layout) -> None:
        layout.prop(self, 'mode', text='')
        mode = int(self.mode)
        col = layout.column()
        if mode == 0:
            col.prop(self, 'vector_xy', text='')
        elif mode == 1:
            col.prop(self, 'vector_xyz', text='')
        elif mode == 2:
            col.prop(self, 'vector_xyzw', text='')

    def init(self, context):
        self.add_output(NodeSocketLogicVectorXYZ, "Vector", 'OUT')
        LogicNodeParameterType.init(self, context)

    def get_attributes(self):
        vec = ''
        match int(self.mode):
            case 0:
                vec = f'Vector(({self.vector_xy[0], self.vector_xy[1]}))'
            case 1:
                vec = f'Vector(({self.vector_xyz[0], self.vector_xyz[1], self.vector_xyz[2]}))'
            case 2:
                vec = f'Vector(({self.vector_xyzw[0], self.vector_xyzw[1], self.vector_xyzw[2], self.vector_xyzw[3]}))'
        return [
            ('vector', vec)
        ]
