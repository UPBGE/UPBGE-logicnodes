# from .parametersocket import NodeSocketLogicParameter
# from .floatpositivesocket import NodeSocketLogicFloatPositive
from .socket import socket_type
from .socket import NodeSocketLogic
from bpy.types import NodeSocket


class NodeSocketLogicDeprecated(NodeSocketLogic):
    bl_label = 'DEPRECATED'
    deprecated = True
    nl_color: list = [1, 0, 0, 1]

    def get_unlinked_value(self):
        return 0.0

    def _draw(self, context, layout, node, text):
        layout.label(text='DEPRECATED!', icon='ERROR')


@socket_type
class NodeSocketLogicExponent(NodeSocket, NodeSocketLogicDeprecated):
    bl_idname = 'NLPositiveStepFloat'

    def get_unlinked_value(self):
        return 1.0


@socket_type
class NodeSocketLogicMouseWheelDirection(NodeSocket, NodeSocketLogicDeprecated):
    bl_idname = 'NLSocketMouseWheelDirection'

    def get_unlinked_value(self):
        return 3


@socket_type
class NodeSocketLogicMaterialSlot(NodeSocket, NodeSocketLogicDeprecated):
    bl_idname = 'NLCountSocket'

    def get_unlinked_value(self):
        return 0


@socket_type
class NodeSocketLogicOptionalFloatVal(NodeSocket, NodeSocketLogicDeprecated):
    bl_idname = 'NLSocketOptionalPositiveFloat'

    def get_unlinked_value(self):
        return 1.0


@socket_type
class NodeSocketLogicDistanceCheck(NodeSocket, NodeSocketLogicDeprecated):
    bl_idname = 'NLSocketDistanceCheck'

    def get_unlinked_value(self):
        return 0


@socket_type
class NodeSocketLogicReadableAttr(NodeSocket, NodeSocketLogicDeprecated):
    bl_idname = 'NLSocketReadableMemberName'

    def get_unlinked_value(self):
        return "'worldPosition'"


@socket_type
class NodeSocketLogicFormatPosFloat(NodeSocket, NodeSocketLogicDeprecated):
    bl_idname = 'NLPosFloatFormatSocket'

    def get_unlinked_value(self):
        return 1.0


@socket_type
class NodeSocketLogicConstraintType(NodeSocket, NodeSocketLogicDeprecated):
    bl_idname = 'NLConstraintTypeSocket'

    def get_unlinked_value(self):
        return '"bge.constraints.POINTTOPOINT_CONSTRAINT"'


@socket_type
class NodeSocketLogicTypeCast(NodeSocket, NodeSocketLogicDeprecated):
    bl_idname = 'NLTypeCastSocket'

    def get_unlinked_value(self):
        return '"bool"'


@socket_type
class NodeSocketLogicQuality(NodeSocket, NodeSocketLogicDeprecated):
    bl_idname = 'NLQualitySocket'

    def get_unlinked_value(self):
        return 0


@socket_type
class NodeSocketLogicVsync(NodeSocket, NodeSocketLogicDeprecated):
    bl_idname = 'NLVSyncSocket'

    def get_unlinked_value(self):
        return '"bge.render.VSYNC_ON"'