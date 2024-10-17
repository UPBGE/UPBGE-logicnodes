from ..node import node_type
from ..node import LogicNodeActionType
from ...sockets import NodeSocketLogicCondition
from ...sockets import NodeSocketLogicMaterial
from ...sockets import NodeSocketLogicTreeNode
from ...sockets import NodeSocketLogicPlayMode
from ...sockets import NodeSocketLogicParameter
from ...sockets import NodeSocketLogicBoolean
from ...sockets import NodeSocketLogicVectorXY
from ...sockets import NodeSocketLogicFloatPositive
import bpy


@node_type
class LogicNodePlaySequence(LogicNodeActionType):
    bl_idname = "NLPlayMaterialSequence"
    bl_label = "Play Sequence"
    bl_description = 'Start an animation on a material texture node'
    nl_module = 'uplogic.nodes.actions'
    nl_class = "ULPaySequence"

    def init(self, context):
        self.add_input(NodeSocketLogicCondition, "Condition", 'condition')
        self.add_input(NodeSocketLogicMaterial, 'Material', 'mat_name')
        self.add_input(NodeSocketLogicTreeNode, 'Node Name', 'node_name', {'ref_index': 1})
        self.add_input(NodeSocketLogicPlayMode, "Mode", 'play_mode', {'enabled': False})
        self.add_input(NodeSocketLogicBoolean, 'Continue', 'play_continue', {'enabled': False})
        self.add_input(NodeSocketLogicVectorXY, "Frames", 'frames', {'enabled': False})
        self.add_input(NodeSocketLogicFloatPositive, "FPS", 'fps', {'enabled': False, 'default_value': 60})
        self.add_output(NodeSocketLogicCondition, "On Start", 'ON_START')
        self.add_output(NodeSocketLogicCondition, "Running", 'RUNNING')
        self.add_output(NodeSocketLogicCondition, "On Finish", 'ON_FINISH')
        self.add_output(NodeSocketLogicParameter, "Current Frame", 'FRAME')
        LogicNodeActionType.init(self, context)

    def draw_buttons(self, context, layout):
        mat = self.inputs[1].default_value
        if mat:
            nde = self.inputs[2].default_value
            target = mat.node_tree.nodes.get(nde)
            if not (
                isinstance(target, bpy.types.ShaderNodeTexImage)
                or
                isinstance(target, bpy.types.ShaderNodeSpritesAnimation)
            ):
                col = layout.column()
                col.label(text='Selected Node', icon='ERROR')
                col.label(text='not playable!')

    def update_draw(self, context=None):
        if not self.ready:
            return
        mat = self.inputs[1]
        nde = self.inputs[2]
        mod = self.inputs[3]
        fra = self.inputs[5]
        fps = self.inputs[6]
        subs = [mod, fra, fps]
        target = mat.default_value.node_tree.nodes.get(nde.default_value) if mat.default_value else None
        valid = (
            isinstance(target, bpy.types.ShaderNodeTexImage)
            or
            isinstance(target, bpy.types.ShaderNodeSpritesAnimation)
        )
        self.inputs[4].enabled = '3' in mod.default_value
        if (mat.default_value or mat.is_linked) and (nde.default_value or nde.is_linked) and valid:
            for ipt in subs:
                ipt.enabled = True
        else:
            for ipt in subs:
                ipt.enabled = False

    # XXX: Remove for 5.0
    def get_input_names(self):
        return [
            "condition",
            "mat_name",
            'node_name',
            'play_mode',
            'play_continue',
            "frames",
            'fps'
        ]

    # XXX: Remove for 5.0
    def get_output_names(self):
        return ['ON_START', 'RUNNING', 'ON_FINISH', 'FRAME']
