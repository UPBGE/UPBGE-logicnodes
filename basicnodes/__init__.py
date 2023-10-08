# import math
# import bpy
# import bge_netlogic
# from bge_netlogic import utilities as utils
# from  bge_netlogic.utilities import ERROR_MESSAGES, WARNING_MESSAGES
# from ui import LogicNodeTree
# from bpy.props import StringProperty
# from bpy.props import BoolProperty
# from bpy.props import EnumProperty
# import socket  # used for automatically setting IP address for server node

# INVALID = 'INVALID'

# CONDITION_NODE_COLOR = utils.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
# PARAMETER_NODE_COLOR = utils.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
# ACTION_NODE_COLOR = utils.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]
# PYTHON_NODE_COLOR = utils.Color.RGBA(0.2, 0.2, 0.2, 1)[:-1]


# _nodes = []


# _enum_look_axis = [
#     ("0", "X Axis", "The Local X Axis [Integer Value 0]"),
#     ("1", "Y Axis", "The Local Y Axis [Integer Value 1]")
# ]

# _enum_vector_types = [
#     ("0", "Vector", "Vector XYZ"),
#     ("1", "Euler", "Euler XYZ")
# ]

# _enum_local_oriented_axis = [
#     ("0", "+X Axis", "The Local X Axis [Integer Value 0]"),
#     ("1", "+Y Axis", "The Local Y Axis [Integer Value 1]"),
#     ("2", "+Z Axis", "The Local Z Axis [Integer Value 2]"),
#     ("3", "-X Axis", "The Local X Axis [Integer Value 3]"),
#     ("4", "-Y Axis", "The Local Y Axis [Integer Value 4]"),
#     ("5", "-Z Axis", "The Local Z Axis [Integer Value 5]")
# ]

# _enum_mouse_wheel_direction = [
#     ("1", "Scroll Up", "Mouse Wheel Scrolled Up [1]"),
#     ("2", "Scroll Down", "Mouse Wheel Scrolled Down [2]"),
#     ("3", "Scroll Up or Down", "Mouse Wheel Scrolled either Up or Down[3]")
# ]


# _enum_vector_math_options = [
#     ("scale", "Scale", "A multiplied by Scale"),
#     ("length", "Length", "Length of A"),
#     ("distance", "Distance", "Distance between A and B"),
#     None,
#     ("dot", "Dot Product", "A dot B"),
#     ("faceforward", "Faceforward", "Orients a vector A to point away from a surface B as defined by its normal C. Returns A if A.dot(B) < 0 else -A"),
#     ("refract", "Refract", "For a given incident vector A, a surface normal B and ratio of indices of refraction, Ior, refract returns the refraction vector, R"),
#     ("reflect", "Reflect", "Reflect A around the normal B. B doesn't need to be normalized"),
#     ("project", "Project", "Project this vector onto another"),
#     ("cross", "Cross Product", "Project A onto B"),
#     None,
#     ("multadd", "Multiply Add", "A * B + C"),
#     ("divide", "Divide", "Entry-wise divide"),
#     ("multiply", "Multiply", "Entry-wise multiply"),
#     ("subtract", "Subtract", "A - B"),
#     ("add", "Add", "A + B"),
#     ("", "Operation", ""),
#     None,
#     ("normalize", "Normalize", "Rescale all values to 0 - 1"),
#     ("lerp", "Lerp", "Linear Interpolation between the two vectors"),
#     ("slerp", "Spherical Lerp", "Spherical Interpolation between the two vectors"),
#     ("negate", "Negate", "Multiply all values by -1")
# ]


# _enum_type_casts = [
#     ("int", "To Integer", "Convert this value to an integer type"),
#     ("bool", "To Boolean", "Convert this value to a boolean type"),
#     ("str", "To String", "Convert this value to a string type"),
#     ("float", "To Float", "Convert this value to a float type")
# ]


# _enum_object_property_types = [
#     ('0', 'Game Property', 'Edit Game Property'),
#     ('1', 'Attribute', 'Edit Internal Attribute (can be used in materials)')
# ]


# _enum_2d_filters = [
#     ('FXAA', 'FXAA', 'Fast Anti-Aliasing'),
#     ('HBAO', 'HBAO', 'Horizon-Based Ambient Occlusion'),
#     ('SSAO', 'SSAO', 'Screen-Space Ambient Occlusion'),
#     ('VIGNETTE', 'Vignette', 'Fade to color at screen edges'),
#     ('BRIGHTNESS', 'Brightness', 'Overall brightness'),
#     ('CHROMAB', 'Chromatic Aberration', 'Lens light bending effect'),
#     ('GRAYSCALE', 'Grayscale', 'Convert image to grayscale'),
#     ('LEVELS', 'Levels', 'Control color levels'),
#     ('MIST', 'Mist', 'Classic depth fog implementation')
# ]


# _enum_constraint_types = [
#     (
#         "bge.constraints.POINTTOPOINT_CONSTRAINT",
#         "Ball",
#         "Allow rotation around all axis"
#     ),
#     (
#         "bge.constraints.LINEHINGE_CONSTRAINT",
#         "Hinge",
#         "Work on one plane, allow rotations on one axis only"
#     ),
#     (
#         "bge.constraints.CONETWIST_CONSTRAINT",
#         "Cone Twist",
#         (
#             'Allow rotations around all axis with limits for the cone '
#             'and twist axis'
#         )
#     ),
#     (
#         "bge.constraints.GENERIC_6DOF_CONSTRAINT",
#         "Generic 6 DOF",
#         "No constraints by default, limits can be set individually"
#     )
# ]

# _enum_vehicle_axis = [
#     ("REAR", "Rear", "Apply to wheels without steering"),
#     ("FRONT", "Front", "Apply to wheels with steering"),
#     ("ALL", "All", "Apply to all wheels")
# ]


# _enum_readable_member_names = [
#     ("worldPosition", "Position (Global)", "The World Position of the object"),
#     ("localPosition", "Position (Local)", "The local position of the object"),
#     (
#         "worldOrientation",
#         "Rotation (Global)",
#         "The World Orientation of the object"
#     ), (
#         "localOrientation",
#         "Rotation (Local)",
#         "The local orientation of the object"
#     ), (
#         "worldLinearVelocity",
#         "Linear Velocity (Global)",
#         "The local linear velocity of the object"
#     ), (
#         "localLinearVelocity",
#         "Linear Velocity (Local)",
#         "The local linear velocity of the object"
#     ), (
#         "worldAngularVelocity",
#         "Angular Velocity (Global)",
#         "The local angular velocity of the object"
#     ), (
#         "localAngularVelocity",
#         "Angular Velocity (Local)",
#         "The local angular velocity of the object"
#     ), (
#         "worldTransform",
#         "Transform (Global)",
#         (
#             'The World Transform of the '
#             'object'
#         )
#     ), (
#         "localTransform",
#         "Transform (Local)",
#         (
#             'The local transform of the '
#             'object'
#         )
#     ),
#     ("worldScale", "World Scale", "The global scale of the object"),
#     ("localScale", "Local Scale", "The local scale of the object"),
#     ("name", "Name", "The name of the object"),
#     ("color", "Color", "The solid color of the object"),
#     (
#         "visible",
#         "Visibility",
#         "True if the object is set to visible, False if it is set of invisible"
#     )
# ]

# _enum_writable_member_names = [
#     ("color", "Color", "The solid color of the object"),
#     ("worldPosition", "Position (Global)", "The World Position of the object"),
#     ("localPosition", "Position (Local)", "The local position of the object"),
#     (
#         "worldOrientation",
#         "Rotation (Global)",
#         "The World Orientation of the object"
#     ), (
#         "localOrientation",
#         "Rotation (Local)",
#         "The local orientation of the object"
#     ), (
#         "worldLinearVelocity",
#         "Linear Velocity (Global)",
#         "The local linear velocity of the object"
#     ), (
#         "localLinearVelocity",
#         "Linear Velocity (Local)",
#         "The local linear velocity of the object"
#     ), (
#         "worldAngularVelocity",
#         "Angular Velocity (Global)",
#         "The local rotational velocity of the object"
#     ), (
#         "localAngularVelocity",
#         "Angular Velocity (Local)",
#         "The local rotational velocity of the object"
#     ), (
#         "worldTransform",
#         "Transform (Global)",
#         (
#             'The World Transform of the '
#             'object'
#         )
#     ), (
#         "localTransform",
#         "Transform (Local)",
#         (
#             'The local transform of the '
#             'object'
#         )
#     ),
#     ("worldScale", "Scale", "The global scale of the object")
# ]

# _enum_vsync_modes = [
#     ("bge.render.VSYNC_OFF", "Off", "Disable Vsync"),
#     ("bge.render.VSYNC_ON", "On", "Enable Vsync"),
#     (
#         "bge.render.VSYNC_ADAPTIVE",
#         "Adaptive",
#         (
#             'Enable adaptive Vsync '
#             '(if supported)'
#         )
#     )
# ]

# _enum_string_ops = [
#     ("0", "Postfix", "Insert A after String"),
#     ("1", "Prefix", "Insert A before String"),
#     ("2", "Infix", "Insert A before String, B after String."),
#     ("3", "Remove Last", "Remove Last Character from String"),
#     ("4", "Remove First", "Remove First Character from String"),
#     (
#         "5",
#         "Replace",
#         'Replace all occurences of A with B'
#     ),
#     ("6", "Upper Case", "Convert to Upper Case"),
#     ("7", "Lower Case", "Convert to Lower Case"),
#     (
#         "8",
#         "Remove Range",
#         'Remove characters from index A to index B'
#     ),
#     (
#         "9",
#         "Insert At",
#         "Insert A at index B"
#     ),
#     (
#         "10",
#         "Length",
#         "Character Count (returns a Number)"
#     ),
#     (
#         "11",
#         "Substring",
#         "Characters between index A and index B"
#     ),
#     (
#         "12",
#         "First Index Of",
#         "Position of the first occurence of A"
#     ),
#     (
#         "13",
#         "Last Index Of",
#         "Position of the last occurence of A"
#     )
# ]

# _enum_math_operations = [
#     ("ADD", "Add", "Sum A and B"),
#     ("SUB", "Subtract", "Subtract B from A"),
#     ("DIV", "Divide", "Divide A by B"),
#     ("MUL", "Multiply", "Multiply A by B"),
#     ("POW", "Power", "A to the power of B"),
#     ("MOD", "Modulo", "Modulo of A by B"),
#     ("FDIV", "Floor Divide", "Floor Divide A by B"),
#     ("MATMUL", "Matrix Multiply", "Transform A by B")
# ]

# _enum_greater_less = [
#     ("GREATER", "Greater", "Value greater than Threshold"),
#     ("LESS", "Less", "Value less than Threshold")
# ]

# _enum_in_or_out = [
#     ("INSIDE", "Within", "Value is within Range"),
#     ("OUTSIDE", "Outside", "Value is outside Range")
# ]

# _enum_logic_operators = [
#     ("0", "Equal", "A equals B"),
#     ("1", "Not Equal", "A not equals B"),
#     ("2", "Greater Than", "A greater than B"),
#     ("3", "Less Than", "A less than B"),
#     ("4", "Greater or Equal", "A greater or equal to B"),
#     ("5", "Less or Equal", "A less or equal to B")
# ]


# _enum_controller_stick_operators = [
#     ("0", "Left Stick", "Left Stick Values"),
#     ("1", "Right Stick", "Right Stick Values")
# ]

# _enum_controller_trigger_operators = [
#     ("0", "Left Trigger", "Left Trigger Values"),
#     ("1", "Right Trigger", "Right Trigger Values")
# ]

# _enum_vrcontroller_trigger_operators = [
#     ("0", "Left", "Left Controller Values"),
#     ("1", "Right", "Right Controller Values")
# ]


# _enum_controller_buttons_operators = [
#     ("0", "A / Cross", "A / Cross Button"),
#     ("1", "B / Circle", "B / Circle Button"),
#     ("2", "X / Square", "X / Square Button"),
#     ("3", "Y / Triangle", "Y / Triangle Button"),
#     ("4", "Select / Share", "Select / Share Button"),
#     ("6", "Start / Options", "Start / Options Button"),
#     ("7", "L3", "Left Stick Button"),
#     ("8", "R3", "Right Stick Button"),
#     ("9", "LB / L1", "Left Bumper / L1 Button"),
#     ("10", "RB / R1", "Right Bumper / R1 Button"),
#     ("11", "D-Pad Up", "D-Pad Up Button"),
#     ("12", "D-Pad Down", "D-Pad Down Button"),
#     ("13", "D-Pad Left", "D-Pad Left Button"),
#     ("14", "D-Pad Right", "D-Pad Right Button")
# ]


# _enum_play_mode_values = [
#     ("bge.logic.KX_ACTION_MODE_PLAY", "Play", "Play the action once"),
#     ("bge.logic.KX_ACTION_MODE_LOOP", "Loop", "Loop the action"),
#     (
#         "bge.logic.KX_ACTION_MODE_PING_PONG",
#         "Ping Pong",
#         "Play the action in one direction then in the opposite one"
#     ),
#     ("bge.logic.KX_ACTION_MODE_PLAY + 3", "Play Stop", "Play the action once"),
#     ("bge.logic.KX_ACTION_MODE_LOOP + 3", "Loop Stop", "Loop the action"),
#     (
#         "bge.logic.KX_ACTION_MODE_PING_PONG + 3",
#         "Ping Pong Stop",
#         "Play the action in one direction then in the opposite one"
#     )
# ]

# _enum_spawn_types = [
#     ("Simple", "Simple", "Spawn an instance without behavior"),
#     ("SimpleBullet", "Simple Bullet", "Spawn a bullet that travels linearly along its local +Y axis"),
#     ("PhysicsBullet", "Physical Bullet", "Spawn a bullet that travels along a trajectory aimed at its local +Y axis")
# ]

# _serialize_types = [
#     ("builtin", "Built-In", "Serialize Built-In data type (int, float, bool, dict, etc.)"),
#     ("Vec2", "2D Vector", "Serialize a 2D Vector"),
#     ("Vec3", "3D Vector", "Serialize a 3D Vector"),
#     ("Vec4", "4D Vector", "Serialize a 4D Vector"),
#     ("Mat3", "3x3 Matrix", "Serialize a 3x3 Matrix"),
#     ("Mat4", "4x4 Matrix", "Serialize a 4x4 Matrix"),
#     ("GameObj", "Game Object", "Serialize a Game Object (Note: Not all data can be serialized)")
# ]


# _enum_msg_types = [
#     ("INFO", "Info", "Will print the message in white (on-screen console)"),
#     ("DEBUG", "Debug", "Will print the message in light yellow (on-screen console)"),
#     ("WARNING", "Warning", "Will print the message in yellow (on-screen console)"),
#     ("ERROR", "Error", "Will print the message in red (on-screen console)"),
#     ("SUCCESS", "Success", "Will print the message in green (on-screen console)")
# ]





# def filter_materials(self, item):
#     if item.is_grease_pencil:
#         return False
#     return True


# def filter_geometry_nodes(self, item):
#     if isinstance(item, bpy.types.GeometryNodeTree):
#         return True
#     return False


# def filter_lights(self, item):
#     if (
#         isinstance(item.data, bpy.types.AreaLight)
#         or isinstance(item.data, bpy.types.PointLight)
#         or isinstance(item.data, bpy.types.SpotLight)
#         or isinstance(item.data, bpy.types.SunLight)
#     ):
#         return True
#     return False


# def filter_texts(self, item):
#     if (
#         item.name.startswith('nl_')
#     ):
#         return False
#     return True


# def filter_navmesh(self, item):
#     if item.game.physics_type == 'NAVMESH':
#         return True
#     return False


# def filter_camera(self, item):
#     if isinstance(item.data, bpy.types.Camera):
#         return True
#     return False


# def filter_speaker(self, item):
#     if isinstance(item.data, bpy.types.Speaker):
#         return True
#     return False


# def filter_armatures(self, item):
#     if (
#         isinstance(item.data, bpy.types.Armature)
#     ):
#         return True
#     return False


# def filter_curves(self, item):
#     if (
#         isinstance(item.data, bpy.types.Curve)
#     ):
#         return True
#     return False


# def filter_logic_trees(self, item):
#     if (
#         isinstance(item, bge_netlogic.ui.LogicNodeTree)
#     ):
#         return True
#     return False


# def filter_node_groups(self, item):
#     if (
#         isinstance(item, bpy.types.ShaderNodeTree)
#     ):
#         return True
#     return False


# def parse_field_value(value_type, value):
#     t = value_type
#     v = value

#     if t == "NONE":
#         return "None"

#     if t == "INTEGER":
#         try:
#             return int(v)
#         except ValueError:
#             return "0.0"

#     if t == "FLOAT":
#         try:
#             return float(v)
#         except ValueError:
#             return "0.0"

#     if t == "STRING":
#         return '"{}"'.format(v)

#     if t == "FILE_PATH":
#         return '"{}"'.format(v)

#     if t == "BOOLEAN":
#         return v

#     raise ValueError(
#         "Cannot parse enum {} type for NLValueFieldSocket".format(t)
#     )


# def update_tree_code(self, context):
#     pass
#     # utils.set_compile_status(utils.TREE_MODIFIED)
#     # if utils.is_compile_status(utils.TREE_COMPILED_ALL):
#     #     return
#     # if not hasattr(context.space_data, 'edit_tree'):
#     #     return
#     # tree = context.space_data.edit_tree
#     # if not tree:
#     #     return
#     # for node in tree.nodes:
#     #     if isinstance(node, NLNode):
#     #         try:
#     #             node.update_draw()
#     #         except Exception:
#     #             pass
#     # if not getattr(bpy.context.scene.logic_node_settings, 'auto_compile'):
#     #     return
#     # bge_netlogic.update_current_tree_code()


# def update_draw(self, context=None):
#     if not hasattr(context.space_data, 'edit_tree'):
#         return
#     tree = context.space_data.edit_tree
#     for node in tree.nodes:
#         if isinstance(node, NLNode):
#             try:
#                 node.update_draw()
#             except Exception as e:
#                 utils.error(f'Failed node {node}, {e}')
#                 pass


# def socket_field(s):
#     return parse_field_value(s.value_type, s.value)


# def keyboard_key_string_to_bge_key(ks):
#     ks = ks.replace("ASTERIX", "ASTER")

#     if ks == "NONE":
#         return "None"

#     if ks == "RET":
#         ks = "ENTER"

#     if ks.startswith("NUMPAD_"):
#         ks = ks.replace("NUMPAD_", "PAD")
#         if("SLASH" in ks or "ASTER" in ks or "PLUS" in ks):
#             ks = ks.replace("SLASH", "SLASHKEY")
#             ks = ks.replace("ASTER", "ASTERKEY")
#             ks = ks.replace("PLUS", "PLUSKEY")
#         return "bge.events.{}".format(ks)

#     x = "{}KEY".format(ks.replace("_", ""))

#     return "bge.events.{}".format(x)


# class NetLogicType:
#     pass


# class NLSocket:
#     valid_sockets: list = []
#     nl_color: list = utils.Color.RGBA(.631, .631, .631, 1.0)
#     type: StringProperty(default='VALUE')
#     shape: StringProperty(default='')

#     def __init__(self):
#         self.socket_id = INVALID
#         self.valid_sockets = []
#         # self.display_shape = 'CIRCLE'
#     #     if len(self.shape):
#     #         self.shape_setup()

#     # def shape_setup(self):
#     #     pass

#     def validate(self, link, from_socket):
#         link.is_valid = False
#         pass

#     def get_unlinked_value(self):
#         raise NotImplementedError()


# class NLNode(NetLogicType):
#     nl_module = None

#     def write_cell_declaration(self, cell_varname, line_writer):
#         classname = self.get_netlogic_class_name()
#         line_writer.write_line("{} = {}()", cell_varname, classname)

#     @property
#     def tree(self):
#         for tree in bpy.data.node_groups:
#             if not isinstance(tree, LogicNodeTree):
#                 continue
#             nodes = [node for node in tree.nodes]
#             if self in nodes:
#                 return tree

#     def setup(
#         self,
#         cell_varname,
#         uids
#     ):
#         text = ''
#         global ERROR_MESSAGES
#         for t in self.get_attributes():
#             field_name = t[0]
#             field_value = t[1]
#             if callable(field_value):
#                 field_value = field_value()
#             text += f'        {cell_varname}.{field_name} = {field_value}\n'
#         for socket in self.inputs:
#             try:
#                 text += self.write_socket_field_initialization(
#                     socket,
#                     cell_varname,
#                     uids
#                 )
#                 # self.mute = False
#             except IndexError as e:
#                 utils.error(
#                     f"Index error for node '{self.name}'. This normally happens when a node has sockets added or removed in an update. Try re-adding the node to resolve this issue."
#                 )
#                 # self.mute = True
#                 ERROR_MESSAGES.append(f'{self.name}: Index Error. FIX: Delete and re-add node; issue might be a linked input node as well.')
#                 self.use_custom_color = True
#                 self.color = (1, 0, 0)
#             except Exception as e:
#                 utils.error(
#                     f'Error occured when writing sockets for {self.__class__} Node: {e}\n'
#                     f'\tInfo:\n'
#                     f'\tSocket: {socket}\n'
#                     f'\tCellname: {cell_varname}\n'
#                     f'\tNode: {self.label if self.label else self.name}\n'
#                     '---END ERROR'
#                 )
#                 # self.mute = True
#                 ERROR_MESSAGES.append(f'{self.name}: Unknown Error: {e}')
#                 self.use_custom_color = True
#                 self.color = (1, 0, 0)
#         return text

#     def write_socket_field_initialization(
#         self,
#         socket,
#         cell_varname,
#         uids
#     ):
#         text = ''
#         input_names = self.get_input_names()
#         input_socket_index = self._index_of(socket, self.inputs)
#         field_name = None
#         if input_names:
#             field_name = input_names[input_socket_index]
#         else:
#             field_name = self.get_field_name_for_socket(socket)
#         field_value = None
#         if socket.is_linked:
#             field_value = self.get_linked_socket_field_value(
#                 socket,
#                 cell_varname,
#                 field_name,
#                 uids
#             )
#         else:
#             field_value = socket.get_unlinked_value()
#         # line_writer.write_line(
#         #     "\t{}.{} = {}",
#         #     cell_varname,
#         #     field_name,
#         #     field_value
#         # )
#         text += f'        {cell_varname}.{field_name} = {field_value}\n'
#         return text

#     def get_attributes(self):
#         """
#         Return a list of (field_name, field_value) tuples, where field_name
#         couples to output socket with a cell field and field_value is
#         either a value or a no-arg callable producing value
#         :return: the non socket fields initializers
#         """
#         return []

#     def get_import_module(self):
#         return self.nl_module

#     def get_input_names(self):
#         return None

#     def get_field_name_for_socket(self, socket):
#         utils.debug("not implemented in ", self)
#         raise NotImplementedError()

#     def get_netlogic_class_name(self):
#         raise NotImplementedError()

#     def _index_of(self, item, a_iterable):
#         i = 0
#         for e in a_iterable:
#             if e == item:
#                 return i
#             i += 1

#     def get_linked_socket_field_value(
#         self,
#         socket,
#         cell_varname,
#         field_name,
#         uids
#     ):
#         output_node = socket.links[0].from_socket.node
#         output_socket = socket.links[0].from_socket

#         while isinstance(output_node, bpy.types.NodeReroute):
#             # cycle through and reset output_node until master is met
#             if not output_node.inputs[0].links:
#                 return None
#             next_socket = output_node.inputs[0].links[0].from_socket
#             next_node = next_socket.node
#             output_socket = next_socket
#             if isinstance(next_node, NLNode):
#                 break
#             output_node = next_node

#         if isinstance(output_node, bpy.types.NodeReroute):
#             output_node = output_node.inputs[0].links[0].from_socket.node
#         output_socket_index = self._index_of(
#             output_socket,
#             output_node.outputs
#         )

#         if not hasattr(output_node, 'nl_module'):
#             raise Exception('No NLNode')
#         output_node_varname = uids.get_varname_for_node(output_node)
#         output_map = output_node.get_output_names()

#         if output_map:
#             varname = output_map[output_socket_index]
#             if varname is utils.OUTCELL:
#                 return output_node_varname
#             else:
#                 return '{}.{}'.format(output_node_varname, varname)
#         else:
#             return output_node_varname

#     def get_output_names(self):
#         return None

#     def update(self):
#         # bge_netlogic.update_current_tree_code()
#         pass


# class NodeSocketLogicCondition(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLConditionSocket"


# class NodeSocketPseudoCondition(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLPseudoConditionSocket"


# class NodeSocketLogicParameter(bpy.types.NodeSocket):
#     bl_idname = 'NLParameterSocket'


# class NodeSocketLogicDictionary(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLDictSocket"


# class NodeSocketLogicUI(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLUISocket"


# class NodeSocketLogicList(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLListSocket"


# class NodeSocketLogicListItem(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLListItemSocket"


# class NodeSocketLogicBitMask(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLCollisionMaskSocket"


# class NodeSocketLogicBrick(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLLogicBrickSocket"


# class NodeSocketLogicPython(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLPythonSocket"


# class NLAbstractNode(NLNode):
#     bl_icon = 'DOT'
#     nl_separate = False
#     deprecated = False
#     search_tags = []

#     @classmethod
#     def poll(cls, node_tree):
#         return isinstance(node_tree, LogicNodeTree)

#     def insert_link(self, link):
#         to_socket = link.to_socket
#         from_socket = link.from_socket
#         # try:
#         #     to_socket.validate(link, from_socket)
#         # except Exception as e:
#         #     utils.warning(e)
#         #     utils.debug(
#         #         'Receiving Node not a Logic Node Type, skipping validation.'
#         #     )

#     def add_input(self, cls, name, settings={}):
#         ipt = self.inputs.new(cls.bl_idname, name)
#         for key, val in settings.items():
#             setattr(ipt, key, val)

#     def add_output(self, cls, name, settings={}):
#         ipt = self.outputs.new(cls.bl_idname, name)
#         for key, val in settings.items():
#             setattr(ipt, key, val)

#     def free(self):
#         pass

#     def check(self, tree):
#         if self.deprecated:
#             global WARNING_MESSAGES
#             utils.deprecate(self, tree)
#             WARNING_MESSAGES.append(f"Deprecated Node: '{self.name}' in '{tree.name}'. Delete to avoid issues.")
#             self.use_custom_color = True
#             self.color = (.8, .6, 0)
#         for socket in self.inputs:
#             socket.check(tree)
#         for socket in self.outputs:
#             socket.check(tree)

#     def draw_buttons(self, context, layout):
#         pass

#     def update_draw(self, context=None):
#         pass

#     def update(self):
#         update_tree_code(self, bpy.context)


# ###############################################################################
# # Basic Nodes
# ###############################################################################


# class LogicNodeConditionType(bpy.types.Node, NLAbstractNode):
#     nl_nodetype = 'CON'

#     def init(self, context):
#         self.use_custom_color = (
#             bpy
#             .context
#             .scene
#             .logic_node_settings
#             .use_custom_node_color
#         )
#         self.color = CONDITION_NODE_COLOR


# class LogicNodeActionType(bpy.types.Node, NLAbstractNode):
#     nl_nodetype = 'ACT'

#     def init(self, context):
#         self.use_custom_color = (
#             bpy
#             .context
#             .scene
#             .logic_node_settings
#             .use_custom_node_color
#         )
#         self.color = ACTION_NODE_COLOR


# class LogicNodeParameterType(bpy.types.Node, NLAbstractNode):
#     nl_nodetype = 'PAR'

#     def init(self, context):
#         self.use_custom_color = (
#             bpy
#             .context
#             .scene
#             .logic_node_settings
#             .use_custom_node_color
#         )
#         self.color = PARAMETER_NODE_COLOR
#         self.master_nodes = []


# ###############################################################################
# # Pointer Sockets
# ###############################################################################


# class NodeSocketLogicObject(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLGameObjectSocket"


# class NodeSocketLogicCamera(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLCameraSocket"


# class NodeSocketLogicSpeaker(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLSpeakerSocket"


# class NodeSocketLogicNavMesh(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLNavMeshSocket"


# class NodeSocketLogicLight(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLLightObjectSocket"


# class NodeSocketLogicArmature(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLArmatureObjectSocket"


# class NodeSocketLogicCurve(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLCurveObjectSocket"


# class NodeSocketLogicGameProperty(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLGamePropertySocket"


# class NodeSocketLogicBone(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLArmatureBoneSocket"


# class NodeSocketLogicBoneConstraint(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLBoneConstraintSocket"


# class NodeSocketLogicGeometryNodeTree(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLGeomNodeTreeSocket"


# class NodeSocketLogicNodeGroup(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLNodeGroupSocket"


# class NodeSocketLogicNodeGroupNode(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLNodeGroupNodeSocket"


# class NodeSocketLogicMaterial(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLMaterialSocket"


# class NodeSocketLogicMaterialNode(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLTreeNodeSocket"


# class NodeSocketLogicScene(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLSceneSocket"


# class NodeSocketLogicText(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLTextIDSocket"


# class NodeSocketLogicMesh(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLMeshSocket"


# class NodeSocketLogicObjectName(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLGameObjectNameSocket"


# class NodeSocketLogicCollection(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLCollectionSocket"


# class NLSocketLogicTree(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLSocketLogicTree"


# class NodeSocketLogicAnimation(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLAnimationSocket"


# class NodeSocketLogicSoundFile(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLSoundFileSocket"


# class NodeSocketLogicImage(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLImageSocket"


# class NodeSocketLogicFont(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLFontSocket"


# ###############################################################################
# # String Pointer Sockets
# ###############################################################################


# class NodeSocketLogicGlobalCategory(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLGlobalCatSocket"


# class NodeSocketLogicGlobalProperty(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLGlobalPropSocket"


# ###############################################################################
# # Value Sockets
# ###############################################################################


# class NodeSocketLogicFloatFactor(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLSocketAlphaFloat"


# class NodeSocketLogicLoopCount(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLSocketLoopCount"


# class NodeSocketLogicBoolean(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLBooleanSocket"


# class NodeSocketLogicVectorXYZ(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLXYZSocket"


# class NodeSocketLogicInvertXY(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLInvertedXYSocket"


# class NodeSocketLogicFloatPositive(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLPositiveFloatSocket"


# class NodeSocketLogicString(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLQuotedStringFieldSocket"


# class NodeSocketLogicFilePath(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLFilePathSocket"


# class NodeSocketLogicInteger(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLIntegerFieldSocket"


# class NodeSocketLogicIntegerPositive(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLPositiveIntegerFieldSocket"


# class NodeSocketLogicIntegerPositiveCent(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLPositiveIntCentSocket"


# class NodeSocketLogicValue(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLValueFieldSocket"


# class NodeSocketLogicValueOptional(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLOptionalValueFieldSocket"


# class NodeSocketLogicKeyboardKey(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLKeyboardKeySocket"


# class NodeSocketLogicMouseButton(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLMouseButtonSocket"


# class NodeSocketLogicPlayMode(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLPlayActionModeSocket"


# class NodeSocketLogicFloat(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLFloatFieldSocket"


# class NodeSocketLogicFloatAngle(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLFloatAngleSocket"


# class NodeSocketLogicTime(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLTimeSocket"


# class NodeSocketLogicVectorXY(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLVec2FieldSocket"


# class NodeSocketLogicVectorXYAngle(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLAngleLimitSocket"


# class NodeSocketLogicVectorXYZ(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLVec3FieldSocket"


# class NodeSocketLogicVectorXYZAngle(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLVec3RotationSocket"


# class NodeSocketLogicVectorXYZVelocity(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLVelocitySocket"


# class NodeSocketLogicColorRGB(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLColorSocket"


# class NodeSocketLogicColorRGBA(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLColorAlphaSocket"


# class NodeSocketLogicVector(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLVectorSocket"


# class NodeSocketLogicAxis(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLSocketLocalAxis"


# class NodeSocketLogicAxisSigned(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLSocketOrientedLocalAxis"


# class NodeSocketLogicBlendMode(bpy.types.NodeSocket, NLSocket):
#     bl_idname = "NLBlendActionMode"


# ###############################################################################
# # NODES
# ###############################################################################


# # Parameters
