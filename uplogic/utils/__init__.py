'''TODO: Documentation
'''

from bge import logic, render
from bge.types import KX_GameObject as GameObject
from mathutils import Vector
import bpy
import json
import math
import operator


###############################################################################
# CONSTANTS
###############################################################################

class _Status(object):
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return self._name


NO_VALUE = _Status("NO_VALUE")
STATUS_WAITING = _Status("WAITING")
STATUS_READY = _Status("READY")
STATUS_INVALID = _Status("INVALID")


# uplogic game properties
VEHICLE = '.ulvehicleconst'
SHIP = '.ulshipconst'
FLOATSAM = '.ulfloatsamconst'

WATER = '.ulwater'


LOGIC_OPERATORS = [
    operator.eq,
    operator.ne,
    operator.gt,
    operator.lt,
    operator.ge,
    operator.le
]


LO_AXIS_TO_STRING_CODE = {
    0: "X", 1: "Y", 2: "Z",
    3: "-X", 4: "-Y", 5: "-Z",
}


LO_AXIS_TO_VECTOR = {
    0: Vector((1, 0, 0)), 1: Vector((0, 1, 0)),
    2: Vector((0, 0, 1)), 3: Vector((-1, 0, 0)),
    4: Vector((0, -1, 0)), 5: Vector((0, 0, -1)),
}


###############################################################################
# LOGIC NODES
###############################################################################


def _name_query(named_items, query):
    assert len(query) > 0
    postfix = (query[0] == "*")
    prefix = (query[-1] == "*")
    infix = (prefix and postfix)
    if infix:
        token = query[1:-1]
        for item in named_items:
            if token in item.name:
                return item
    if prefix:
        token = query[:-1]
        for item in named_items:
            if item.name.startswith(token):
                return item
    if postfix:
        token = query[1:]
        for item in named_items:
            if item.name.endswith(token):
                return item
    for item in named_items:
        if item.name == query:
            return item
    return None


def check_game_object(query, scene=None):
    '''TODO: Documentation
    '''
    if not scene:
        scene = logic.getCurrentScene()
    else:
        scene = scene
    if (query is None) or (query == ""):
        return
    if not is_invalid(scene):
        # find from scene
        return _name_query(scene.objects, query)


def compute_distance(parama, paramb) -> float:
    '''TODO: Documentation
    '''
    if is_invalid(parama):
        return None
    if is_invalid(paramb):
        return None
    if hasattr(parama, "getDistanceTo"):
        return parama.getDistanceTo(paramb)
    if hasattr(paramb, "getDistanceTo"):
        return paramb.getDistanceTo(parama)
    va = Vector(parama)
    vb = Vector(paramb)
    return (va - vb).length


def debug(message: str):
    if not hasattr(bpy.types.Scene, 'logic_node_settings'):
        return
    if not bpy.context or not bpy.context.scene:
        return
    if not bpy.context.scene.logic_node_settings.use_node_debug:
        return
    else:
        print('[UPLOGIC] ' + message)


def is_invalid(*a) -> bool:
    for ref in a:
        if ref is None or ref is STATUS_WAITING or ref == '':
            return True
        if not hasattr(ref, "invalid"):
            continue
        elif ref.invalid:
            return True
    return False


def is_waiting(*args) -> bool:
    if STATUS_WAITING in args:
        return True
    return False


def make_valid_name(name):
    valid_characters = (
        "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    )
    clsname = name.replace(' ', '_')
    stripped_name = "".join(
        [c for c in clsname if c in valid_characters]
    )
    return stripped_name


def not_met(*conditions) -> bool:
    for c in conditions:
        if (
            c is STATUS_WAITING or
            c is None or
            c is False
        ):
            return True
    return False


def load_user_module(module_name, clsname):
    import sys
    order = f'import {module_name}'
    print(order)
    exec(order)
    print('#######################################################')
    for t in globals():
        print(t)
    print('#######################################################')
    print(sys.modules[module_name].globals())  # {clsname}']()


def unload_nodes(a, b):
    if not hasattr(bpy.types.Scene, 'nl_globals_initialized'):
        return
    delattr(bpy.types.Scene, 'nl_globals_initialized')


def move_to(
    moving_object,
    destination_point,
    speed,
    time_per_frame,
    dynamic,
    distance
):
    if dynamic:
        direction = (
            destination_point -
            moving_object.worldPosition)
        dst = direction.length
        if(dst <= distance):
            return True
        direction.z = 0
        direction.normalize()
        velocity = direction * speed
        velocity.z = moving_object.worldLinearVelocity.z
        moving_object.worldLinearVelocity = velocity
        return False
    else:
        direction = (
            destination_point -
            moving_object.worldPosition
            )
        dst = direction.length
        if(dst <= distance):
            return True
        direction.normalize()
        displacement = speed * time_per_frame
        motion = direction * displacement
        moving_object.worldPosition += motion
        return False


def project_vector3(v, xi, yi):
    return Vector((v[xi], v[yi]))


def xrot_to(
    rotating_object,
    target_pos,
    front_axis_code,
    speed,
    time_per_frame
):
    front_vector = LO_AXIS_TO_VECTOR[front_axis_code]
    vec = rotating_object.getVectTo(target_pos)[1]
    if speed == 0:
        if front_axis_code >= 3:
            vec.negate()
            front_axis_code = front_axis_code - 3
        if vec.x == vec.y == vec.z == 0:
            return
        rotating_object.alignAxisToVect(vec, front_axis_code, 1.0)
        rotating_object.alignAxisToVect(LO_AXIS_TO_VECTOR[0], 0, 1.0)
        return True
    else:
        vec = project_vector3(vec, 1, 2)
        vec.normalize()
        front_vector = rotating_object.getAxisVect(front_vector)
        front_vector = project_vector3(front_vector, 1, 2)
        signed_angle = vec.angle_signed(front_vector, None)
        if signed_angle is None:
            return
        abs_angle = abs(signed_angle)
        if abs_angle < 0.01:
            return True
        angle_sign = (signed_angle > 0) - (signed_angle < 0)
        drot = angle_sign * abs_angle * speed * time_per_frame
        eulers = rotating_object.localOrientation.to_euler()
        eulers[0] += drot
        rotating_object.localOrientation = eulers
        return False


def yrot_to(
    rotating_object,
    target_pos,
    front_axis_code,
    speed,
    time_per_frame
):
    front_vector = LO_AXIS_TO_VECTOR[front_axis_code]
    vec = rotating_object.getVectTo(target_pos)[1]
    if speed == 0:
        if front_axis_code >= 3:
            vec.negate()
            front_axis_code = front_axis_code - 3
        if vec.x == vec.y == vec.z == 0:
            return
        rotating_object.alignAxisToVect(vec, front_axis_code, 1.0)
        rotating_object.alignAxisToVect(LO_AXIS_TO_VECTOR[1], 1, 1.0)
        return True
    else:
        vec = project_vector3(vec, 2, 0)
        vec.normalize()
        front_vector = rotating_object.getAxisVect(front_vector)
        front_vector = project_vector3(front_vector, 2, 0)
        signed_angle = vec.angle_signed(front_vector, None)
        if signed_angle is None:
            return
        abs_angle = abs(signed_angle)
        if abs_angle < 0.01:
            return True
        angle_sign = (signed_angle > 0) - (signed_angle < 0)
        drot = angle_sign * abs_angle * speed * time_per_frame
        eulers = rotating_object.localOrientation.to_euler()
        eulers[1] += drot
        rotating_object.localOrientation = eulers
        return False


def zrot_to(
    rotating_object,
    target_pos,
    front_axis_code,
    speed,
    time_per_frame
):
    front_vector = LO_AXIS_TO_VECTOR[front_axis_code]
    vec = rotating_object.getVectTo(target_pos)[1]
    if speed == 0:
        if front_axis_code >= 3:
            vec.negate()
            front_axis_code = front_axis_code - 3
        if vec.x == vec.y == vec.z == 0:
            return
        rotating_object.alignAxisToVect(vec, front_axis_code, 1.0)
        rotating_object.alignAxisToVect(LO_AXIS_TO_VECTOR[2], 2, 1.0)
        return True
    else:
        # project in 2d, compute angle diff, set euler rot 2
        vec = project_vector3(vec, 0, 1)
        vec.normalize()
        front_vector = rotating_object.getAxisVect(front_vector)
        front_vector = project_vector3(front_vector, 0, 1)
        signed_angle = vec.angle_signed(front_vector, None)
        if signed_angle is None:
            return True
        abs_angle = abs(signed_angle)
        if abs_angle < 0.01:
            return True
        angle_sign = (signed_angle > 0) - (signed_angle < 0)
        drot = angle_sign * abs_angle * speed * time_per_frame
        eulers = rotating_object.localOrientation.to_euler()
        eulers[2] += drot
        rotating_object.localOrientation = eulers
        return False


def rot_to(
    rot_axis_index,
    rotating_object,
    target_pos,
    front_axis_code,
    speed,
    time_per_frame
):
    if rot_axis_index == 0:
        return xrot_to(
            rotating_object,
            target_pos,
            front_axis_code,
            speed,
            time_per_frame
        )
    elif rot_axis_index == 1:
        return yrot_to(
            rotating_object,
            target_pos,
            front_axis_code,
            speed,
            time_per_frame
        )
    elif rot_axis_index == 2:
        return zrot_to(
            rotating_object,
            target_pos,
            front_axis_code,
            speed,
            time_per_frame
        )


###############################################################################
# DATA
###############################################################################

def load_json_as_dict(filepath):
    if not filepath.endswith('.json'):
        path = f'{filepath}.json'
    if path:
        f = open(path, 'r')
        data = json.load(f)
        f.close()
        return data


###############################################################################
# SCENE
###############################################################################

def make_unique_light(old_lamp_ge: GameObject) -> GameObject:
    '''TODO: Documentation
    '''
    scene = logic.getCurrentScene()
    name = old_lamp_ge.name
    old_lamp = old_lamp_ge.blenderObject
    old_lamp.name = 'OLD_LAMP'

    settings = [
        'color',
        'energy',
        'diffuse_factor',
        'specular_factor',
        'volume_factor',
        'shadow_soft_size',
        'use_custom_distance',
        'cutoff_distance',
        'spot_size',
        'spot_blend',
        'show_cone',
        'angle',
        'shape',
        'size',
        'size_y',
        'use_shadow',
        'shadow_buffer_clip_start',
        'shadow_buffer_bias',
        'use_soft_shadows',
        'use_contact_shadow',
        'contact_shadow_distance',
        'contact_shadow_bias',
        'contact_shadow_thickness',
        'shadow_cascade_count',
        'shadow_cascade_fade',
        'shadow_cascade_max_distance',
        'shadow_cascade_exponent'
    ]

    types = {
        'POINT': 'Point',
        'AREA': 'Area',
        'SPOT': 'Spot',
        'SUN': 'Sun'
    }

    light_type = old_lamp.data.type
    bpy.ops.object.light_add(
        type=light_type,
        location=old_lamp_ge.worldPosition,
        rotation=old_lamp_ge.worldOrientation.to_euler()
    )
    index = 1
    light = None
    while light is None:
        if types[light_type] in bpy.data.objects[-index].name:
            light = bpy.data.objects[-index]
        index += 1
    for attr in settings:
        try:
            setattr(light.data, attr, getattr(old_lamp.data, attr))
        except Exception:
            pass
    light.name = name
    new_lamp_ge = scene.convertBlenderObject(light)
    for p in old_lamp_ge.getPropertyNames():
        new_lamp_ge[p] = old_lamp_ge[p]
    old_lamp_ge.endObject()
    real_name = light.name
    light.name = real_name
    if old_lamp_ge.parent:
        new_lamp_ge.setParent(old_lamp_ge.parent)
    return new_lamp_ge


def get_closest_instance(game_obj: GameObject, name: str):
    '''TODO: Documentation
    '''
    objs = []
    distances = {}
    for obj in logic.getCurrentScene().objects:
        if obj.name == name:
            objs.append(obj)
    for obj in objs:
        distances[game_obj.getDistanceTo(obj)] = obj
    return distances[min(distances.keys())]


def is_water(game_object: GameObject):
    return WATER in game_object


###############################################################################
# MATH
###############################################################################


def clamp(value: float, min: float = 0, max: float = 1) -> float:
    """Clamp a value in between two other values.

    :param value: input value
    :param min: minimum value
    :param max: maximum value

    :returns: clamped value as float
    """

    if value < min:
        return min
    if value > max:
        return max
    return value


def vec_clamp(vec: Vector, min: float = 0, max: float = 1) -> Vector:
    """Clamp length of a vector.

    :param value: `Vector`
    :param min: minimum length
    :param max: maximum length

    :returns: clamped vector as float
    """
    vec = vec.copy()

    if vec.length < min:
        vec.normalize()
        return vec * min
    if vec.length > max:
        vec.normalize()
        return vec * max
    return vec


def interpolate(a: float, b: float, fac: float) -> float:
    """Interpolate between 2 values using a factor.

    :param a: starting value
    :param b: target value
    :param fac: interpolation factor

    :returns: calculated value as float
    """
    if -.001 < a-b < .001:
        return b
    return (fac * b) + ((1-fac) * a)


def lerp(a: float, b: float, fac: float) -> float:
    """Interpolate between 2 values using a factor.

    :param a: starting value
    :param b: target value
    :param fac: interpolation factor

    :returns: calculated value as float
    """
    if -.001 < a-b < .001:
        return b
    return (fac * b) + ((1-fac) * a)


def vec_abs(vec):
    """Make every value of this vector positive.\n
    Only supports less than 4 Dimensions.

    :param a: `Vector`

    :returns: positive vector
    """
    vec = vec.copy()
    vec.x = abs(vec.x)
    vec.y = abs(vec.y)
    vec.z = abs(vec.z)
    return vec


def get_angle(a: Vector, b: Vector, up=Vector((0, 0, 1))) -> float:
    """Get the angle between the direction from a to b and up.

    :param a: `Vector` a
    :param b: `Vector` b
    :param up: compare direction

    :returns: calculated value as float
    """
    direction = get_direction(a, b)
    rad: float = direction.angle(up)
    deg: float = rad * 180/math.pi
    return deg


def get_direction(a, b, local=False) -> Vector:
    """Get the direction from one vector to another.

    :param a: `Vector` a
    :param b: `Vector` b
    :param local: use local space (position only)

    :returns: direction as `Vector`
    """
    start = a.worldPosition.copy() if hasattr(a, "worldPosition") else a
    if hasattr(b, "worldPosition"):
        b = b.worldPosition.copy()
    if local:
        b = start + b
    d = b - start
    d.normalize()
    return d


def ray_data(origin, dest, local, dist):
    """Get necessary data to calculate the ray.\n
    Not intended for manual use.
    """
    start = (
        origin.worldPosition.copy()
        if hasattr(origin, "worldPosition")
        else origin
    )
    if hasattr(dest, "worldPosition"):
        dest = dest.worldPosition.copy()
    if local:
        dest = start + dest
    d = dest - start
    d.normalize()
    return d, dist if dist else (start - dest).length, dest


def raycast(
    caster,
    origin,
    dest,
    distance=0,
    property_name='',
    xray=False,
    local=False,
    visualize=False
):
    """Raycast from any point to any target

    :param caster: casting object, this object will be ignored by the ray.
    :param origin: origin point; any vector or list.
    :param dest: target point; any vector or list.
    :param distance: distance the ray will be cast
    (0 means the ray will only be cast to target).
    :param property_name: look only for this property,
    leave empty to look for all.
    :param xray: look for objects behind others.
    :param local: add the target vector to the origin.
    :param visualize: show the raycast.

    :returns: obj, point, normal, direction
    """
    direction, distance, dest = ray_data(origin, dest, local, distance)
    obj, point, normal = caster.rayCast(
        dest,
        origin,
        distance,
        property_name,
        xray=xray
    )
    if visualize:
        origin = getattr(origin, 'worldPosition', origin)
        line_dest: Vector = direction.copy()
        line_dest.x *= distance
        line_dest.y *= distance
        line_dest.z *= distance
        line_dest = line_dest + origin
        render.drawLine(
            origin,
            line_dest,
            [1, 0, 0, 1]
        )
        if obj:
            render.drawLine(
                origin,
                point,
                [0, 1, 0, 1]
            )
    return obj, point, normal, direction
