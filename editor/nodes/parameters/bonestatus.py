from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicArmature
from ...sockets import NodeSocketLogicBone
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeBoneStatus(LogicNodeParameterType):
    bl_idname = "NLParameterBoneStatus"
    bl_label = "Bone Status"
    nl_category = 'Animation'
    nl_subcat = 'Armature / Rig'
    nl_module = 'parameters'

    def init(self, context):
        LogicNodeParameterType.init(self, context)
        self.add_input(NodeSocketLogicArmature, "Armature Object")
        self.add_input(NodeSocketLogicBone, "Bone Name")
        self.add_output(NodeSocketLogicVectorXYZ, "Position")
        self.add_output(NodeSocketLogicVectorXYZ, "Rotation")
        self.add_output(NodeSocketLogicVectorXYZ, "Scale")

    def get_netlogic_class_name(self):
        return "ULBoneStatus"

    def get_input_names(self):
        return ["armature", "bone_name"]

    def get_output_names(self):
        return ["XYZ_POS", "XYZ_ROT", "XYZ_SCA"]
