_enum_local_axis = [
    ("0", "X Axis", "The Local X Axis [Integer Value 0]"),
    ("1", "Y Axis", "The Local Y Axis [Integer Value 1]"),
    ("2", "Z Axis", "The Local Z Axis [Integer Value 2]")
]


_enum_look_axis = [
    ("0", "X Axis", "The Local X Axis [Integer Value 0]"),
    ("1", "Y Axis", "The Local Y Axis [Integer Value 1]")
]


_enum_vector_types = [
    ("0", "Vector", "Vector XYZ"),
    ("1", "Euler", "Euler XYZ")
]


_enum_local_oriented_axis = [
    ("0", "+X Axis", "The Local X Axis [Integer Value 0]"),
    ("1", "+Y Axis", "The Local Y Axis [Integer Value 1]"),
    ("2", "+Z Axis", "The Local Z Axis [Integer Value 2]"),
    ("3", "-X Axis", "The Local X Axis [Integer Value 3]"),
    ("4", "-Y Axis", "The Local Y Axis [Integer Value 4]"),
    ("5", "-Z Axis", "The Local Z Axis [Integer Value 5]")
]


_enum_mouse_wheel_direction = [
    ("1", "Scroll Up", "Mouse Wheel Scrolled Up [1]"),
    ("2", "Scroll Down", "Mouse Wheel Scrolled Down [2]"),
    ("3", "Scroll Up or Down", "Mouse Wheel Scrolled either Up or Down[3]")
]


_enum_vector_math_options = [
    ("", "Operation", ""),
    ("add", "Add", "A + B"),
    ("subtract", "Subtract", "A - B"),
    ("multiply", "Multiply", "Entry-wise multiply"),
    ("divide", "Divide", "Entry-wise divide"),
    ("multadd", "Multiply Add", "A * B + C"),
    ("matmul", "Matrix Multiply", "Transform A by B"),
    None,
    ("scale", "Scale", "A multiplied by Scale"),
    ("length", "Length", "Length of A"),
    ("distance", "Distance", "Distance between A and B"),
    None,
    # ("angle_signed", "Signed Angle", "The angle between 2 vectors with respect to direction"),
    ("dot", "Dot Product", "A dot B"),
    ("angle", "Angle", "The angle between 2 vectors"),
    # ("faceforward", None, "Orients a vector A to point away from a surface B as defined by its normal C. Returns A if A.dot(B) < 0 else -A"),
    ("refract", "Refract", "For a given incident vector A, a surface normal B and ratio of indices of refraction, Ior, refract returns the refraction vector, R"),
    ("reflect", "Reflect", "Reflect A around the normal B. B doesn't need to be normalized"),
    ("project", "Project", "Project this vector onto another"),
    ("cross", "Cross Product", "Project A onto B"),
    None,
    ("normalize", "Normalize", "Rescale all values to 0 - 1"),
    ("lerp", "Mix (Lerp)", "Linear Interpolation between the two vectors"),
    ("slerp", "Spherical Lerp", "Spherical Interpolation between the two vectors"),
    ("negate", "Negate", "Multiply all values by -1")
]


_enum_type_casts = [
    ("int", "To Integer", "Convert this value to an integer type"),
    ("bool", "To Boolean", "Convert this value to a boolean type"),
    ("str", "To String", "Convert this value to a string type"),
    ("float", "To Float", "Convert this value to a float type")
]


_enum_distance_models = [
    ('INVERSE', 'Inverse', 'Sound will fade exponentially (Realistic)'),
    ('INVERSE_CLAMPED', 'Inverse Clamped',
     'Sound will fade exponentially (Realistic, Clamped)'),
    ('EXPONENT', 'Exponent', 'Sound will fade detemined by an exponent (Good audibility)'),
    ('EXPONENT_CLAMPED', 'Exponent Clamped',
     'Sound will fade detemined by an exponent (Good audibility, Clamped)'),
    ('LINEAR', 'Linear', 'Sound will fade in a linear relation to distance'),
    ('LINEAR_CLAMPED', 'Linear Clamped',
     'Sound will fade in a linear relation to distance (Clamped)'),
    ('NONE', 'None', "Don't use a distance model")
]


_enum_object_property_types = [
    ('0', 'Game Property', 'Edit Game Property'),
    ('1', 'Attribute', 'Edit Internal Attribute (can be used in materials)')
]


_bone_attrs = [
    ('', 'Position', ''),
    ("location", "Location", "Location of the bone relative to armature"),  # Vector
    ("pose_rotation_euler", "Euler Rotation", "Rotation of the bone in euler coordinates"),  # Vector
    None,
    ("head", "Head", "Location of head end of the bone relative to its parent"),  # Vector
    ("head_local", "Local Head", "Location of head end of the bone relative to armature"),  # Vector
    ("head_pose", "Pose Head", "Location of head end of the bone relative to armature in the current pose"),  # Vector
    None,
    ("center", "Center", "Location of center of the bone relative to its parent"),  # Vector
    ("center_local", "Local Center", "Location of center of the bone relative to armature"),  # Vector
    ("center_pose", "Pose Center", "Location of center of the bone relative to armature in the current pose"),  # Vector
    None,
    ("tail", "Tail", "Location of tail end of the bone relative to its parent"),  # Vector
    ("tail_pose", "Pose Tail", "Location of tail end of the bone relative to armature in the current pose"),  # Vector
    ("tail_local", "Local Tail", "Location of tail end of the bone relative to armature"),  # Vector
    ('', 'Other', ''),
    ("name", "Name", "Name of the Bone"),  # String
    None,
    ("inherit_scale", "Inherit Scale", "Specifies how the bone inherits scaling from the parent bone"),  # Enum
    ("inherit_rotation", "Inherit Rotation", "Bone inherits rotation or scale from parent bone"),  # Boolean
    None,
    ("connected", "Connected", "When bone has a parent, bone's head is stuck to the parent's tail"),  # Boolean
    ("deform", "Deform", "Enable Bone to deform geometry"),  # Boolean
    ("use_local_location", "Use Local", "Bone location is set in local space"),  # Boolean
    ("use_relative_parent", "Use Relative Parent", "Object children will use relative transform, like deform"),  # Boolean
    ("use_scale_easing", "Scale Easing", "Multiply the final easing values by the Scale In/Out Y factors")  # Boolean
]


_set_bone_attrs = [
    ("location", "Location", "Location of the bone relative to armature"),  # Vector
    ("pose_rotation_euler", "Euler Rotation", "Rotation of the bone in euler coordinates"),  # Vector
    None,
    ("inherit_scale", "Inherit Scale", "Specifies how the bone inherits scaling from the parent bone"),  # Enum
    ("inherit_rotation", "Inherit Rotation", "Bone inherits rotation or scale from parent bone"),  # Boolean
    None,
    ("deform", "Deform", "Enable Bone to deform geometry"),  # Boolean
    ("use_local_location", "Use Local", "Bone location is set in local space"),  # Boolean
    ("use_relative_parent", "Use Relative Parent", "Object children will use relative transform, like deform"),  # Boolean
    ("use_scale_easing", "Scale Easing", "Multiply the final easing values by the Scale In/Out Y factors")  # Boolean
]


_enum_ik_mode_values = [
    ("None", "None", "Not set"),
    (
        "bge.logic.CONSTRAINT_IK_MODE_INSIDE",
        "Inside",
        "Keep the bone with IK Distance of target"
    ),
    (
        "bge.logic.CONSTRAINT_IK_MODE_OUTSIDE",
        "Outside",
        "Keep the bone outside IK Distance of target"
    ),
    (
        "bge.logic.CONSTRAINT_IK_MODE_ONSURFACE",
        "On Surface",
        "Keep the bone exactly at IK Distance of the target"
    )
]


_enum_field_value_types = [
    ("STRING", "String", "A String"),
    ("FLOAT", "Float", "A Float value"),
    ("INTEGER", "Integer", "An Integer value"),
    ("BOOLEAN", "Bool", "A True/False value"),
    ("FILE_PATH", "File Path", 'Choose a file path')
]


_enum_numeric_field_value_types = [
    ("NONE", "None", "The None value"),
    ("INTEGER", "Integer", "An Integer value"),
    ("FLOAT", "Float", " A Float value"),
    ("EXPRESSION", "Expression", "A numeric expression")
]


_enum_optional_float_value_types = [
    ("NONE", "None", "No value"),
    ("FLOAT", "Float", "A decimal value"),
    ("EXPRESSION", "Expression", "A numeric expression")
]


_enum_vehicle_axis = [
    ("REAR", "Rear", "Apply to wheels without steering"),
    ("FRONT", "Front", "Apply to wheels with steering"),
    ("ALL", "All", "Apply to all wheels")
]


_enum_readable_member_names = [
    ("worldPosition", "World Position", "The World Position of the object"),
    (
        "worldOrientation",
        "World Orientation",
        "The World Orientation of the object"
    ), (
        "worldLinearVelocity",
        "World Linear Velocity",
        "The local linear velocity of the object"
    ), (
        "worldAngularVelocity",
        "World Angular Velocity",
        "The local angular velocity of the object"
    ), (
        "worldTransform",
        "World Transform",
        (
            'The World Transform of the '
            'object'
        )
    ),
    ("worldScale", "World Scale", "The global scale of the object"),
    None,
    ("localPosition", "Local Position", "The local position of the object"),
    (
        "localOrientation",
        "Local Orientation",
        "The local orientation of the object"
    ), (
        "localLinearVelocity",
        "Local Linear Velocity",
        "The local linear velocity of the object"
    ), (
        "localAngularVelocity",
        "Local Angular Velocity",
        "The local angular velocity of the object"
    ), (
        "localTransform",
        "Local Transform",
        (
            'The local transform of the '
            'object'
        )
    ),
    ("localScale", "Local Scale", "The local scale of the object"),
    None,
    ("name", "Name", "The name of the object"),
    ("color", "Color", "The solid color of the object"),
    (
        "visible",
        "Visibility",
        "True if the object is set to visible, False if it is set to invisible"
    )
]


_enum_writable_member_names = [
    ("worldPosition", "World Position", "The World Position of the object"),
    (
        "worldOrientation",
        "World Orientation",
        "The World Orientation of the object"
    ), (
        "worldLinearVelocity",
        "World Linear Velocity",
        "The local linear velocity of the object"
    ), (
        "worldAngularVelocity",
        "World Angular Velocity",
        "The local angular velocity of the object"
    ), (
        "worldTransform",
        "World Transform",
        'The World Transform of the object'
    ),
    ("worldScale", "World Scale", "The global scale of the object"),
    None,
    ("localPosition", "Local Position", "The local position of the object"),
    (
        "localOrientation",
        "Local Orientation",
        "The local orientation of the object"
    ), (
        "localLinearVelocity",
        "Local Linear Velocity",
        "The local linear velocity of the object"
    ), (
        "localAngularVelocity",
        "Local Angular Velocity",
        "The local angular velocity of the object"
    ), (
        "localTransform",
        "Local Transform",
        'The local transform of the object'
    ),
    None,
    ('color', 'Color', 'Color')
]


_enum_matrix_dimensions = [
    ('1', '3x3', 'A 3x3 Matrix.'),
    ('2', '4x4', 'A 4x4 Matrix.')
]


_enum_mouse_buttons = [
    ("bge.events.LEFTMOUSE", "Left Button", "Left Mouse Button"),
    ("bge.events.MIDDLEMOUSE", "Middle Button", "Middle Mouse Button"),
    ("bge.events.RIGHTMOUSE", "Right Button", "Right Mouse Button")
]


_enum_euler_orders = [
    ("XYZ", "XYZ", "XYZ Order"),
    ("XZY", "XZY", "XZY Order"),
    ("YXZ", "YXZ", "YXZ Order"),
    ("YZX", "YZX", "YZX Order"),
    ("ZXY", "ZXY", "ZXY Order"),
    ("ZYX", "ZYX", "ZYX Order")
]


_enum_vsync_modes = [
    ("bge.render.VSYNC_OFF", "Off", "Disable Vsync"),
    ("bge.render.VSYNC_ON", "On", "Enable Vsync"),
    (
        "bge.render.VSYNC_ADAPTIVE",
        "Adaptive",
        (
            'Enable adaptive Vsync '
            '(if supported)'
        )
    )
]


_enum_string_ops = [
    ("0", "Postfix", "Insert A after String"),
    ("1", "Prefix", "Insert A before String"),
    ("2", "Infix", "Insert A before String, B after String."),
    ("3", "Remove Last", "Remove Last Character from String"),
    ("4", "Remove First", "Remove First Character from String"),
    (
        "5",
        "Replace",
        'Replace all occurences of A with B'
    ),
    ("6", "Upper Case", "Convert to Upper Case"),
    ("7", "Lower Case", "Convert to Lower Case"),
    (
        "8",
        "Remove Range",
        'Remove characters from index A to index B'
    ),
    (
        "9",
        "Insert At",
        "Insert A at index B"
    ),
    (
        "10",
        "Length",
        "Character Count (returns a Number)"
    ),
    (
        "11",
        "Substring",
        "Characters between index A and index B"
    ),
    (
        "12",
        "First Index Of",
        "Position of the first occurence of A"
    ),
    (
        "13",
        "Last Index Of",
        "Position of the last occurence of A"
    )
]


_enum_quality_levels = [
    ("0", "Low", "Set a lower quality to increase performance"),
    ("1", "Medium", "Set a medium quality for a balanced performance"),
    ("2", "High", "Set a high quality at the cost of performance"),
    ("3", "Ultra", "Set a very high quality at the cost of performance")
]


_enum_math_operations = [
    ("ADD", "Add", "Sum A and B"),
    ("SUB", "Subtract", "Subtract B from A"),
    ("DIV", "Divide", "Divide A by B"),
    ("MUL", "Multiply", "Multiply A by B"),
    ("POW", "Power", "A to the power of B"),
    ("MOD", "Modulo", "Modulo of A by B"),
    ("FDIV", "Floor Divide", "Floor Divide A by B")
]


_enum_greater_less = [
    ("GREATER", "Greater", "Value greater than Threshold"),
    ("LESS", "Less", "Value less than Threshold")
]


_enum_in_or_out = [
    ("INSIDE", "Within", "Value is within Range"),
    ("OUTSIDE", "Outside", "Value is outside Range")
]


_enum_logic_operators = [
    ("0", "Equal", "A equals B"),
    ("1", "Not Equal", "A not equals B"),
    ("2", "Greater Than", "A greater than B"),
    ("3", "Less Than", "A less than B"),
    ("4", "Greater or Equal", "A greater or equal to B"),
    ("5", "Less or Equal", "A less or equal to B")
]


_enum_controller_stick_operators = [
    ("0", "Left Stick", "Left Stick Values"),
    ("1", "Right Stick", "Right Stick Values")
]


_enum_controller_trigger_operators = [
    ("0", "Left Trigger", "Left Trigger Values"),
    ("1", "Right Trigger", "Right Trigger Values")
]


_enum_controller_buttons_operators = [
    ("0", "A / Cross", "A / Cross Button"),
    ("1", "B / Circle", "B / Circle Button"),
    ("2", "X / Square", "X / Square Button"),
    ("3", "Y / Triangle", "Y / Triangle Button"),
    (None),
    ("9", "LB / L1", "Left Bumper / L1 Button"),
    ("10", "RB / R1", "Right Bumper / R1 Button"),
    ("15", "LT / L2", "Left Trigger Button"),
    ("16", "RT / R2", "Right Trigger Button"),
    ("7", "L3", "Left Stick Button"),
    ("8", "R3", "Right Stick Button"),
    (None),
    ("11", "D-Pad Up", "D-Pad Up Button"),
    ("12", "D-Pad Down", "D-Pad Down Button"),
    ("13", "D-Pad Left", "D-Pad Left Button"),
    ("14", "D-Pad Right", "D-Pad Right Button"),
    (None),
    ("4", "Select / Share", "Select / Share Button"),
    ("6", "Start / Options", "Start / Options Button")
]


_enum_input_types = [
    ('0', 'Tap', 'True if the input is first activated'),
    ('1', 'Down', 'True if the input is held down'),
    ('2', 'Up', 'True if the input is released')
]


_enum_play_mode_values = [
    ("bge.logic.KX_ACTION_MODE_PLAY", "Play", "Play the action once (0)"),
    ("bge.logic.KX_ACTION_MODE_LOOP", "Loop", "Loop the action (1)"),
    (
        "bge.logic.KX_ACTION_MODE_PING_PONG",
        "Ping Pong",
        "Play the action in one direction then in the opposite one (2)"
    ),
    ("bge.logic.KX_ACTION_MODE_PLAY + 3", "Play Stop", "Play the action once (3)"),
    ("bge.logic.KX_ACTION_MODE_LOOP + 3", "Loop Stop", "Loop the action (4)"),
    (
        "bge.logic.KX_ACTION_MODE_PING_PONG + 3",
        "Ping Pong Stop",
        "Play the action in one direction then in the opposite one (5)"
    )
]


_enum_blend_mode_values = [
    (
        "bge.logic.KX_ACTION_BLEND_BLEND",
        "Blend",
        "Blend layers using linear interpolation"
    ),
    ("bge.logic.KX_ACTION_BLEND_ADD", "Add", "Adds the layer together")
]


_enum_spawn_types = [
    ("0", "Simple", "Spawn an instance without behavior"),
    ("1", "Simple Bullet", "Spawn a bullet that travels linearly along its local +Y axis"),
    ("2", "Physical Bullet", "Spawn a bullet that travels along a trajectory aimed at its local +Y axis"),
    None,
    ("3", "Instance", "Spawn an instance of an object with its logic, physics and children")
]


_serialize_types = [
    ("builtin", "Built-In", "Serialize Built-In data type (int, float, bool, dict, etc.)"),
    ("Vec2", "2D Vector", "Serialize a 2D Vector"),
    ("Vec3", "3D Vector", "Serialize a 3D Vector"),
    ("Vec4", "4D Vector", "Serialize a 4D Vector"),
    ("Mat3", "3x3 Matrix", "Serialize a 3x3 Matrix"),
    ("Mat4", "4x4 Matrix", "Serialize a 4x4 Matrix"),
    ("GameObj", "Game Object", "Serialize a Game Object (Note: Not all data can be serialized)")
]


_enum_msg_types = [
    ("INFO", "Info", "Will print the message in white (on-screen console)"),
    ("DEBUG", "Debug", "Will print the message in light yellow (on-screen console)"),
    ("WARNING", "Warning", "Will print the message in yellow (on-screen console)"),
    ("ERROR", "Error", "Will print the message in red (on-screen console)"),
    ("SUCCESS", "Success", "Will print the message in green (on-screen console)")
]


_enum_python_types = [
    ("0", "Module", "Execute a script"),
    ("1", "Function", "Execute a single function from a .py file")
]


_writeable_widget_attrs = [
    ("show", "Visibility", "Visibility of Widget and its children"),#
    ("bg_color", "Color", "Background color"),#
    ("opacity", "Opacity", "Opacity"),#
    ("pos", "Position", "Widget Position (0-1 if set to relative)"),#
    ("pivot", "Pivot", "Widget screen position in pixels"),#
    ("size", "Size", "Widget Size (0-1 if set to relative)"),#
    ("angle", "Angle", "Widget Angle in degrees"),#
    ("width", "Width", "Widget Width (0-1 if set to relative)"),#
    ("height", "Height", "Widget Height (0-1 if set to relative)"),#
    ("use_clipping", "Clipping", "Cut off child widgets if they go over the edges"),#
    ("halign", "X Align", "Positioning direction along the X axis (Left-Right)"),#
    ("valign", "Y Align", "Positioning direction along the Y axis (Top-Bottom)"),#
    None,
    ("border_width", "Border Width", "Border draw width"),#
    ("border_color", "Border Color", "Border draw color"),#
    None,
    ("orientation", "Orientation", "Child widget arrangement mode (BoxLayout only)"),#
    ("spacing", "Spacing", "Pixels in between child widgets (BoxLayout only)"),#
    ("radius", "Radius", "Distance of the children to the center of the layout (PolarLayout only)"),#
    ("starting_angle", "Starting Angle", "Start positioning the child widgets from this angle. 0 is right, 90 is up. (PolarLayout only)"),#
    None,
    ("hover_color", "Hover Color", "Color for when the mouse is over widget (Button only)"),#
    None,
    ("text", "Text", "Text (Label only)"),#
    ("font", "Font", "Font to use for this label (Label only)"),
    ("font_color", "Font Color", "Font Color (Label only)"),#
    ("font_size", "Font Size", "Font Size (Label only)"),#
    ("font_opacity", "Font Opacity", "Font Opacity (Label Only)"),#
    ("line_height", "Line Height", "Line Height as factor (1 = Letter Height) (Label only)"),#
    ("text_halign", "Text X Align", "Text X Alignment (Label only)"),#
    ("text_valign", "Text Y Align", "Text Y Alignment (Label only)"),#
    ("wrap", "Word Wrap", "Use the size of this label to wrap text (Label only)"),#
    ("shadow", "Use Shadow", "Draw a shadow under the text (Label only)"),#
    ("shadow_offset", "Shadow Offset", "Offset for the shadow font (Label only)"),#
    ("shadow_color", "Shadow Color", "Color for the shadow font (Label only)"),#
    None,
    ("texture", "Image", "Texture to use as image (Image and Sprite only)"),
    None,
    ("icon", "Icon", "Icon (Sprite) position on sheet (Icon only)"),
    ("rows", "Rows", "Rows in the Icon (Sprite) sheet (Icon only)"),
    ("cols", "Columns", "Columns in the Icon (Sprite) sheet (Icon only)"),
    None,
    ("points", "Points", "Points of the path (Path only)")
]


_ui_layout_types = [
    ("FloatLayout", "Float Layout", "A Layout that places its child widgets independent of its own position"),
    ("RelativeLayout", "Relative Layout", "A Layout that places its child widgets relative to its own position"),
    ("BoxLayout", "Box Layout", "A Layout that automatically places widgets in either rows or columns"),
    ("GridLayout", "Grid Layout", "A Layout that automatically places widgets in a grid of rows or columns"),
    ("PolarLayout", "Polar Layout", "A Layout that automatically places widgets in a circle around itself")
]


_ui_boxlayout_types = [
    ("vertical", "Vertical", "Arrange child widgets horizontally"),
    ("horizontal", "Horizontal", "Arrange child widgets horizontally")
]


_ui_slider_types = [
    ("0", "Simple", "A knob sliding along a bar"),
    ("1", "Framed", "A knob sliding inside a frame"),
    ("2", "Progress", "A frame filled with color corresponding to knob position")
]


_ui_halign_types = [
    ("left", "Left", "Start positioning from the left side of the widget"),
    ("center", "Center", "Use the position as horizontal center"),
    ("right", "Right", "Start positioning from the right side of the widget")
]


_ui_valign_types = [
    ("bottom", "Bottom", "Start positioning from the bottom side of the widget"),
    ("center", "Center", "Use the position as vertical center"),
    ("top", "Top", "Start positioning from the top side of the widget")
]

_enum_math_functions = [
    ("User Defined", "User Defined", "A formula defined by the user"),
    ("abs(a)", "abs(a)", "absolute value of a"),
    ("acos(a)", "acos(a)", "arc cosine of a, radians"),
    ("acosh(a)", "acosh(a)", "inverse hyperbolic cosine of a"),
    ("asin(a)", "asin(a)", "arc sine of a, radians"),
    ("asinh(a)", "asinh(a)", "inverse hyperbolic cosing of a"),
    ("atan(a)", "atan(a)", "arc tangent of a, radians"),
    ("atan2(a,b)", "atan2(a,b)", "atan(a / b), radians"),
    ("atanh(a)", "atanh(a)", "inverse hyperbolic tangent of a"),
    ("ceil(a)", "ceil(a)", "smallest integer value = or > to a"),
    ("cos(a)", "cos(a)", "cosine of a, radians"),
    ("cosh(a)", "cosh(a)", "hyperbolic cosine of a"),
    ("curt(a)", "curt(a)", "cubic root of a"),
    ("degrees(a)", "degrees(a)", "convert a from radians to degrees"),
    ("e", "e", "the e constant"),
    ("exp(a)", "exp(e)", "e to the power a"),
    ("floor(a)", "floor(a)", "largest integer value < or = to a"),
    ("hypot(a,b)", "hypot(a,b)", "sqrt(a*a + b*b)"),
    ("log(a)", "log(a)", "natural log of a"),
    ("log10(a)", "log10(a)", "base 10 log of a"),
    ("mod(a,b)", "mod(a,b)", "a modulo b"),
    ("pi", "pi", "the PI constant"),
    ("pow(a,b)", "pow(a,b)", "a to the power b"),
    ("radians(a)", "radians(a)", "convert a from degrees to radians"),
    ("sign(a)", "sign(a)", "0 if a is 0, -1 if a < 0, 1 if a > 0"),
    ("sin(a)", "sin(a)", "sine of a, radians"),
    ("sinh(a)", "sinh(a)", "hyperbolic sine of a"),
    ("sqrt(a)", "sqrt(a)", "square root of a"),
    ("tan(a)", "tan(a)", "tangent of a, radians"),
    ("tanh(a)", "tanh(a)", "hyperbolic tangent of a")
]


_logic_gates = [
    ("0", "And", "True if A and B are True"),
    ("1", "Or", "True if A or B or both are True"),
    ("2", "Xor", "True only if either A or B is True, not both"),
    ("3", "Not", "True if A is False"),
    ("4", "Nand", "False if A and B are True"),
    ("5", "Nor", "True if A and B are False"),
    ("6", "Xnor", "True if A equals B"),
    ("7", "And Not", "True if A is True and B is False")
]


_logic_gates_list = [
    ("0", "And", ""),
    ("1", "Or", "")
]


_random_value_types = [
    ("0", "Float", ""),
    ("1", "Integer", ""),
    ("2", "Vector", ""),
    ("3", "Boolean", "")
]


_transform_types = [
    ("0", "Movement", ""),
    ("1", "Rotation", ""),
    ("2", "Force", ""),
    ("3", "Torque", ""),
    ("4", "Impulse", "")
]


_collision_bitmask_types = [
    ("0", "Group", ""),
    ("1", "Mask", "")
]


_rotate_by_types = [
    ("0", "2D", ""),
    ("1", "3D", ""),
    ("2", "Axis", "")
]


_socket_types = [
    ('', 'Type', ''),
    ('0', 'Generic', ''),
    None,
    ('1', 'Float', ''),
    ('2', 'Integer', ''),
    ('3', 'String', ''),
    ('4', 'Boolean', ''),
    None,
    ('5', 'Vector', ''),
    ('6', 'Color', ''),
    ('7', 'List', ''),
    ('8', 'Dictionary', ''),
    ('', '', ''),
    ('9', 'Datablock', ''),
    ('10', 'Object', ''),
    ('11', 'Collection', ''),
    None,
    ('12', 'Condition', ''),
    ('13', 'Python Object Instance', ''),
    ('14', 'UI Widget', '')
]
