from ..node import node_type
from ..node import LogicNodeParameterType
from ...sockets import NodeSocketLogicArmature
from ...sockets import NodeSocketLogicBone
from ...sockets import NodeSocketLogicVectorXYZ


@node_type
class LogicNodeBoneStatus(LogicNodeParameterType):
    bl_idname = "NLParameterBoneStatus"
    bl_label = "Bone Status"
    nl_module = 'uplogic.nodes.parameters'
    bl_description = 'Transformation Status of an Armature Bone'
    nl_class = "ULBoneStatus"
    deprecated = True
    deprecation_message = 'Node will be removed in a future update'

    def init(self, context):
        self.add_input(NodeSocketLogicArmature, "Armature Object")
        self.add_input(NodeSocketLogicBone, "Bone Name")
        self.add_output(NodeSocketLogicVectorXYZ, "Position")
        self.add_output(NodeSocketLogicVectorXYZ, "Rotation")
        self.add_output(NodeSocketLogicVectorXYZ, "Scale")
        LogicNodeParameterType.init(self, context)

    def get_input_names(self):
        return ["armature", "bone_name"]

    def get_output_names(self):
        return ["XYZ_POS", "XYZ_ROT", "XYZ_SCA"]
