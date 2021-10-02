from bge import logic
import bge
from bge.types import KX_GameObject as GameObject
import bpy
import aud
from mathutils import Vector, Euler, Matrix, Quaternion
import math
import numbers
import collections
import time
import os
import random
import sys
import operator
import json


DISTANCE_MODELS = {
    'INVERSE': aud.DISTANCE_MODEL_INVERSE,
    'INVERSE_CLAMPED': aud.DISTANCE_MODEL_INVERSE_CLAMPED,
    'EXPONENT': aud.DISTANCE_MODEL_EXPONENT,
    'EXPONENT_CLAMPED': aud.DISTANCE_MODEL_EXPONENT_CLAMPED,
    'LINEAR': aud.DISTANCE_MODEL_LINEAR,
    'LINEAR_CLAMPED': aud.DISTANCE_MODEL_LINEAR_CLAMPED,
    'NONE': aud.DISTANCE_MODEL_INVALID
}


def interpolate(a: float, b: float, fac: float):
    return (fac * b) + ((1-fac) * a)


def alpha_move(a, b, fac):
    if a < b:
        return a + fac
    elif a > b:
        return a - fac
    else:
        return a


class Invalid():
    pass


class _Status(object):
    def __init__(self, name):
        self._name = name

    def __repr__(self):
        return self._name


STATUS_WAITING = _Status("WAITING")
STATUS_READY = _Status("READY")
NO_VALUE = _Status("NO_VALUE")


# Persistent maps

class GlobalDB(object):
    index: int

    class LineBuffer(object):
        def __init__(self, buffer=[]):
            self.buffer = buffer
            self.index = 0
            self.size = len(self.buffer)

        def read(self):
            line = self.buffer[self.index]
            self.index += 1
            return line

        def write(self, line):
            self.buffer.append(line + "\n")

        def has_next(self):
            return self.index < self.size

        def flush(self, file):
            with open(file, "a") as f:
                f.writelines(self.buffer)

    class Serializer(object):
        def read(self, line_reader):
            raise NotImplementedError()

        def write(self, value, line_writer):
            raise NotImplementedError()

    serializers = {}
    storage_dir = logic.expandPath("//Globals")
    shared_dbs = {}

    @classmethod
    def retrieve(cls, fname):
        db = cls.shared_dbs.get(fname)
        if db is None:
            db = GlobalDB(fname)
            cls.shared_dbs[fname] = db
        return db

    @classmethod
    def get_storage_dir(cls):
        return cls.storage_dir

    @classmethod
    def put_value(cls, key, value, buffer):
        type_name = str(type(value))
        serializer = cls.serializers.get(type_name)
        if not serializer:
            return False
        buffer.write("PUT")
        buffer.write(key)
        buffer.write(type_name)
        serializer.write(value, buffer)

    @classmethod
    def read_existing(cls, fpath, intodic):
        lines = []
        with open(fpath, "r") as f:
            lines.extend(f.read().splitlines())
        buffer = GlobalDB.LineBuffer(lines)
        log_size = 0
        while buffer.has_next():
            op = buffer.read()
            assert op == "PUT"
            key = buffer.read()
            type_id = buffer.read()
            serializer = GlobalDB.serializers.get(type_id)
            value = serializer.read(buffer)
            intodic[key] = value
            log_size += 1
        return log_size

    @classmethod
    def write_put(cls, fname, key, value):
        type_name = str(type(value))
        serializer = cls.serializers.get(type_name)
        if not serializer:
            return  # no serializer for given value type
        if not os.path.exists(cls.get_storage_dir()):
            os.mkdir(cls.get_storage_dir())
        fpath = os.path.join(
            cls.get_storage_dir(),
            "{}.logdb.txt".format(fname)
        )
        buffer = GlobalDB.LineBuffer()
        cls.put_value(key, value, buffer)
        buffer.flush(fpath)

    @classmethod
    def read(cls, fname, intodic):
        fpath = os.path.join(
            cls.get_storage_dir(),
            "{}.logdb.txt".format(fname)
        )
        if os.path.exists(fpath):
            return cls.read_existing(fpath, intodic)
        else:
            return 0

    @classmethod
    def compress(cls, fname, data):
        buffer = GlobalDB.LineBuffer()
        for key in data:
            value = data[key]
            cls.put_value(key, value, buffer)
        fpath = os.path.join(
            cls.get_storage_dir(),
            "{}.logdb.txt".format(fname)
        )
        with open(fpath, "w") as f:
            f.writelines(buffer.buffer)

    def __init__(self, file_name):
        self.fname = file_name
        self.data = {}

        filter(lambda a: a.__name__ == 'unload_nodes', bpy.app.handlers.game_post)
        remove_f = []
        for f in bpy.app.handlers.game_post:
            if f.__name__ == 'unload_nodes':
                remove_f.append(f)
        for f in remove_f:
            bpy.app.handlers.game_post.remove(f)
        bpy.app.handlers.game_post.append(unload_nodes)

        log_size = GlobalDB.read(self.fname, self.data)
        if log_size > (5 * len(self.data)):
            debug("Compressing sld {}".format(file_name))
            GlobalDB.compress(self.fname, self.data)

    def get(self, key, default_value=None):
        return self.data.get(key, default_value)

    def clear(self):
        self.data.clear()

    def put(self, key, value, persist=True):
        self.data[key] = value
        if persist:
            old_value = self.data.get(key)
            changed = old_value != value
            if changed:
                GlobalDB.write_put(self.fname, key, value)

    def pop(self, key, default):
        return self.data.pop(key, None)

    def log(self):
        print(self.data)


class StringSerializer(GlobalDB.Serializer):

    def write(self, value, line_writer):
        line_writer.write(value)

    def read(self, line_reader):
        data = line_reader.read()
        return None if data == "None" else data


class FloatSerializer(GlobalDB.Serializer):

    def write(self, value, line_writer): line_writer.write(str(value))

    def read(self, line_reader):
        data = line_reader.read()
        return None if data == "None" else float(data)


class IntegerSerializer(GlobalDB.Serializer):

    def write(self, value, line_writer): line_writer.write(str(value))

    def read(self, line_reader):
        data = line_reader.read()
        return None if data == "None" else int(data)


class ListSerializer(GlobalDB.Serializer):

    def write(self, value, line_writer):
        line_writer.write(str(len(value)))
        for e in value:
            tp = str(type(e))
            serializer = GlobalDB.serializers.get(tp)
            if serializer:
                line_writer.write(tp)
                serializer.write(e, line_writer)

    def read(self, line_reader):
        data = []
        count = int(line_reader.read())
        for i in range(0, count):
            tp = line_reader.read()
            serializer = GlobalDB.serializers.get(tp)
            value = serializer.read(line_reader)
            data.append(value)
        return data


class VectorSerializer(GlobalDB.Serializer):
    def write(self, value, line_writer):
        if value is None:
            line_writer.write("None")
        else:
            line = ""
            for i in value:
                line += str(i) + " "
            line_writer.write(line)

    def read(self, line_reader):
        line = line_reader.read()
        if line == "None":
            return None
        data = line.rstrip().split(" ")
        components = [float(d) for d in data]
        return Vector(components)


GlobalDB.serializers[str(type(""))] = StringSerializer()
GlobalDB.serializers[str(type(1.0))] = FloatSerializer()
GlobalDB.serializers[str(type(10))] = IntegerSerializer()
GlobalDB.serializers[str(type([]))] = ListSerializer()
GlobalDB.serializers[str(type((0, 0, 0)))] = ListSerializer()
GlobalDB.serializers[str(type(Vector()))] = (
    VectorSerializer()
)

# End of persistent maps

LO_AXIS_TO_STRING_CODE = {
    0: "X", 1: "Y", 2: "Z",
    3: "-X", 4: "-Y", 5: "-Z",
}

LO_AXIS_TO_VECTOR = {
    0: Vector((1, 0, 0)), 1: Vector((0, 1, 0)),
    2: Vector((0, 0, 1)), 3: Vector((-1, 0, 0)),
    4: Vector((0, -1, 0)), 5: Vector((0, 0, -1)),
}

LOGIC_OPERATORS = [
    operator.eq,
    operator.ne,
    operator.gt,
    operator.lt,
    operator.ge,
    operator.le
]


# distance between objects or vectors or tuples. None if not computable
def compute_distance(parama, paramb):
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


def debug(message):
    if not hasattr(bpy.types.Scene, 'logic_node_settings'):
        return
    if not bpy.context or not bpy.context.scene:
        return
    if not bpy.context.scene.logic_node_settings.use_node_debug:
        return
    else:
        print('[Logic Nodes] ' + message)


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
    pass


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


def stop_all_sounds(a, b):
    if not hasattr(bpy.types.Scene, 'nl_aud_system'):
        return
    bpy.types.Scene.nl_aud_system.device.stopAll()
    delattr(bpy.types.Scene, 'nl_aud_system')


def unload_nodes(a, b):
    if not hasattr(bpy.types.Scene, 'nl_globals_initialized'):
        return
    delattr(bpy.types.Scene, 'nl_globals_initialized')


def check_game_object(query, scene=None):
    if not scene:
        scene = logic.getCurrentScene()
    else:
        scene = scene
    if (query is None) or (query == ""):
        return
    if not is_invalid(scene):
        # find from scene
        return _name_query(scene.objects, query)


def invalid(ref):
    if ref is None:
        return False
    if not hasattr(ref, "invalid"):
        return False
    return ref.invalid


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


_loaded_userlogic_files = {}


def load_user_logic(module_name):
    full_path = logic.expandPath(
        "//bgelogic/cells/{}.py".format(module_name)
    )
    loaded_value = _loaded_userlogic_files.get(full_path)
    if loaded_value:
        return loaded_value
    import sys
    python_version = sys.version_info
    major = python_version[0]
    minor = python_version[1]
    if (major < 3) or (major == 3 and minor < 3):
        import imp
        loaded_value = imp.load_source(module_name, full_path)
    elif (major == 3) and (minor < 5):
        from importlib.machinery import SourceFileLoader
        loaded_value = SourceFileLoader(module_name, full_path).load_module()
    else:
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, full_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        loaded_value = module
    _loaded_userlogic_files[module_name] = loaded_value
    return loaded_value


def load_user_module(module_name):
    import sys
    exec("import {}".format(module_name))
    return sys.modules[module_name]


class AudioSystem(object):
    def __init__(self):
        self.active_sounds = []
        self.listener = logic.getCurrentScene().active_camera
        self.old_lis_pos = self.listener.worldPosition.copy()
        bpy.types.Scene.nl_aud_system = self
        self.device = aud.Device()
        self.device.distance_model = aud.DISTANCE_MODEL_INVERSE_CLAMPED
        self.device.speed_of_sound = bpy.context.scene.audio_doppler_speed
        self.device.doppler_factor = bpy.context.scene.audio_doppler_factor

        filter(lambda a: a.__name__ == 'stop_all_sounds', bpy.app.handlers.game_post)
        remove_f = []
        for f in bpy.app.handlers.game_post:
            if f.__name__ == 'stop_all_sounds':
                remove_f.append(f)
        for f in remove_f:
            bpy.app.handlers.game_post.remove(f)
        bpy.app.handlers.game_post.append(stop_all_sounds)

    def get_distance_model(self, name):
        return DISTANCE_MODELS.get(name, aud.DISTANCE_MODEL_INVERSE_CLAMPED)

    def compute_listener_velocity(self, listener):
        wpos = listener.worldPosition.copy()
        olp = self.old_lis_pos
        vel = (
            (wpos.x - olp.x) * 50,
            (wpos.y - olp.y) * 50,
            (wpos.z - olp.z) * 50
        )
        self.old_lis_pos = wpos
        return vel

    def update(self, network):
        c = logic.getCurrentScene().active_camera
        self.listener = c
        if not self.active_sounds:
            return  # do not update if no sound has been installed
        # update the listener data
        dev = self.device
        listener_vel = self.compute_listener_velocity(c)
        dev.listener_location = c.worldPosition
        dev.listener_orientation = c.worldOrientation.to_quaternion()
        dev.listener_velocity = listener_vel


class GELogicBase(object):
    def get_value(self): pass
    def has_status(self, status): pass


class GELogicContainer(GELogicBase):

    def __init__(self):
        self._uid = None
        self._status = STATUS_WAITING
        self._value = None
        self._children = []
        self.network = None
        self.is_waiting = False

    def get_value(self):
        return self._value

    def _set_value(self, value):
        self._value = value

    def setup(self, network):
        """
        This is called by the network once, after all the
        cells have been loaded into the tree.
        :return: None
        """
        pass

    def stop(self, network):
        pass

    def _set_ready(self):
        self._status = STATUS_READY

    def _set_status(self, status):
        """
        Check the current status of the cell. Should return
        True if status equals the current status of the cell.
        :param status:
        :return:
        """
        self._status = status

    def has_status(self, status):
        return status == self._status

    def get_game_object(self, param, scene):
        if str(param) == 'NLO:U_O':
            return self.network._owner
        else:
            return check_game_object(param.split(':')[-1], scene)

    def get_socket_value(self, param, scene=None):
        if str(param).startswith('NLO:'):
            return self.get_game_object(param, scene)
        if isinstance(param, GELogicBase):
            if param.has_status(STATUS_READY):
                return param.get_value()
            else:
                return STATUS_WAITING
        else:
            return param

    def reset(self):
        """
        Resets the status of the cell to GELogicContainer.STATUS_WAITING.
        A cell may override this to reset other states
        or to keep the value at STATUS_READY if evaluation is required
        to happen only once (or never at all)
        :return:
        """
        self._set_status(STATUS_WAITING)

    def evaluate(self):
        """
        A logic cell implements this method to do its job. The network
        evaluates a cell until its status becomes
         LogicNetwor.STATUS_READY. When that happens, the cell is
         removed from the update queue.
        :return:
        """
        raise NotImplementedError(
            "{} doesn't implement evaluate".format(self.__class__.__name__)
        )

    def _always_ready(self, status):
        return status is STATUS_READY

    def _skip_evaluate(self):
        return

    def deactivate(self):
        self.has_status = self._always_ready
        self.evaluate = self._skip_evaluate


class GEOutSocket(GELogicBase):

    def __init__(self, node, value_getter):
        self.node = node
        self.get_value = value_getter

    def has_status(self, status):
        return self.node.has_status(status)


class GELogicTree(GELogicContainer):
    def __init__(self):
        GELogicContainer.__init__(self)
        self._cells = []
        self._iter = collections.deque()
        self._lastuid = 0
        self._owner = None
        self._max_blocking_loop_count = 0
        self._events = GlobalDB.retrieve('NL_MessageService')
        self.keyboard = None
        self.mouse = None
        self.keyboard_events = None
        self.active_keyboard_events = None
        self.mouse_events = None
        self.stopped = False
        self.timeline = 0.0
        self._time_then = None
        self.time_per_frame = 0.0
        self._do_remove = False
        self._last_mouse_position = [
            logic.mouse.position[0], logic.mouse.position[1]
        ]
        self.mouse_motion_delta = [0.0, 0.0]
        self.mouse_wheel_delta = 0
        self.aud_system_owner = False
        self.init_glob_cats()
        self.audio_system = self.create_aud_system()
        self.sub_networks = []  # a list of networks updated by this network
        self.capslock_pressed = False
        self.evaluated_cells = 0
        bpy.app.handlers.depsgraph_update_post.append(self.on_scene_update)

    def on_scene_update(self, a, b):
        if self._do_remove:
            self.clear_events()

    def create_aud_system(self):
        if not hasattr(bpy.types.Scene, 'nl_aud_system'):
            self.aud_system_owner = True
            return AudioSystem()
        else:
            return bpy.types.Scene.nl_aud_system

    def init_glob_cats(self):
        if not hasattr(bpy.types.Scene, 'nl_globals_initialized'):
            scene = bge.logic.getCurrentScene()
            cats = getattr(bpy.data.scenes[scene.name], 'nl_global_categories', None)
            if not cats:
                return

            msg = ''

            dat = {
                'STRING': 'string_val',
                'FLOAT': 'float_val',
                'INTEGER': 'int_val',
                'BOOLEAN': 'bool_val',
                'FILE_PATH': 'filepath_val'
            }

            for c in cats:
                db = GlobalDB.retrieve(c.name)
                msg += f' {c.name},'
                for v in c.content:
                    val = getattr(v , dat.get(v.value_type, 'FLOAT'), 0)
                    db.put(v.name, val, v.persistent)

            if msg:
                debug(f'Globals Initialized:{msg[:-1]}')
            bpy.types.Scene.nl_globals_initialized = True

    def ray_cast(
        self,
        caster_object,
        ray_origin,
        ray_destination,
        property,
        xray,
        distance
    ):
        now = time.time()
        cached_data = caster_object.get("_NL_ray_cast_data")
        if cached_data is not None:
            data_time = cached_data[0]
            data_origin = cached_data[1]
            data_destination = cached_data[2]
            data_property = cached_data[3]
            data_distance = cached_data[4]
            d_time = now - data_time
            # only if we are in the same frame,
            # otherwise scenegraph might have changed
            if d_time < 0.01:
                if (
                    (data_origin == ray_origin) and
                    (data_destination == ray_destination) and
                    (data_property == property) and
                    (data_distance == distance)
                ):
                    return cached_data[5]
            pass
        obj, point, normal = None, None, None
        if property is not None:
            obj, point, normal = caster_object.rayCast(
                ray_destination,
                ray_origin,
                distance,
                property,
                xray=xray
            )
        else:
            obj, point, normal = caster_object.rayCast(
                ray_destination,
                ray_origin,
                distance,
                xray=xray
            )
        cached_data = (
            now,
            ray_origin,
            ray_destination,
            property,
            distance,
            (obj, point, normal)
        )
        caster_object["_NL_ray_cast_data"] = cached_data
        return obj, point, normal

    def set_mouse_position(self, screen_x, screen_y):
        self.mouse.position = (screen_x, screen_y)
        self._last_mouse_position = [screen_x, screen_y]
        pass

    def get_owner(self):
        return self._owner

    def setup(self):
        self.time_per_frame = 0.0
        for cell in self._cells:
            cell.network = self
            cell.setup(self)
        self._last_mouse_position[:] = logic.mouse.position

    def is_running(self):
        return not self.stopped

    def is_stopped(self):
        return self.stopped

    def stop(self, network=None):
        self.clear_events()
        if self.stopped:
            return
        self._time_then = None
        self.stopped = True
        for cell in self._cells:
            cell.stop(self)

    def _generate_cell_uid(self):
        self._lastuid += 1
        return self._lastuid

    def clear_events(self):
        li = []
        for m in self._events.data:
            if self._events.data[m][2] in self._cells:
                li.append(m)
        for m in li:
            self._events.pop(m, None)
        del li

    def add_cell(self, cell):
        self._cells.append(cell)
        self._iter.append(cell)
        self._max_blocking_loop_count = len(self._cells) * len(self._cells)
        cell._uid = self._generate_cell_uid()
        return cell

    def evaluate(self):
        now = time.time()
        if self._time_then is None:
            self._time_then = now
        dtime = now - self._time_then
        self._time_then = now
        self.timeline += dtime
        self.time_per_frame = dtime
        if self._owner.invalid:
            self.clear_events()
            debug("Network Owner removed from game. Shutting down the network")
            return True
        self.keyboard = logic.keyboard
        self.mouse = logic.mouse
        # compute mouse translation since last frame (or initialization)
        curr_mpos = self.mouse.position
        last_mpos = self._last_mouse_position
        mpos_delta = self.mouse_motion_delta
        mpos_delta[0] = curr_mpos[0] - last_mpos[0]
        mpos_delta[1] = curr_mpos[1] - last_mpos[1]
        last_mpos[:] = curr_mpos
        # store mouse and keyboard events to be used by cells
        self.keyboard_events = self.keyboard.inputs.copy()
        self.active_keyboard_events = self.keyboard.activeInputs.copy()
        caps_lock_event = self.keyboard_events[bge.events.CAPSLOCKKEY]
        if(caps_lock_event.released):
            self.capslock_pressed = not self.capslock_pressed
        me = self.mouse.inputs
        self.mouse_wheel_delta = 0
        if(me[bge.events.WHEELUPMOUSE].activated):
            self.mouse_wheel_delta = 1
        elif(
            me[bge.events.WHEELDOWNMOUSE].activated
        ):
            self.mouse_wheel_delta = -1
        self.mouse_events = me
        # update the cells
        cells = self._iter
        max_loop_count = len(cells)
        loop_index = 0
        done_cells = []
        while cells:
            if loop_index == self._max_blocking_loop_count:
                debug(
                    "Network found a blocking condition" +
                    " (due to unconnected or non responsive cell)"
                )
                debug("Stopping network...")
                self.stop()
                return
            cell = cells.popleft()
            if cell in done_cells:
                continue
            else:
                done_cells.append(cell)
            cell.evaluate()
            self.evaluated_cells += 1
            if not cell.has_status(STATUS_READY):
                cells.append(cell)
            loop_index += 1
        done_cells = []
        if(loop_index > max_loop_count):
            debug(
                "Wrong sorting alghorithm!",
                loop_index,
                max_loop_count)
        for cell in self._cells:
            cell.reset()
            if cell.has_status(STATUS_WAITING):
                cells.append(cell)
        # update the sound system
        if self.aud_system_owner:
            self.audio_system.update(self)
        # pulse subnetworks
        for network in self.sub_networks:
            if network._owner.invalid:
                self.sub_networks.remove(network)
            elif network.is_running():
                network.evaluate()

    def install_subnetwork(self, owner_object, node_tree_name, initial_status):
        # transform the tree name into a NL module name
        valid_characters = (
            "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        stripped_name = "".join(
            [c for c in node_tree_name if c in valid_characters]
        )
        if stripped_name in owner_object:
            debug("Network {} already installed for {}".format(
                    stripped_name, owner_object.name
                ))
            if(initial_status is True):
                owner_object[f'IGNLTree_{node_tree_name}'].stopped = False
        else:
            debug("Installing sub network...")
            initial_status_key = f'NL__{node_tree_name}'
            owner_object[initial_status_key] = initial_status
            module_name = 'bgelogic.NL{}'.format(stripped_name)
            module = load_user_module(module_name)
            module._initialize(owner_object)
            subnetwork = owner_object[f'IGNLTree_{node_tree_name}']
            self.sub_networks.append(subnetwork)


def is_waiting(*args):
    if STATUS_WAITING in args:
        return True
    return False


def is_invalid(*a):
    for ref in a:
        if ref is None or ref is STATUS_WAITING or ref == '':
            return True
        if not hasattr(ref, "invalid"):
            continue
        elif ref.invalid:
            return True
    return False


def not_met(*conditions):
    for c in conditions:
        if (
            c is STATUS_WAITING or
            c is None or
            c is False
        ):
            return True
    return False


###############################################################################
# Basic Cells
###############################################################################


class GELogicNode(GELogicContainer):
    pass


class GEParameterNode(GELogicNode):
    pass


class GEActionNode(GELogicNode):
    pass


class GEConditionNode(GELogicNode):
    pass


###############################################################################
# Events
###############################################################################
###############################################################################
# Game
###############################################################################
###############################################################################
# Input -> Mouse
###############################################################################
###############################################################################
# Input -> Gamepad
###############################################################################


class ConditionGamepadTrigger(GEConditionNode):
    def __init__(self, axis=0):
        GEConditionNode.__init__(self)
        self.axis = axis
        self.index = None
        self.sensitivity = None
        self.threshold = None
        self._value = None
        self.VAL = GEOutSocket(self, self.get_value)

    def get_x_axis(self):
        return self._value

    def evaluate(self):
        self._set_ready()
        axis = self.get_socket_value(self.axis)
        if is_invalid(axis):
            debug('Gamepad Trigger Node: Invalid Controller Trigger!')
            return
        index = self.get_socket_value(self.index)
        sensitivity = self.get_socket_value(self.sensitivity)
        threshold = self.get_socket_value(self.threshold)
        if logic.joysticks[index]:
            joystick = logic.joysticks[index]
        else:
            debug('Gamepad Trigger Node: No Joystick at that Index!')
            self._x_axis_values = 0
            self._y_axis_values = 0
            return
        if is_invalid(joystick):
            return
        value = joystick.axisValues[4] if axis == 0 else joystick.axisValues[5]

        if -threshold < value < threshold:
            value = 0
        self._value = value * sensitivity


class GEGamepadVibration(GEConditionNode):
    def __init__(self, axis=0):
        GEConditionNode.__init__(self)
        self.condition = None
        self.index = None
        self.left = None
        self.right = None
        self.time = None
        self.done = None
        self.DONE = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self._set_ready()
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        index = self.get_socket_value(self.index)
        left = self.get_socket_value(self.left)
        right = self.get_socket_value(self.right)
        time = self.get_socket_value(self.time)
        if is_waiting(index, left, right, time):
            return

        if not logic.joysticks[index]:
            return
        joystick = logic.joysticks[index]
        if not joystick.hasVibration:
            debug('Joystick at index {} has no vibration!'.format(index))
            return

        joystick.strengthLeft = left
        joystick.strengthRight = right
        joystick.duration = int(round(time * 1000))

        joystick.startVibration()
        self.done = True


###############################################################################
# Input -> Keyboard
###############################################################################


class ParameterKeyboardKeyCode(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.key_code = None

    def evaluate(self):
        self._set_ready()
        key_code = self.get_socket_value(self.key_code)
        self._set_value(key_code)


class ConditionKeyPressed(GEConditionNode):
    def __init__(self, pulse=False, key_code=None):
        GEConditionNode.__init__(self)
        self.pulse = pulse
        self.key_code = key_code
        self.network = None

    def setup(self, network):
        self.network = network

    def evaluate(self):
        keycode = self.get_socket_value(self.key_code)
        if is_waiting(keycode):
            return
        self._set_ready()
        keystat = self.network.keyboard_events[keycode]
        if self.pulse:
            self._set_value(
                (
                    keystat.active or keystat.activated
                )
            )
        else:
            self._set_value(keystat.activated)


class GEKeyboardActive(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
    
    def evaluate(self):
        self._set_ready()
        self._set_value(
            len(self.network.active_keyboard_events) > 0
        )


###############################################################################
# Unordered
###############################################################################


class ParamOwnerObject(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)

    def setup(self, network):
        GEParameterNode.setup(self, network)
        self._set_status(STATUS_READY)
        self._set_value(network.get_owner())

    def reset(self):
        pass

    def evaluate(self):
        pass


class ParameterBoneStatus(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.armature = None
        self.bone_name = None
        self._prev_armature = NO_VALUE
        self._prev_bone = NO_VALUE
        self._channel = None
        self._pos = Vector((0, 0, 0))
        self._rot = Euler((0, 0, 0), "XYZ")
        self._sca = Vector((0, 0, 0))
        self.XYZ_POS = GEOutSocket(self, self._get_pos)
        self.XYZ_ROT = GEOutSocket(self, self._get_rot)
        self.XYZ_SCA = GEOutSocket(self, self._get_sca)

    def _get_pos(self):
        return self._pos

    def _get_sca(self):
        return self._sca

    def _get_rot(self):
        return self._rot

    def evaluate(self):
        armature = self.get_socket_value(self.armature)
        bone_name = self.get_socket_value(self.bone_name)
        if is_invalid(armature, bone_name):
            return
        self._set_ready()
        channel = None
        if (
            (armature is self._prev_armature) and
            (bone_name == self._prev_bone)
        ):
            channel = self._channel
        else:
            self._prev_armature = armature
            self._prev_bone = bone_name
            self._channel = armature.channels[bone_name]
            channel = self._channel
        if channel.rotation_mode is logic.ROT_MODE_QUAT:
            self._rot[:] = (
                Quaternion(channel.rotation_quaternion).to_euler()
            )
        else:
            self._rot[:] = channel.rotation_euler
        self._pos[:] = channel.location
        self._sca[:] = channel.scale


class ParameterCurrentScene(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self._set_ready()

    def get_value(self):
        return logic.getCurrentScene()

    def reset(self): pass
    def evaluate(self): pass


class ParameterParentGameObject(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.game_object = None

    def evaluate(self):
        self._set_ready()
        game_object = self.get_socket_value(self.game_object)
        if is_invalid(game_object):
            return
        self._set_value(game_object.parent)


class ParameterAxisVector(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.game_object = None

    def evaluate(self):
        obj = self.get_socket_value(self.game_object)
        front_vector = LO_AXIS_TO_VECTOR[self.axis]
        if is_invalid(obj, front_vector):
            return
        self._set_ready()
        self._set_value(obj.getAxisVect(front_vector))


class GetObjectDataName(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.game_object = None

    def evaluate(self):
        obj = self.get_socket_value(self.game_object)
        if is_invalid(obj):
            return
        self._set_ready()
        self._set_value(obj.blenderObject.name)


class GetCurvePoints(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.curve = None

    def evaluate(self):
        obj = self.get_socket_value(self.curve)
        if is_invalid(obj):
            return
        self._set_ready()
        offset = obj.worldPosition
        o = obj.blenderObject.data.splines[0]
        if o.type == 'BEZIER':
            self._set_value([Vector(p.co) + offset for p in o.bezier_points])
        else:
            self._set_value([Vector(p.co[:-1]) + offset for p in o.points])


class GetObjectVertices(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.game_object = None

    def evaluate(self):
        obj = self.get_socket_value(self.game_object)
        if is_invalid(obj):
            return
        self._set_ready()

        offset = obj.worldPosition
        self._set_value(sorted([Vector(v.co) + offset for v in obj.blenderObject.data.vertices]))


class ParameterSwitchValue(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.state = None
        self.outcome = False
        self.TRUE = GEOutSocket(self, self.get_true_value)
        self.FALSE = GEOutSocket(self, self.get_false_value)

    def get_true_value(self):
        state = self.get_socket_value(self.state)
        if state:
            return True
        else:
            return False

    def get_false_value(self):
        state = self.get_socket_value(self.state)
        if state:
            return False
        else:
            return True

    def evaluate(self):
        state = self.get_socket_value(self.state)
        if is_waiting(state):
            return
        self._set_ready()
        if state:
            self.outcome = True
        self._set_value(self.outcome)


class ParameterObjectProperty(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.game_object = None
        self.property_name = None

    def evaluate(self):
        game_object = self.get_socket_value(self.game_object)
        property_name = self.get_socket_value(self.property_name)
        if is_invalid(game_object, property_name):
            return
        self._set_ready()
        if property_name not in game_object:
            game_object[property_name] = None
        else:
            self._set_value(game_object[property_name])


class ParameterGetNodeTreeNodeValue(GEParameterNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.tree_name = None
        self.node_name = None
        self.input_slot = None
        self.val = False
        self.OUT = GEOutSocket(self, self._get_val)

    def _get_val(self):
        return self.val

    def evaluate(self):
        tree_name = self.get_socket_value(self.tree_name)
        node_name = self.get_socket_value(self.node_name)
        if is_invalid(tree_name, node_name):
            return
        input_slot = self.get_socket_value(self.input_slot)
        if is_waiting(tree_name):
            return
        self._set_ready()
        self.val = (
            bpy.data.node_groups[tree_name]
            .nodes[node_name]
            .inputs[input_slot]
            .default_value
        )


class ParameterGetNodeTreeNodeAttribute(GEParameterNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.mat_name = None
        self.node_name = None
        self.internal = None
        self.attribute = None
        self.val = False
        self.OUT = GEOutSocket(self, self._get_val)

    def _get_val(self):
        return self.val

    def evaluate(self):
        mat_name = self.get_socket_value(self.mat_name)
        node_name = self.get_socket_value(self.node_name)
        if is_invalid(mat_name, node_name):
            return
        internal = self.get_socket_value(self.internal)
        attribute = self.get_socket_value(self.attribute)
        if is_waiting(mat_name):
            return
        self._set_ready()
        target = (
            bpy.data
            .node_groups[mat_name]
            .nodes[node_name]
        )
        if internal:
            target = getattr(target, internal, target)
        self.val = getattr(target, attribute, None)


class ParameterGetMaterialNodeValue(GEParameterNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.mat_name = None
        self.node_name = None
        self.input_slot = None
        self.val = False
        self.OUT = GEOutSocket(self, self._get_val)

    def _get_val(self):
        return self.val

    def evaluate(self):
        mat_name = self.get_socket_value(self.mat_name)
        node_name = self.get_socket_value(self.node_name)
        if is_invalid(mat_name, node_name):
            return
        input_slot = self.get_socket_value(self.input_slot)
        if is_waiting(mat_name):
            return
        self._set_ready()
        self.val = (
            bpy.data.materials[mat_name]
            .node_tree
            .nodes[node_name]
            .inputs[input_slot]
            .default_value
        )


class ParameterGetMaterialNodeAttribute(GEParameterNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.mat_name = None
        self.node_name = None
        self.internal = None
        self.attribute = None
        self.val = False
        self.OUT = GEOutSocket(self, self._get_val)

    def _get_val(self):
        return self.val

    def evaluate(self):
        mat_name = self.get_socket_value(self.mat_name)
        node_name = self.get_socket_value(self.node_name)
        if is_invalid(mat_name, node_name):
            return
        internal = self.get_socket_value(self.internal)
        attribute = self.get_socket_value(self.attribute)
        if is_waiting(mat_name):
            return
        self._set_ready()
        target = (
            bpy.data.materials[mat_name]
            .node_tree
            .nodes[node_name]
        )
        if internal:
            target = getattr(target, internal, target)
        self.val = getattr(target, attribute, None)


class ParameterGetMaterialNode(GEParameterNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.mat_name = None
        self.node_name = None
        self.val = False
        self.OUT = GEOutSocket(self, self._get_val)

    def _get_val(self):
        return self.val

    def evaluate(self):
        mat_name = self.get_socket_value(self.mat_name)
        node_name = self.get_socket_value(self.node_name)
        if is_invalid(mat_name, node_name):
            return
        self._set_ready()
        self.val = (
            bpy.data.materials[mat_name]
            .node_tree
            .nodes[node_name]
        )


class ParameterObjectHasProperty(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.game_object = None
        self.property_name = None

    def evaluate(self):
        game_object = self.get_socket_value(self.game_object)
        property_name = self.get_socket_value(self.property_name)
        if is_invalid(game_object, property_name):
            debug('Has Property Node: Object or Property Name invalid!')
            return
        self._set_ready()
        self._set_value(
            True if property_name in game_object.getPropertyNames()
            else False
        )


class ParameterDictionaryValue(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.dict = None
        self.key = None

    def evaluate(self):
        dictionary = self.get_socket_value(self.dict)
        key = self.get_socket_value(self.key)
        if is_invalid(dictionary, key):
            return
        self._set_ready()
        if key in dictionary:
            self._set_value(dictionary[key])
        else:
            debug("Dict Get Value Node: Key '{}' Not In Dict!".format(key))


class ParameterListIndex(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.items = None
        self.index = None

    def evaluate(self):
        list_d = self.get_socket_value(self.items)
        index = self.get_socket_value(self.index)
        if is_invalid(list_d):
            return
        if is_waiting(index):
            return
        self._set_ready()
        if index <= len(list_d) - 1:
            self._set_value(list_d[index])
        else:
            debug('List Index Node: Index Out Of Range!')


class ParameterRandomListIndex(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.condition = None
        self._item = None
        self.items = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            self._set_value(self._item)
            return
        list_d = self.get_socket_value(self.items)
        if is_invalid(list_d):
            return
        self._set_ready()
        self._item = random.choice(list_d)
        self._set_value(self._item)


class DuplicateList(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.condition = None
        self.items = None

    def evaluate(self):
        list_d = self.get_socket_value(self.items)
        if is_invalid(list_d):
            return
        self._set_ready()
        self._set_value(list_d.copy())


class GetActuator(GEParameterNode):

    @classmethod
    def act(cls, actuator):
        return actuator

    @classmethod
    def obj(cls, obj_name):
        return obj_name

    def __init__(self):
        GEParameterNode.__init__(self)
        self.obj_name = None
        self.act_name = None

    def evaluate(self):
        game_obj = self.get_socket_value(self.obj_name)
        if is_invalid(game_obj, self.act_name):
            return
        self._set_ready()
        self._set_value(game_obj.actuators[self.act_name])


class GetActuatorByName(GEParameterNode):

    def __init__(self):
        GEParameterNode.__init__(self)
        self.act_name = None

    def evaluate(self):
        act_name = self.get_socket_value(self.act_name)
        cont = logic.getCurrentController()
        if is_invalid(act_name):
            return
        if act_name not in cont.actuators:
            debug(f'Controller "{cont}" has no actuator "{act_name}"')
            return
        self._set_ready()
        self._set_value(logic.getCurrentController().actuators[act_name])


class GetActuatorValue(GEParameterNode):

    def __init__(self):
        GEParameterNode.__init__(self)
        self.actuator = None
        self.field = None

    def evaluate(self):
        actuator = self.get_socket_value(self.actuator)
        field = self.get_socket_value(self.field)
        if is_invalid(actuator, field):
            return
        self._set_ready()
        self._set_value(getattr(actuator, field))


class ActivateActuator(GEParameterNode):

    def __init__(self):
        GEParameterNode.__init__(self)
        self.condition = None
        self.actuator = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        actuator = str(self.get_socket_value(self.actuator))
        self._set_ready()
        if is_invalid(actuator):
            return
        controller = logic.getCurrentController()
        if actuator not in controller.actuators:
            debug(f'Controller "{controller}" has no actuator "{actuator}"')
            return
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            controller.deactivate(actuator)
            return
        controller.activate(actuator)
        self.done = True


class DeactivateActuator(GEParameterNode):

    def __init__(self):
        GEParameterNode.__init__(self)
        self.condition = None
        self.actuator = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        actuator = str(self.get_socket_value(self.actuator))
        if is_invalid(actuator):
            return
        controller = logic.getCurrentController()
        if actuator not in controller.actuators:
            return
        self._set_ready()
        controller.deactivate(actuator)
        self.done = True


class ActivateActuatorByName(GEParameterNode):

    def __init__(self):
        GEParameterNode.__init__(self)
        self.condition = None
        self.actuator = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        actuator = str(self.get_socket_value(self.actuator))
        if is_invalid(actuator):
            return
        controller = logic.getCurrentController()
        if actuator not in controller.actuators:
            debug(f'Controller "{controller}" has no actuator "{actuator}"')
            return
        condition = self.get_socket_value(self.condition)
        self._set_ready()
        if not_met(condition):
            controller.deactivate(actuator)
            return
        controller.activate(actuator)
        self.done = True


class DeactivateActuatorByName(GEParameterNode):

    def __init__(self):
        GEParameterNode.__init__(self)
        self.condition = None
        self.actuator = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        actuator = str(self.get_socket_value(self.actuator))
        if is_invalid(actuator):
            return
        condition = self.get_socket_value(self.condition)
        controller = logic.getCurrentController()
        if actuator not in controller.actuators:
            return
        self._set_ready()
        if not_met(condition):
            return
        controller.deactivate(actuator)
        self.done = True


class SetActuatorValue(GEParameterNode):

    def __init__(self):
        GEParameterNode.__init__(self)
        self.condition = None
        self.actuator = None
        self.field = None
        self.value = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        actuator = self.get_socket_value(self.actuator)
        if is_invalid(actuator):
            return
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        field = self.get_socket_value(self.field)
        value = self.get_socket_value(self.value)
        if is_waiting(field, value):
            return
        setattr(actuator, field, value)
        self.done = True


class GetController(GEParameterNode):

    @classmethod
    def cont(cls, controller):
        return controller

    @classmethod
    def obj(cls, obj_name):
        return obj_name

    def __init__(self):
        GEParameterNode.__init__(self)
        self.obj_name = None
        self.cont_name = None

    def evaluate(self):
        game_obj = self.get_socket_value(self.obj_name)
        if is_invalid(game_obj):
            debug('Get Controller Node: No Game Object selected!')
            return
        if is_invalid(self.cont_name):
            debug('Get Controller Node: No Controller selected!')
            return
        self._set_ready()
        self._set_value(game_obj.controllers[self.cont_name])


class GetCurrentControllerLB(GEParameterNode):

    def __init__(self):
        GEParameterNode.__init__(self)

    def evaluate(self):
        self._set_ready()
        self._set_value(logic.getCurrentController())


class GetSensor(GEParameterNode):

    @classmethod
    def sens(cls, sensor):
        return sensor

    @classmethod
    def obj(cls, obj_name):
        return obj_name

    def __init__(self):
        GEParameterNode.__init__(self)
        self.obj_name = None
        self.sens_name = None

    def evaluate(self):
        game_obj = self.get_socket_value(self.obj_name)
        if is_invalid(game_obj):
            debug('Get Sensor Node: No Game Object selected!')
            return
        if is_invalid(self.sens_name):
            debug('Get Sensor Node: No Sensor selected!')
            return
        self._set_ready()
        self._set_value(game_obj.sensors[self.sens_name].positive)


class GetSensorByName(GEParameterNode):

    def __init__(self):
        GEParameterNode.__init__(self)
        self.obj = None
        self.name = None

    def evaluate(self):
        obj = self.get_socket_value(self.obj)
        name = self.get_socket_value(self.name)
        if name in obj.sensors:
            self._set_ready()
            self._set_value(obj.sensors[name].positive)
        else:
            debug("{} has no Sensor named '{}'!".format(obj.name, name))
            return


class GetSensorValueByName(GEParameterNode):

    def __init__(self):
        GEParameterNode.__init__(self)
        self.obj = None
        self.name = None
        self.field = None

    def evaluate(self):
        obj = self.get_socket_value(self.obj)
        name = self.get_socket_value(self.name)
        field = self.get_socket_value(self.field)
        if name in obj.sensors:
            self._set_ready()
            self._set_value(getattr(obj.sensors[name], field))
        else:
            debug("{} has no Sensor named '{}'!".format(obj.name, name))


class SensorValue(GEParameterNode):

    @classmethod
    def sens(cls, sensor):
        return sensor

    @classmethod
    def obj(cls, obj_name):
        return obj_name

    def __init__(self):
        GEParameterNode.__init__(self)
        self.obj_name = None
        self.sens_name = None
        self.field = None
        self.val = None
        self.VAL = GEOutSocket(self, self.get_val)

    def get_val(self):
        return self.val

    def evaluate(self):
        game_obj = self.get_socket_value(self.obj_name)
        if is_invalid(game_obj):
            debug('Get Sensor Node: No Game Object selected!')
            return
        if is_invalid(self.sens_name):
            debug('Get Sensor Node: No Sensor selected!')
            return
        field = self.get_socket_value(self.field)
        if is_waiting(field):
            return
        self._set_ready()
        self.val = getattr(game_obj.sensors[self.sens_name], field)


class SensorPositive(GEParameterNode):

    def __init__(self):
        GEParameterNode.__init__(self)
        self.sensor = None
        self.done = None

    def evaluate(self):
        sens = self.get_socket_value(self.sensor)
        if is_invalid(sens):
            return
        self._set_ready()
        self._set_value(sens.positive)


class ParameterActiveCamera(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)

    def evaluate(self):
        scene = logic.getCurrentScene()
        self._set_ready()
        if is_invalid(scene):
            debug('Active Camera Node: Invalid Scene!')
            self._set_value(None)
        else:
            self._set_value(scene.active_camera)


class GetGravity(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.collection = None

    def evaluate(self):
        self._set_ready()
        self._set_value(bge.logic.getCurrentScene().gravity)


class GetCollection(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.collection = None

    def evaluate(self):
        collection = self.get_socket_value(self.collection)
        if is_invalid(collection):
            return
        self._set_ready()
        self._set_value(collection)


class GetCollectionObjects(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.collection = None

    def evaluate(self):
        collection = self.get_socket_value(self.collection)
        if is_invalid(collection):
            return
        self._set_ready()
        col = bpy.data.collections.get(collection)
        if not col:
            return
        objects = []
        for o in col.objects:
            objects.append(check_game_object(o.name))
        self._set_value(objects)


class GetCollectionObjectNames(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.condition = None
        self.collection = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        collection = self.get_socket_value(self.collection)
        if is_invalid(collection):
            return
        self._set_ready()
        col = bpy.data.collections.get(collection)
        if not col:
            return
        objects = []
        for o in col.objects:
            if not o.parent:
                objects.append(o.name)
        self._set_value(objects)


class GESetOverlayCollection(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.condition = None
        self.camera = None
        self.collection = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        collection = self.get_socket_value(self.collection)
        camera = self.get_socket_value(self.camera)
        if is_invalid(camera, collection):
            return
        self._set_ready()
        col = bpy.data.collections.get(collection)
        if not col:
            return
        logic.getCurrentScene().addOverlayCollection(camera, col)
        self._set_value(True)


class GERemoveOverlayCollection(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.collection = None

    def evaluate(self):
        collection = self.get_socket_value(self.collection)
        if is_invalid(collection):
            return
        self._set_ready()
        col = bpy.data.collections.get(collection)
        if not col:
            return
        logic.getCurrentScene().removeOverlayCollection(col)
        self._set_value(True)


class ParameterScreenPosition(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.game_object = None
        self.camera = None
        self.xposition = GEOutSocket(self, self._get_xposition)
        self.yposition = GEOutSocket(self, self._get_yposition)
        self._xpos = None
        self._ypos = None

    def _get_xposition(self):
        return self._xpos

    def _get_yposition(self):
        return self._ypos

    def evaluate(self):
        self._set_ready()
        game_object = self.get_socket_value(self.game_object)
        camera = self.get_socket_value(self.camera)
        if is_invalid(game_object) or is_invalid(camera):
            self._xpos = None
            self._ypos = None
            self._set_value(None)
            return
        position = camera.getScreenPosition(game_object)
        self._set_value(position)
        self._xpos = position[0]
        self._ypos = position[1]


class ParameterWorldPosition(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.camera = None
        self.screen_x = None
        self.screen_y = None
        self.world_z = None

    def evaluate(self):
        self._set_ready()
        camera = self.get_socket_value(self.camera)
        screen_x = self.get_socket_value(self.screen_x)
        screen_y = self.get_socket_value(self.screen_y)
        world_z = self.get_socket_value(self.world_z)
        if (
            is_invalid(camera) or
            (screen_x is None) or
            (screen_y is None) or
            (world_z is None)
        ):
            self._set_value(None)
        else:
            direction = camera.getScreenVect(screen_x, screen_y)
            origin = camera.worldPosition
            aim = direction * -world_z
            point = origin + (aim)
            self._set_value(point)


class GECursorBehavior(GEActionNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.condition = None
        self.cursor_object = None
        self.world_z = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        self._set_ready()
        camera = logic.getCurrentScene().active_camera
        condition = self.get_socket_value(self.condition)
        cursor_object = self.get_socket_value(self.cursor_object)
        world_z = self.get_socket_value(self.world_z)
        if is_invalid(cursor_object):
            return
        if not_met(condition):
            if cursor_object.visible:
                cursor_object.setVisible(False, True)
            return
        if not cursor_object.visible:
            cursor_object.setVisible(True, True)
        else:
            x = self.network._last_mouse_position[0]
            y = self.network._last_mouse_position[1]
            direction = camera.getScreenVect(x, y)
            origin = camera.worldPosition
            aim = direction * -world_z
            point = origin + aim
            cursor_object.worldOrientation = camera.worldOrientation
            cursor_object.worldPosition = point
        self.done = True


class ParameterPythonModuleFunction(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.condition = None
        self.module_name = None
        self.module_func = None
        self.arg = None
        self.val = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.VAL = GEOutSocket(self, self.get_val)
        self._old_mod_name = None
        self._old_mod_fun = None
        self._module = None
        self._modfun = None

    def get_done(self):
        return self.done

    def get_val(self):
        return self.val

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        mname = self.get_socket_value(self.module_name)
        mfun = self.get_socket_value(self.module_func)
        if is_waiting(mname, mfun):
            return
        arg = self.get_socket_value(self.arg)
        self._set_ready()
        if mname and (self._old_mod_name != mname):
            exec("import {}".format(mname))
            self._old_mod_name = mname
            self._module = eval(mname)
        if self._old_mod_fun != mfun:
            self._modfun = getattr(self._module, mfun)
            self._old_mod_fun = mfun
        if not isinstance(arg, Invalid):
            self.val = self._modfun(arg)
        else:
            self.val = self._modfun()
        self.done = True


class ParameterTime(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.network = None
        self.TIME_PER_FRAME = GEOutSocket(
            self,
            self.get_time_per_frame
        )
        self.FPS = GEOutSocket(self, self.get_fps)
        self.TIMELINE = GEOutSocket(self, self.get_timeline)

    def get_time_per_frame(self):
        return self.network.time_per_frame

    def get_fps(self):
        tpf = self.network.time_per_frame
        if not tpf:
            return 1
        fps = (1 / tpf)
        return fps

    def get_timeline(self):
        return self.network.timeline

    def setup(self, network):
        self.network = network

    def has_status(self, status):
        return status is STATUS_READY

    def evaluate(self):
        pass


class ParameterObjectAttribute(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.game_object = None
        self.attribute_name = None

    def evaluate(self):
        game_object = self.get_socket_value(self.game_object)
        attribute_name = self.get_socket_value(self.attribute_name)
        if is_waiting(game_object, attribute_name):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if not hasattr(game_object, attribute_name):
            debug(
                'Get Object Data Node: {} has no attribute {}!'
                .format(game_object, attribute_name)
            )
            return
        val = getattr(game_object, attribute_name)
        self._set_value(
            val.copy() if isinstance(val, Vector)
            else val
        )


class ClampValue(GEParameterNode):

    def __init__(self):
        GEParameterNode.__init__(self)
        self.value = None
        self.range = None

    def evaluate(self):
        value = self.get_socket_value(self.value)
        range_ft = self.get_socket_value(self.range)
        if is_waiting(range_ft):
            return
        if is_invalid(value):
            return
        self._set_ready()
        if range_ft.x == range_ft.y:
            self._set_value(value)
            return
        if value < range_ft.x:
            value = range_ft.x
        if value > range_ft.y:
            value = range_ft.y
        self._set_value(value)


class GetImage(GEParameterNode):

    def __init__(self):
        GEParameterNode.__init__(self)
        self.image = None

    def evaluate(self):
        image = self.get_socket_value(self.image)
        if is_invalid(image):
            return
        self._set_ready()
        self._set_value(bpy.data.images[image])


class GetSound(GEParameterNode):

    def __init__(self):
        GEParameterNode.__init__(self)
        self.sound = None

    def evaluate(self):
        sound = self.get_socket_value(self.sound)
        if is_invalid(sound):
            return
        self._set_ready()
        self._set_value(sound)


class InterpolateValue(GEParameterNode):

    def __init__(self):
        GEParameterNode.__init__(self)
        self.value_a = None
        self.value_b = None
        self.factor = None

    def evaluate(self):
        value_a = self.get_socket_value(self.value_a)
        value_b = self.get_socket_value(self.value_b)
        factor = self.get_socket_value(self.factor)
        if is_invalid(value_a, value_b, factor):
            return
        self._set_ready()
        self._set_value((factor * value_b) + ((1-factor) * value_a))


class ParameterArithmeticOp(GEParameterNode):

    @classmethod
    def op_by_code(cls, str):
        import operator
        opmap = {
            "ADD": operator.add,
            "SUB": operator.sub,
            "DIV": operator.truediv,
            "MUL": operator.mul
        }
        return opmap.get(str)

    def __init__(self):
        GEParameterNode.__init__(self)
        self.operand_a = None
        self.operand_b = None
        self.operator = None

    def get_vec_calc(self, vec, num):
        if len(vec) == 4:
            return Vector(
                (
                    self.operator(vec.x, num),
                    self.operator(vec.y, num),
                    self.operator(vec.z, num),
                    self.operator(vec.w, num)
                )
            )
        else:
            return Vector(
                (
                    self.operator(vec.x, num),
                    self.operator(vec.y, num),
                    self.operator(vec.z, num)
                )
            )

    def get_vec_vec_calc(self, vec, vec2):
        if len(vec) == 4 and len(vec2) == 4:
            return Vector(
                (
                    self.operator(vec.x, vec2.x),
                    self.operator(vec.y, vec2.y),
                    self.operator(vec.z, vec2.z),
                    self.operator(vec.w, vec2.w)
                )
            )
        else:
            return Vector(
                (
                    self.operator(vec.x, vec2.x),
                    self.operator(vec.y, vec2.y),
                    self.operator(vec.z, vec2.z)
                )
            )

    def evaluate(self):
        a = self.get_socket_value(self.operand_a)
        b = self.get_socket_value(self.operand_b)
        if is_invalid(a, b):
            return
        self._set_ready()
        if (a is None) or (b is None):
            self._set_value(None)
        else:
            if (
                isinstance(a, Vector) and
                isinstance(b, Vector)
            ):
                self._set_value(self.get_vec_vec_calc(a, b))
                return
            elif isinstance(a, Vector):
                self._set_value(self.get_vec_calc(a, b))
                return
            elif isinstance(b, Vector):
                debug('Math Node: Only Second Argument is Vector! \
                    Either both or only first can be Vector!')
                return
            self._set_value(self.operator(a, b))


class Threshold(GEParameterNode):

    @classmethod
    def op_by_code(cls, op):
        return op

    def __init__(self):
        GEParameterNode.__init__(self)
        self.value = None
        self.else_z = None
        self.threshold = None
        self.operator = None

    def calc_threshold(self, op, v, t, e):
        if op == 'GREATER':
            return v if v > t else (0 if e else t)
        if op == 'LESS':
            return v if v < t else (0 if e else t)

    def evaluate(self):
        v = self.get_socket_value(self.value)
        e = self.get_socket_value(self.else_z)
        t = self.get_socket_value(self.threshold)
        if is_waiting(v, t):
            return
        value = self.calc_threshold(self.operator, v, t, e)
        self._set_ready()
        if (v is None) or (t is None):
            self._set_value(None)
        else:
            self._set_value(value)


class RangedThreshold(GEParameterNode):

    @classmethod
    def op_by_code(cls, op):
        return op

    def __init__(self):
        GEParameterNode.__init__(self)
        self.value = None
        self.threshold = None
        self.operator = None

    def calc_threshold(self, op, v, t):
        if op == 'OUTSIDE':
            return v if (v < t.x or v > t.y) else 0
        if op == 'INSIDE':
            return v if (t.x < v < t.y) else 0

    def evaluate(self):
        v = self.get_socket_value(self.value)
        t = self.get_socket_value(self.threshold)
        if is_waiting(v, t):
            return
        value = self.calc_threshold(self.operator, v, t)
        self._set_ready()
        if (v is None) or (t is None):
            self._set_value(None)
        else:
            self._set_value(value)


class GELimitRange(GEParameterNode):

    @classmethod
    def op_by_code(cls, op):
        return op

    def __init__(self):
        GEParameterNode.__init__(self)
        self.value = None
        self.threshold = Vector((0, 0))
        self.operator = None
        self.last_val = 0

    def calc_threshold(self, op, v, t):
        l = self.last_val
        if op == 'OUTSIDE':
            if (v < t.x or v > t.y):
                self.last_val = v
            else:
                self.last_val = t.x if l <= t.x else t.y
        if op == 'INSIDE':
            if (t.x < v < t.y):
                self.last_val = v
            else:
                self.last_val = t.x if v <= t.x else t.y

    def evaluate(self):
        v = self.get_socket_value(self.value)
        t = self.get_socket_value(self.threshold)
        if is_waiting(v, t):
            return
        self.calc_threshold(self.operator, v, t)
        self._set_ready()
        if (v is None) or (t is None):
            self._set_value(None)
        else:
            self._set_value(self.last_val)


class WithinRange(GEParameterNode):

    @classmethod
    def op_by_code(cls, op):
        return op

    def __init__(self):
        GEParameterNode.__init__(self)
        self.value = None
        self.range = None
        self.operator = None

    def calc_range(self, op, v, r):
        if op == 'OUTSIDE':
            return True if (v < r.x or v > r.y) else False
        if op == 'INSIDE':
            return True if (r.x < v < r.y) else False

    def evaluate(self):
        v = self.get_socket_value(self.value)
        r = self.get_socket_value(self.range)
        if is_waiting(v, r):
            return
        value = self.calc_range(self.operator, v, r)
        self._set_ready()
        if (v is None) or (r is None):
            self._set_value(None)
        else:
            self._set_value(value)


class GetObInstanceAttr(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.instance = None
        self.attr = None

    def evaluate(self):
        instance = self.get_socket_value(self.instance)
        attr = self.get_socket_value(self.attr)
        if is_waiting(instance, attr):
            return
        if not hasattr(instance, attr):
            debug(
                'Get Object Attribute Node: Object has no attr "{}"'.format(
                    attr
                )
            )
            self._set_ready()
            self._set_value(None)
            return
        self._set_ready()
        self._set_value(getattr(instance, attr))


class GetScene(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)

    def evaluate(self):
        self._set_ready()
        self._set_value(logic.getCurrentScene())


class GetTimeScale(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)

    def evaluate(self):
        self._set_ready()
        self._set_value(logic.getTimeScale())


class SetObInstanceAttr(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.condition = None
        self.instance = None
        self.attr = None
        self.value = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        instance = self.get_socket_value(self.instance)
        attr = self.get_socket_value(self.attr)
        value = self.get_socket_value(self.value)
        if is_waiting(instance, attr, value):
            return
        self._set_ready()
        setattr(instance, attr, value)


class NormalizeVector(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.vector = None

    def evaluate(self):
        vector = self.get_socket_value(self.vector)
        if is_waiting(vector):
            return
        self._set_ready()
        self._set_value(vector.normalize())


class ParameterActionStatus(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.game_object = None
        self.action_layer = None
        self._action_name = ""
        self._action_frame = 0.0
        self.NOT_PLAYING = GEOutSocket(self, self.get_not_playing)
        self.ACTION_NAME = GEOutSocket(self, self.get_action_name)
        self.ACTION_FRAME = GEOutSocket(self, self.get_action_frame)

    def get_action_name(self):
        return self._action_name

    def get_action_frame(self):
        return self._action_frame

    def get_not_playing(self):
        return not self.get_value()

    def evaluate(self):
        game_object = self.get_socket_value(self.game_object)
        action_layer = self.get_socket_value(self.action_layer)
        if is_waiting(game_object, action_layer):
            return
        self._set_ready()
        if is_invalid(game_object):
            self._action_name = ""
            self._action_frame = 0.0
            self._set_value(False)
        else:
            self._set_value(game_object.isPlayingAction(action_layer))
            self._action_name = game_object.getActionName(action_layer)
            self._action_frame = game_object.getActionFrame(action_layer)


class ParameterSimpleValue(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.value = None

    def evaluate(self):
        value = self.get_socket_value(self.value)
        self._set_ready()
        self._set_value(value)


class ParameterTypeCast(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.value = None
        self.to_type = None

    def typecast_value(self, value, t):
        if t == 'int':
            return int(value)
        elif t == 'bool':
            return bool(value)
        elif t == 'str':
            return str(value)
        elif t == 'float':
            return float(value)
        return value

    def evaluate(self):
        value = self.get_socket_value(self.value)
        to_type = self.get_socket_value(self.to_type)
        if is_waiting(to_type, value):
            return
        self._set_ready()
        self._set_value(self.typecast_value(value, to_type))


class ParameterVectorMath(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.op = None
        self.vector = None
        self.vector_2 = None
        self.factor = None

    def calc_output_vector(self, op, vec, vec2, fac):
        matvec = vec.copy()
        if op == 'normalize':
            matvec.normalize()
        elif op == 'lerp':
            return matvec.lerp(vec2, fac)
        elif op == 'negate':
            matvec.negate()
        elif op == 'dot':
            return matvec.dot(vec2)
        elif op == 'cross':
            return matvec.cross(vec2)
        elif op == 'project':
            return matvec.project(vec2)
        return matvec

    def evaluate(self):
        op = self.get_socket_value(self.op)
        vector = self.get_socket_value(self.vector)
        vector_2 = self.get_socket_value(self.vector_2)
        factor = self.get_socket_value(self.factor)
        if is_waiting(
            op,
            factor
        ):
            return
        if is_invalid(
            vector,
            vector_2
        ):
            return
        self._set_ready()
        self._set_value(self.calc_output_vector(op, vector, vector_2, factor))


class VectorAngle(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.op = None
        self.vector: Vector = None
        self.vector_2: Vector = None

    def evaluate(self):
        vector: Vector = self.get_socket_value(self.vector)
        vector_2: Vector = self.get_socket_value(self.vector_2)
        if is_invalid(
            vector,
            vector_2
        ):
            return
        self._set_ready()
        rad: float = math.acos(vector.dot(vector_2))
        deg: float = rad * 180/math.pi
        self._set_value(deg)


class VectorAngleCheck(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.op: str = None
        self.vector: Vector = None
        self.vector_2: Vector = None
        self.value = None
        self._angle = 0
        self.ANGLE = GEOutSocket(self, self.get_angle)

    def get_angle(self):
        return self._angle

    def evaluate(self):
        op: str = self.get_socket_value(self.op)
        vector: Vector = self.get_socket_value(self.vector)
        vector_2: Vector = self.get_socket_value(self.vector_2)
        value: float = self.get_socket_value(self.value)
        if is_waiting(
            op
        ):
            return
        if is_invalid(
            vector,
            vector_2
        ):
            return
        self._set_ready()
        rad: float = math.acos(vector.dot(vector_2))
        deg: float = rad * 180/math.pi
        self._angle = deg
        self._set_value(LOGIC_OPERATORS[int(op)](deg, value))



class ParameterVector(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.input_vector = None
        self.input_x = None
        self.input_y = None
        self.input_z = None
        self.output_vector = Vector()
        self.OUTX = GEOutSocket(self, self.get_out_x)
        self.OUTY = GEOutSocket(self, self.get_out_y)
        self.OUTZ = GEOutSocket(self, self.get_out_z)
        self.OUTV = GEOutSocket(self, self.get_out_v)
        self.NORMVEC = GEOutSocket(self, self.get_normalized_vector)

    def get_out_x(self): return self.output_vector.x
    def get_out_y(self): return self.output_vector.y
    def get_out_z(self): return self.output_vector.z
    def get_out_v(self): return self.output_vector.copy()
    def get_normalized_vector(self): return self.output_vector.normalized()

    def evaluate(self):
        self._set_ready()
        x = self.get_socket_value(self.input_x)
        y = self.get_socket_value(self.input_y)
        z = self.get_socket_value(self.input_z)
        v = self.get_socket_value(self.input_vector)
        # TODO: zero vector if v is None?
        if not is_invalid(v):
            self.output_vector[:] = v
        if not is_invalid(x):
            self.output_vector.x = x
        if not is_invalid(y):
            self.output_vector.y = y
        if not is_invalid(z):
            self.output_vector.z = z
        self._set_value(self.output_vector)


class ParameterVector2Simple(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.input_x = None
        self.input_y = None
        self.output_vector = Vector()
        self.OUTV = GEOutSocket(self, self.get_out_v)

    def get_out_v(self): return self.output_vector.copy()
    def get_normalized_vector(self): return self.output_vector.normalized()

    def evaluate(self):
        self._set_ready()
        x = self.get_socket_value(self.input_x)
        y = self.get_socket_value(self.input_y)
        if not is_invalid(x):
            self.output_vector.x = x
        if not is_invalid(y):
            self.output_vector.y = y
        self._set_value(self.output_vector)


class ParameterVector2Split(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.input_v = None
        self.output_v = Vector()
        self.OUTX = GEOutSocket(self, self.get_out_x)
        self.OUTY = GEOutSocket(self, self.get_out_y)

    def get_out_x(self): return self.output_v.x
    def get_out_y(self): return self.output_v.y

    def evaluate(self):
        self._set_ready()
        vec = self.get_socket_value(self.input_v)
        if vec is not None:
            self.output_v = vec
        self._set_value(vec)


class ParameterVector3Split(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.input_v = None
        self.output_v = Vector()
        self.OUTX = GEOutSocket(self, self.get_out_x)
        self.OUTY = GEOutSocket(self, self.get_out_y)
        self.OUTZ = GEOutSocket(self, self.get_out_z)

    def get_out_x(self): return self.output_v.x
    def get_out_y(self): return self.output_v.y
    def get_out_z(self): return self.output_v.z

    def evaluate(self):
        self._set_ready()
        vec = self.get_socket_value(self.input_v)
        if vec is not None:
            self.output_v = vec
        self._set_value(vec)


class ParameterAbsVector3(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.input_v = None
        self.output_v = Vector()
        self.OUTV = GEOutSocket(self, self.get_out_v)

    def get_out_v(self): return self.output_v

    def evaluate(self):
        self._set_ready()
        vec = self.get_socket_value(self.input_v)
        vec.x = abs(vec.x)
        vec.y = abs(vec.y)
        vec.z = abs(vec.z)
        if vec is not None:
            self.output_v = vec
        self._set_value(vec)


class ParameterEulerToMatrix(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.input_e = None
        self.matrix = Matrix()
        self.OUT = GEOutSocket(self, self.get_matrix)

    def get_matrix(self):
        return self.matrix

    def evaluate(self):
        self._set_ready()
        vec = self.get_socket_value(self.input_e)
        if isinstance(vec, Vector):
            vec = Euler((vec.x, vec.y, vec.z), 'XYZ')
        self.matrix = vec.to_matrix()


class ParameterMatrixToEuler(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.input_m = None
        self.euler = Euler()
        self.OUT = GEOutSocket(self, self.get_euler)

    def get_euler(self):
        return self.euler

    def evaluate(self):
        self._set_ready()
        matrix = self.get_socket_value(self.input_m)
        self.euler = matrix.to_euler()


class ParameterMatrixToVector(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.input_m = None
        self.vec = Vector()
        self.OUT = GEOutSocket(self, self.get_vec)

    def get_vec(self):
        return self.vec

    def evaluate(self):
        self._set_ready()
        matrix = self.get_socket_value(self.input_m)
        if is_waiting(matrix):
            return
        e = matrix.to_euler()
        self.vec = Vector((e.x, e.y, e.z))


class ParameterVector3Simple(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.input_x = None
        self.input_y = None
        self.input_z = None
        self.output_vector = Vector()
        self.OUTV = GEOutSocket(self, self.get_out_v)

    def get_out_v(self):
        return self.output_vector.copy()

    def get_normalized_vector(self):
        return self.output_vector.normalized()

    def evaluate(self):
        self._set_ready()
        x = self.get_socket_value(self.input_x)
        y = self.get_socket_value(self.input_y)
        z = self.get_socket_value(self.input_z)
        if is_invalid(x):
            return
        if is_waiting(x, y, z):
            return
        self.output_vector.x = x
        self.output_vector.y = y
        self.output_vector.z = z
        self._set_value(self.output_vector)


class ParameterVector4Simple(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.input_x = None
        self.input_y = None
        self.input_z = None
        self.input_w = None
        self.output_vector = Vector((0, 0, 0, 0))
        self.OUTV = GEOutSocket(self, self.get_out_v)

    def get_out_v(self):
        return self.output_vector.copy()

    def evaluate(self):
        self._set_ready()
        x = self.get_socket_value(self.input_x)
        y = self.get_socket_value(self.input_y)
        z = self.get_socket_value(self.input_z)
        w = self.get_socket_value(self.input_w)
        if is_invalid(x, y, z, w):
            return
        self.output_vector.x = x
        self.output_vector.y = y
        self.output_vector.z = z
        self.output_vector.w = w
        self._set_value(self.output_vector)


class ParameterColor(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.color = None
        self.output_vector = None
        self.OUTV = GEOutSocket(self, self.get_out_v)

    def get_out_v(self):
        return self.output_vector.copy()

    def get_normalized_vector(self):
        return self.output_vector.normalized()

    def evaluate(self):
        self._set_ready()
        c = self.get_socket_value(self.color)
        if is_waiting(c):
            return
        self.output_vector = c


class ParameterColorAlpha(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.color = None
        self.output_vector = None
        self.OUTV = GEOutSocket(self, self.get_out_v)

    def get_out_v(self):
        return self.output_vector.copy()

    def get_normalized_vector(self):
        return self.output_vector.normalized()

    def evaluate(self):
        self._set_ready()
        c = self.get_socket_value(self.color)
        if is_waiting(c):
            return
        self.output_vector = c


class ParameterEulerSimple(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.input_x = None
        self.input_y = None
        self.input_z = None
        self.output_euler = Euler()
        self.OUTV = GEOutSocket(self, self.get_out_v)

    def get_out_x(self): return self.output_euler.x
    def get_out_y(self): return self.output_euler.y
    def get_out_z(self): return self.output_euler.z
    def get_out_v(self): return self.output_euler.copy()
    def get_normalized_vector(self): return self.output_euler.normalized()

    def evaluate(self):
        self._set_ready()
        x = self.get_socket_value(self.input_x)
        y = self.get_socket_value(self.input_y)
        z = self.get_socket_value(self.input_z)
        if x is not None:
            self.output_euler.x = x
        if y is not None:
            self.output_euler.y = y
        if z is not None:
            self.output_euler.z = z
        self._set_value(self.output_euler)


class ParameterVector4(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.in_x = None
        self.in_y = None
        self.in_z = None
        self.in_w = None
        self.in_vec = None
        self.out_x = 0
        self.out_y = 0
        self.out_z = 0
        self.out_w = 1
        self.out_vec = Vector((0, 0, 0, 1))
        self.OUTX = GEOutSocket(self, self._get_out_x)
        self.OUTY = GEOutSocket(self, self._get_out_y)
        self.OUTZ = GEOutSocket(self, self._get_out_z)
        self.OUTW = GEOutSocket(self, self._get_out_w)
        self.OUTVEC = GEOutSocket(self, self._get_out_vec)

    def _get_out_x(self):
        return self.out_x

    def _get_out_y(self):
        return self.out_y

    def _get_out_z(self):
        return self.out_z

    def _get_out_w(self):
        return self.out_w

    def _get_out_vec(self):
        return self.out_vec.copy()

    def get_socket_value(self, param, default_value):
        if param is None:
            return default_value
        elif hasattr(param, "get_value"):
            value = param.get_value()
            if is_waiting(value):
                raise "Unexpected error in tree"
            else:
                return value
        else:
            return param

    def evaluate(self):
        self._set_ready()
        x = self.get_socket_value(self.in_x, None)
        y = self.get_socket_value(self.in_y, None)
        z = self.get_socket_value(self.in_z, None)
        w = self.get_socket_value(self.in_w, None)
        vec = self.get_socket_value(self.in_vec, None)
        if(vec is not None):
            # out is vec with vec components replaced by non null x,y,z,w
            self.out_x = vec.x if x is None else x
            self.out_y = vec.y if y is None else y
            self.out_z = vec.z if z is None else z
            self.out_w = 1
            if(len(vec) >= 4):
                self.out_w = vec.w if w is None else w
            elif(w is not None):
                self.out_w = w
            self.out_vec[:] = (self.out_x, self.out_y, self.out_z, self.out_w)
        else:
            # in vec is None
            self.out_x = 0 if x is None else x
            self.out_y = 0 if y is None else y
            self.out_z = 0 if z is None else z
            self.out_w = 1 if w is None else w
            self.out_vec[:] = (self.out_x, self.out_y, self.out_z, self.out_w)


class ParameterFindChildByName(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.from_parent = None
        self.child = None
        self.CHILD = GEOutSocket(self, self.get_child)

    def get_child(self):
        parent = self.get_socket_value(self.from_parent)
        childName = self.get_socket_value(self.child)
        return(parent.childrenRecursive.get(childName))

    def evaluate(self):
        self._set_ready()
        self._set_value(None)

        parent = self.get_socket_value(self.from_parent)
        child = self.get_socket_value(self.child)

        if (child is None) or (child == ""):
            return

        if is_waiting(parent, child):
            return
        elif not is_invalid(parent):
            # find from parent
            self._set_value(_name_query(parent.childrenRecursive, child))
            # return


class FindChildByIndex(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.from_parent: GameObject = None
        self.index: int = None

    def evaluate(self):
        self._set_ready()
        self._set_value(None)

        parent: GameObject = self.get_socket_value(self.from_parent)
        index: int = self.get_socket_value(self.index)

        if is_waiting(parent, index):
            return
        elif not is_invalid(parent):
            # find from parent
            if len(parent.children) > index:
                self._set_value(parent.children[index])
            else:
                self._set_value(False)
            # return

# Condition cells
class ConditionAlways(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.repeat = False
        self._set_status(STATUS_READY)
        self._value = True

    def reset(self):
        if not self.repeat:
            self._value = False

    def evaluate(self):
        pass


class ObjectPropertyOperator(GEConditionNode):
    def __init__(self, operator='EQUAL'):
        GEActionNode.__init__(self)
        self.game_object = None
        self.property_name = None
        self.operator = operator
        self.compare_value = None
        self.val = 0
        self.VAL = GEOutSocket(self, self.get_val)

    def get_val(self):
        return self.val

    def evaluate(self):
        game_object = self.get_socket_value(self.game_object)
        property_name = self.get_socket_value(self.property_name)
        compare_value = self.get_socket_value(self.compare_value)
        operator = self.get_socket_value(self.operator)
        if is_waiting(property_name, compare_value):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        value = self.val = game_object[property_name]
        if operator > 1:  # eq and neq are valid for None
            if is_invalid(value, compare_value):
                return
        if operator is None:
            return
        self._set_value(LOGIC_OPERATORS[operator](value, compare_value))


class ConditionNot(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.condition = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if is_waiting(condition):
            return
        self._set_ready()
        self._set_value(not condition)


class ConditionLNStatus(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.game_object = None
        self.tree_name = None
        self._running = False
        self._stopped = False
        self.IFRUNNING = GEOutSocket(self, self.get_running)
        self.IFSTOPPED = GEOutSocket(self, self.get_stopped)

    def get_running(self):
        return self._running

    def get_stopped(self):
        return self._stopped

    def evaluate(self):
        game_object = self.get_socket_value(self.game_object)
        tree_name = self.get_socket_value(self.tree_name)
        if is_waiting(game_object, tree_name):
            return
        self._set_ready()
        self._running = False
        self._stopped = False
        if is_invalid(game_object):
            return
        tree = game_object.get(f'IGNLTree_{tree_name}')
        if tree is None:
            return
        self._running = tree.is_running()
        self._stopped = tree.is_stopped()


class ConditionLogicOp(GEConditionNode):
    def __init__(self, operator='GREATER'):
        GEConditionNode.__init__(self)
        self.operator = operator
        self.param_a = None
        self.param_b = None
        self.threshold = None

    def evaluate(self):
        a = self.get_socket_value(self.param_a)
        b = self.get_socket_value(self.param_b)
        threshold = self.get_socket_value(self.threshold)
        operator = self.get_socket_value(self.operator)
        if is_waiting(a, b, threshold):
            return
        self._set_ready()
        if operator > 1:  # eq and neq are valid for None
            if a is None:
                return
            if b is None:
                return
        if threshold is None:
            threshold = 0
        if threshold > 0 and abs(a - b) < threshold:
            a = b
        if operator is None:
            return
        self._set_value(LOGIC_OPERATORS[operator](a, b))


class ConditionCompareVecs(GEConditionNode):
    def __init__(self, operator='GREATER'):
        GEConditionNode.__init__(self)
        self.operator = operator
        self.all = None
        self.threshold = None
        self.param_a = None
        self.param_b = None

    def get_vec_val(self, op, a, b, xyz, threshold):
        for ax in ['x', 'y', 'z']:
            av = getattr(a, ax)
            bv = getattr(b, ax)
            av = bv if abs(av - bv) < threshold else av
            if xyz[ax] and not LOGIC_OPERATORS[op](av, bv):
                return False
        return True

    def evaluate(self):
        a = self.get_socket_value(self.param_a)
        b = self.get_socket_value(self.param_b)
        all_values = self.get_socket_value(self.all)
        operator = self.get_socket_value(self.operator)
        threshold = self.get_socket_value(self.threshold)
        if is_waiting(a, b, all_values, operator, threshold):
            return
        if (
            not isinstance(a, Vector)
            or not isinstance(b, Vector)
        ):
            return
        self._set_ready()
        if operator > 1:  # eq and neq are valid for None
            if a is None:
                return
            if b is None:
                return
        if operator is None:
            return
        self._set_value(
            self.get_vec_val(
                operator,
                a,
                b,
                all_values,
                threshold
            )
        )


class ConditionDistanceCheck(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.param_a = None
        self.param_b = None
        self.operator = None
        self.dist = None
        self.hyst = None
        self._check = self._strict_check

    def _strict_check(self, opindex, value, hyst, threshold):
        v = LOGIC_OPERATORS[opindex](value, threshold)
        if v is True:
            self._set_value(True)
        else:
            self._set_value(False)
            self._check = self._hyst_check

    def _hyst_check(self, opindex, value, hyst, threshold):
        if (opindex == 2) or (opindex == 4):
            v = LOGIC_OPERATORS[opindex](value, threshold + hyst)
            if v is True:
                self._set_value(True)
                self._check = self._strict_check
            else:
                self._set_value(False)
        elif (opindex == 3) or (opindex == 5):
            v = LOGIC_OPERATORS[opindex](value, threshold - hyst)
            if v is True:
                self._set_value(True)
                self._check = self._strict_check
            else:
                self._set_value(False)

    def evaluate(self):
        a = self.get_socket_value(self.param_a)
        b = self.get_socket_value(self.param_b)
        op = self.get_socket_value(self.operator)
        dist = self.get_socket_value(self.dist)
        hyst = self.get_socket_value(self.hyst)
        if is_waiting(a, b, op, dist, hyst):
            return
        self._set_ready()
        if is_invalid(a):
            return
        if is_invalid(b):
            return
        if op is None:
            return
        if dist is None:
            return
        distance = compute_distance(a, b)
        if distance is None:
            return self._set_value(False)
        if hyst is None:  # plain check, no threshold
            v = LOGIC_OPERATORS[op](distance, dist)
            self._set_value(v)
        else:  # check with hysteresys value, if >, >=, <, <=
            self._check(op, distance, hyst, dist)


class ConditionAnd(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.condition_a = None
        self.condition_b = None

    def evaluate(self):
        ca = self.get_socket_value(self.condition_a)
        cb = self.get_socket_value(self.condition_b)
        self._set_ready()
        if is_waiting(ca, cb):
            self._set_value(False)
            return
        self._set_value(ca and cb)
    pass


class ConditionAndNot(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.condition_a = None
        self.condition_b = None

    def evaluate(self):
        ca = self.get_socket_value(self.condition_a)
        cb = not self.get_socket_value(self.condition_b)
        self._set_ready()
        if is_waiting(ca, cb):
            self._set_value(False)
            return
        self._set_value(ca and cb)
    pass


class ConditionNotNone(GEConditionNode):

    def __init__(self):
        GEConditionNode.__init__(self)
        self.checked_value = None

    def evaluate(self):
        value = self.get_socket_value(self.checked_value)
        self._set_ready()
        self._set_value(value is not None)


class ConditionNone(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.checked_value = None

    def evaluate(self):
        self._set_ready()
        value = self.get_socket_value(self.checked_value)
        self._set_value(value is None)


class ConditionValueValid(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.checked_value = None

    def evaluate(self):
        self._set_ready()
        value = self.get_socket_value(self.checked_value)
        self._set_value(not is_invalid(value))


class ConditionOr(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.condition_a = True
        self.condition_b = True

    def evaluate(self):
        ca = self.get_socket_value(self.condition_a)
        cb = self.get_socket_value(self.condition_b)
        if is_waiting(ca):
            ca = False
        if is_waiting(cb):
            cb = False
        self._set_ready()
        self._set_value(ca or cb)


class ConditionOrList(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.ca = False
        self.cb = False
        self.cc = False
        self.cd = False
        self.ce = False
        self.cf = False

    def evaluate(self):
        ca = self.get_socket_value(self.ca)
        cb = self.get_socket_value(self.cb)
        cc = self.get_socket_value(self.cc)
        cd = self.get_socket_value(self.cd)
        ce = self.get_socket_value(self.ce)
        cf = self.get_socket_value(self.cf)
        if is_waiting(ca, cb, cc, cd, ce, cf):
            c = False
        self._set_ready()
        self._set_value(ca or cb or cc or cd or ce or cf)


class ConditionAndList(GEConditionNode):

    def __init__(self):
        GEConditionNode.__init__(self)
        self.ca = True
        self.cb = True
        self.cc = True
        self.cd = True
        self.ce = True
        self.cf = True

    def evaluate(self):
        ca = self.get_socket_value(self.ca)
        cb = self.get_socket_value(self.cb)
        cc = self.get_socket_value(self.cc)
        cd = self.get_socket_value(self.cd)
        ce = self.get_socket_value(self.ce)
        cf = self.get_socket_value(self.cf)
        self._set_ready()
        if is_waiting(ca, cb, cc, cd, ce, cf):
            self._set_value(False)
            return
        self._set_value(ca and cb and cc and cd and ce and cf)


class ActionKeyLogger(GEActionNode):
    def __init__(self, pulse=False):
        GEActionNode.__init__(self)
        self.condition = None
        self.pulse = pulse
        self._key_logged = None
        self._key_code = None
        self._character = None
        self.KEY_LOGGED = GEOutSocket(self, self.get_key_logged)
        self.KEY_CODE = GEOutSocket(self, self.get_key_code)
        self.CHARACTER = GEOutSocket(self, self.get_character)

    def get_key_logged(self):
        return self._key_logged

    def get_key_code(self):
        return self._key_code

    def get_character(self):
        return self._character

    def reset(self):
        GELogicContainer.reset(self)
        self._key_logged = False
        self._key_code = None
        self._character = None

    def evaluate(self):
        self._set_ready()
        condition = self.get_socket_value(self.condition)
        if not condition:
            return
        network = self.network
        keyboard_status = network.keyboard_events
        left_shift_status = keyboard_status[bge.events.LEFTSHIFTKEY].active
        right_shift_status = keyboard_status[bge.events.RIGHTSHIFTKEY].active
        shift_down = (
            left_shift_status or
            right_shift_status or
            network.capslock_pressed
        )
        active_events = network.active_keyboard_events
        active = (
            'active' if self.pulse
            else 'activated'
        )
        for keycode in active_events:
            event = active_events[keycode]
            if getattr(event, active):
                # something has been pressed
                self._character = bge.events.EventToCharacter(
                    event.type,
                    shift_down
                )
                self._key_code = keycode
                self._key_logged = True


class ConditionTimeElapsed(GEConditionNode):

    def __init__(self):
        GEConditionNode.__init__(self)
        self.condition = None
        self.delta_time = None
        self._trigger = 0
        self.network = None

    def setup(self, network):
        self.network = network

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        delta_time = self.get_socket_value(self.delta_time)
        if is_waiting(delta_time):
            return
        self._set_ready()
        now = self.network.timeline

        if not not_met(condition):
            self._trigger = now + delta_time

        if now >= self._trigger:
            self._set_value(True)
        else:
            self._set_value(False)


class ConditionKeyReleased(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.pulse = False
        self.key_code = None
        self.network = None

    def setup(self, network):
        self.network = network

    def evaluate(self):
        keycode = self.get_socket_value(self.key_code)
        if is_waiting(keycode):
            return
        self._set_ready()
        keystat = self.network.keyboard_events[keycode]
        if self.pulse:
            self._set_value(
                keystat.released or
                keystat.inactive
            )
        else:
            self._set_value(keystat.released)
    pass


class ConditionMouseLeft(GEConditionNode):
    def __init__(self, repeat=None):
        GEConditionNode.__init__(self)
        self.network = None
        self.repeat = repeat
        self._consumed = False

    def setup(self, network):
        self.network = network

    def reset(self):
        if self._consumed:
            self._set_value(False)
            self._set_status(STATUS_READY)
        else:
            GEConditionNode.reset(self)

    def evaluate(self):
        repeat = self.get_socket_value(self.repeat)
        if is_waiting(repeat):
            return
        self._set_ready()
        dx = self.network.mouse_motion_delta[0]
        self._set_value(dx > 0)
        if not self.repeat:
            self._consumed = True


class ConditionMouseRight(GEConditionNode):
    def __init__(self, repeat=None):
        GEConditionNode.__init__(self)
        self.network = None
        self.repeat = repeat
        self._consumed = False

    def setup(self, network):
        self.network = network

    def reset(self):
        if self._consumed:
            self._set_value(False)
            self._set_status(STATUS_READY)
        else:
            GEConditionNode.reset(self)

    def evaluate(self):
        repeat = self.get_socket_value(self.repeat)
        if is_waiting(repeat):
            return
        self._set_ready()
        dx = self.network.mouse_motion_delta[0]
        self._set_value(dx < 0)
        if not self.repeat:
            self._consumed = True


class ActionRepeater(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.input_value = None
        self.output_cells = []
        self.output_value = None

    def setup(self, network):
        super(GEActionNode, self).setup(network)
        for cell in self.output_cells:
            cell.setup(network)

    def evaluate(self):
        self._set_ready()
        condition = self.get_socket_value(self.condition)
        if not condition:
            return
        input_value = self.get_socket_value(self.input_value)
        if isinstance(input_value, numbers.Number):
            for e in range(0, input_value):
                self._set_value(e)
                for cell in self.output_cells:
                    cell.evaluate()
        else:
            for e in input_value:
                self._set_value(e)
                for cell in self.output_cells:
                    cell.evaluate()
                pass
            pass
        for cell in self.output_cells:
            cell.reset()
            pass
        pass
    pass


class ConditionCollision(GEConditionNode):
    def __init__(self):
        GEConditionNode.__init__(self)
        self.game_object = None
        self.use_mat = None
        self.prop = None
        self.material = None
        self._set_value("False")
        self.pulse = False
        self._target = None
        self._point = None
        self._normal = None
        self._collision_triggered = False
        self._consumed = False
        self._last_monitored_object = None
        self._objects = []
        self.TARGET = GEOutSocket(self, self.get_target)
        self.POINT = GEOutSocket(self, self.get_point)
        self.NORMAL = GEOutSocket(self, self.get_normal)
        self.OBJECTS = GEOutSocket(self, self.get_objects)

    def get_point(self):
        return self._point

    def get_normal(self):
        return self._normal

    def get_target(self):
        return self._target

    def get_objects(self):
        return self._objects

    def _collision_callback(self, obj, point, normal):
        self._objects.append(obj)
        use_mat = self.get_socket_value(self.use_mat)
        if use_mat:
            material = self.get_socket_value(self.material)
            if material:
                for obj in self._objects:
                    bo = obj.blenderObject
                    if material not in [slot.material.name for slot in bo.material_slots]:
                        self._objects.remove(obj)
                    else:
                        self._collision_triggered = True
                        self._target = obj
                        self._point = point
                        self._normal = normal
                        return
                self._collision_triggered = False
                return
        else:
            prop = self.get_socket_value(self.prop)
            if prop:
                for obj in self._objects:
                    if prop not in obj:
                        self._objects.remove(obj)
                    else:
                        self._collision_triggered = True
                        self._target = obj
                        self._point = point
                        self._normal = normal
                        return
                self._collision_triggered = False
                return
        self._collision_triggered = True
        self._target = obj
        self._point = point
        self._normal = normal

    def reset(self):
        GELogicContainer.reset(self)
        self._collision_triggered = False
        self._objects = []

    def _reset_last_monitored_object(self, new_monitored_object):
        if is_invalid(new_monitored_object):
            new_monitored_object = None
        if self._last_monitored_object == new_monitored_object:
            return
        if not isinstance(new_monitored_object, bge.types.KX_GameObject):
            if self._last_monitored_object is not None:
                self._last_monitored_object.collisionCallbacks.remove(
                    self._collision_callback
                )
                self._last_monitored_object = None
        else:
            if self._last_monitored_object is not None:
                self._last_monitored_object.collisionCallbacks.remove(
                    self._collision_callback
                )
            if new_monitored_object is not None:
                new_monitored_object.collisionCallbacks.append(
                    self._collision_callback
                )
                self._last_monitored_object = new_monitored_object
        self._set_value(False)
        self._target = None
        self._point = None
        self._normal = None
        self._collision_triggered = False

    def evaluate(self):
        last_target = self._target
        game_object = self.get_socket_value(self.game_object)
        self._reset_last_monitored_object(game_object)
        if is_waiting(game_object):
            return
        self._set_ready()
        collision = self._collision_triggered
        if last_target is not self._target:
            self._consumed = False
        if collision and not self.pulse:
            self._set_value(collision and not self._consumed)
            self._consumed = True
        elif self.pulse:
            self._set_value(collision)
        else:
            self._consumed = False
            self._set_value(False)


# Action Cells


class ActionAddObject(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.name = None
        self.reference = None
        self.life = None
        self.done = False
        self.obj = False
        self.OBJ = GEOutSocket(self, self._get_obj)
        self.OUT = GEOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def _get_obj(self):
        return self.obj

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        life = self.get_socket_value(self.life)
        name = self.get_socket_value(self.name)
        self._set_ready()
        reference = self.get_socket_value(self.reference)
        scene = logic.getCurrentScene()
        if is_waiting(life, name, reference):
            return
        self.obj = scene.addObject(name, reference, life)
        self.done = True


class ActionSetGameObjectGameProperty(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.property_name = None
        self.property_value = None
        self.done = False
        self.OUT = GEOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        property_name = self.get_socket_value(self.property_name)
        property_value = self.get_socket_value(self.property_value)
        if is_waiting(property_name, property_value):
            return
        if is_invalid(game_object):
            return
        if condition:
            self.done = True
            self._set_ready()
            game_object[property_name] = property_value


class SetMaterial(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.slot = None
        self.mat_name = None
        self.done = False
        self.OUT = GEOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        game_object = self.get_socket_value(self.game_object)
        slot = self.get_socket_value(self.slot) - 1
        mat_name = self.get_socket_value(self.mat_name)
        if not_met(condition):
            return
        if is_invalid(game_object):
            return
        if is_waiting(mat_name, slot):
            return
        self._set_ready()
        bl_obj = game_object.blenderObject
        if slot > len(bl_obj.material_slots) - 1:
            debug('Set Material: Slot does not exist!')
            return
        bl_obj.material_slots[slot].material = bpy.data.materials[mat_name]
        self.done = True


class ActionSetNodeTreeNodeValue(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.tree_name = None
        self.node_name = None
        self.input_slot = None
        self.value = None
        self.done = False
        self.OUT = GEOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        tree_name = self.get_socket_value(self.tree_name)
        node_name = self.get_socket_value(self.node_name)
        input_slot = self.get_socket_value(self.input_slot)
        value = self.get_socket_value(self.value)
        if is_waiting(node_name, input_slot, value):
            return
        if is_invalid(tree_name):
            return
        if condition:
            self.done = True
            self._set_ready()
            (
                bpy.data.node_groups[tree_name]
                .nodes[node_name]
                .inputs[input_slot]
                .default_value
            ) = value


class ActionSetNodeTreeNodeAttribute(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.tree_name = None
        self.node_name = None
        self.internal = None
        self.attribute = None
        self.value = None
        self.done = False
        self.OUT = GEOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        tree_name = self.get_socket_value(self.tree_name)
        node_name = self.get_socket_value(self.node_name)
        attribute = self.get_socket_value(self.attribute)
        internal = self.get_socket_value(self.internal)
        value = self.get_socket_value(self.value)
        if is_waiting(node_name, attribute, internal, value):
            return
        if is_invalid(tree_name):
            return
        if condition:
            self._set_ready()
            target = (
                bpy
                .data
                .node_groups[tree_name]
                .nodes[node_name]
            )
            if internal:
                target = getattr(target, internal, target)
            if hasattr(target, attribute):
                setattr(target, attribute, value)
            self.done = True


class ActionSetMaterialNodeValue(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.mat_name = None
        self.node_name = None
        self.input_slot = None
        self.value = None
        self.done = False
        self.OUT = GEOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        mat_name = self.get_socket_value(self.mat_name)
        node_name = self.get_socket_value(self.node_name)
        input_slot = self.get_socket_value(self.input_slot)
        value = self.get_socket_value(self.value)
        if is_waiting(node_name, input_slot, value):
            return
        if is_invalid(mat_name):
            return
        if condition:
            self.done = True
            self._set_ready()
            (
                bpy.data.materials[mat_name]
                .node_tree
                .nodes[node_name]
                .inputs[input_slot]
                .default_value
            ) = value


class ActionSetMaterialNodeAttribute(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.mat_name = None
        self.node_name = None
        self.internal = None
        self.attribute = None
        self.value = None
        self.done = False
        self.OUT = GEOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        mat_name = self.get_socket_value(self.mat_name)
        node_name = self.get_socket_value(self.node_name)
        attribute = self.get_socket_value(self.attribute)
        internal = self.get_socket_value(self.internal)
        value = self.get_socket_value(self.value)
        if is_waiting(node_name, attribute, internal, value):
            return
        if is_invalid(mat_name):
            return
        if condition:
            self._set_ready()
            target = (
                bpy.data.materials[mat_name]
                .node_tree
                .nodes[node_name]
            )
            if internal:
                target = getattr(target, internal, target)
            if hasattr(target, attribute):
                setattr(target, attribute, value)
            self.done = True


class ActionPlayMaterialSequence(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.mat_name = None
        self.node_name = None
        self.play_mode = None
        self.play_continue = None
        self.frames = None
        self.fps = None
        self.reverse = False
        self.time = 0.0
        self.on_start = False
        self.running = False
        self.on_finish = False
        self.frame = 0
        self._consumed = False
        self.ON_START = GEOutSocket(self, self._get_on_start)
        self.RUNNING = GEOutSocket(self, self._get_running)
        self.ON_FINISH = GEOutSocket(self, self._get_on_finish)
        self.FRAME = GEOutSocket(self, self._get_frame)

    def _get_on_start(self):
        return self.on_start
    
    def _get_running(self):
        return self.running
    
    def _get_on_finish(self):
        return self.on_finish
    
    def _get_frame(self):
        return self.frame

    def evaluate(self):
        self.done = False
        self.on_finish = False
        self.on_start = False
        running = self.running
        condition = self.get_socket_value(self.condition)
        play_continue = self.get_socket_value(self.play_continue)
        if not_met(condition) and not running:
            return
        self.time += self.network.time_per_frame
        mat_name = self.get_socket_value(self.mat_name)
        node_name = self.get_socket_value(self.node_name)
        play_mode = self.get_socket_value(self.play_mode)
        frames = self.get_socket_value(self.frames)
        fps = self.get_socket_value(self.fps)
        if is_waiting(
            mat_name,
            node_name,
            play_mode,
            frames,
            fps
        ):
            return
        rate = 1/fps
        speed = self.time / rate
        self._set_ready()
        if speed < 1:
            return
        self.time -= rate * speed
        player = (
            bpy.data.materials[mat_name]
            .node_tree
            .nodes[node_name]
        ).image_user
        start_frame = frames.y if self.reverse else frames.x
        end_frame = frames.x if self.reverse else frames.y
        inverted = (start_frame > end_frame)
        frame = self.frame = player.frame_offset
        reset_cond = (frame <= end_frame) if inverted else (frame >= end_frame)
        if not running:
            if not play_continue and play_mode > 2 or reset_cond:
                player.frame_offset = start_frame if inverted else end_frame
            if not play_continue:
                self.reverse = False
            self.on_start = True
            self._consumed = False
        stops = [3, 4, 5]

        start_cond = (frame > start_frame) if inverted else (frame < start_frame)

        if not condition and play_mode in stops:
            self.on_finish = True
            self.running = False
            return
        if start_cond:
            self.running = True
            player.frame_offset = start_frame
        frame = player.frame_offset
        run_cond = (frame > end_frame) if inverted else (frame < end_frame)
        if run_cond:
            self.running = True
            s = round(speed)
            if inverted:
                if frame - s < end_frame:
                    if play_mode in [1, 4]:
                        leftover = abs(frame - s - end_frame)
                        span = start_frame - end_frame
                        while leftover > span:
                            leftover -= span
                        player.frame_offset = start_frame - leftover
                    else:
                        player.frame_offset = end_frame
                else:
                    player.frame_offset -= s
            else:
                if frame + s > end_frame:
                    if play_mode in [1, 4]:
                        leftover = frame + s - end_frame
                        span = end_frame - start_frame
                        while leftover > span:
                            leftover -= span
                        player.frame_offset = start_frame + leftover
                    else:
                        player.frame_offset = end_frame
                else:
                    player.frame_offset += s
        elif play_mode == 1 and condition:
            player.frame_offset = start_frame
        elif play_mode == 4:
            player.frame_offset = start_frame
        elif play_mode == 3:
            if running and not self._consumed:
                self.on_finish = True
                self._consumed = True
        elif play_mode == 0 or play_mode == 3:
            if running and not self._consumed:
                self.on_finish = True
                self._consumed = True
            if not condition:
                self.running = False
        elif play_mode == 2 or play_mode == 5:
            if running and not condition:
                self.on_finish = True
            if not condition:
                self.running = False
            self.reverse = not self.reverse
        else:
            if running:
                self.on_finish = True
            self.running = False
        self.done = True


class ActionToggleGameObjectGameProperty(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.property_name = None
        self.done = False
        self.OUT = GEOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        property_name = self.get_socket_value(self.property_name)
        if is_waiting(property_name):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        if condition:
            value = game_object[property_name]
            game_object[property_name] = not value
        self.done = True


class ActionAddToGameObjectGameProperty(GEActionNode):

    @classmethod
    def op_by_code(cls, str):
        import operator
        opmap = {
            "ADD": operator.add,
            "SUB": operator.sub,
            "DIV": operator.truediv,
            "MUL": operator.mul
        }
        return opmap.get(str)

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.property_name = None
        self.property_value = None
        self.operator = None
        self.done = False
        self.OUT = GEOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        property_name = self.get_socket_value(self.property_name)
        property_value = self.get_socket_value(self.property_value)
        if is_waiting(property_name, property_value):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        value = game_object[property_name]
        game_object[property_name] = (
            self.operator(value, property_value)
        )
        self.done = True


class CopyPropertyFromObject(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.from_object = None
        self.to_object = None
        self.property_name = None
        self.done = False
        self.OUT = GEOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        from_object = self.get_socket_value(self.from_object)
        to_object = self.get_socket_value(self.to_object)
        if is_invalid(from_object, to_object):
            return
        property_name = self.get_socket_value(self.property_name)
        if is_waiting(property_name):
            return
        self._set_ready()
        val = from_object.get(property_name)
        if val is not None:
            to_object[property_name] = val
        self.done = True


class ActionClampedAddToGameObjectGameProperty(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.property_name = None
        self.property_value = None
        self.range = None
        self.done = False
        self.OUT = GEOutSocket(self, self._get_done)

    def _get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        game_object = self.get_socket_value(self.game_object)
        if not_met(condition):
            return
        if is_invalid(game_object):
            return
        property_name = self.get_socket_value(self.property_name)
        property_value = self.get_socket_value(self.property_value)
        val_range = self.get_socket_value(self.range)
        if is_waiting(property_name, property_value):
            return
        self._set_ready()
        value = game_object[property_name]
        new_val = value + property_value
        if new_val > val_range.y:
            new_val = val_range.y
        if new_val < val_range.x:
            new_val = val_range.x
        game_object[property_name] = (
            new_val
        )
        self.done = True


class ValueSwitch(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.conditon = None
        self.val_a = None
        self.val_b = None
        self.out_value = False
        self.VAL = GEOutSocket(self, self._get_out_value)

    def _get_out_value(self):
        return self.out_value

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        val_a = self.get_socket_value(self.val_a)
        val_b = self.get_socket_value(self.val_b)
        self._set_ready()
        self.out_value = (
            val_a if condition is True else val_b
        )


class InvertBool(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.value = None
        self.out_value = False
        self.OUT = GEOutSocket(self, self._get_out_value)

    def _get_out_value(self):
        return self.out_value

    def evaluate(self):
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            self.out_value = False
            return
        self._set_ready()
        self.out_value = not value


class InvertValue(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.value = None
        self.out_value = False
        self.OUT = GEOutSocket(self, self._get_out_value)

    def _get_out_value(self):
        return self.out_value

    def evaluate(self):
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            self.out_value = 0
            return
        self._set_ready()
        self.out_value = -value


class AbsoluteValue(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.value = None
        self.out_value = False
        self.OUT = GEOutSocket(self, self._get_out_value)

    def _get_out_value(self):
        return self.out_value

    def evaluate(self):
        if is_invalid(self.value):
            return
        value = self.get_socket_value(self.value)
        self._set_ready()
        self.out_value = math.fabs(value)


class ActionPrint(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        self._set_ready()
        print(value)
        self.done = True


class ActionCreateVehicle(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.wheels_steering = None
        self.wheels = None
        self.suspension = None
        self.stiffness = None
        self.damping = None
        self.friction = None
        self.done = None
        self.vehicle = None
        self.wheels = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.VEHICLE = GEOutSocket(self, self.get_vehicle)
        self.WHEELS = GEOutSocket(self, self.get_wheels)

    def get_done(self):
        return self.done

    def get_vehicle(self):
        return self.vehicle

    def get_wheels(self):
        return self.wheels

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        wheels_steering = self.get_socket_value(self.wheels_steering)
        wheels = self.get_socket_value(self.wheels)
        suspension = self.get_socket_value(self.suspension)
        stiffness = self.get_socket_value(self.stiffness)
        damping = self.get_socket_value(self.damping)
        friction = self.get_socket_value(self.friction)
        if is_waiting(
            game_object,
            wheels_steering,
            wheels,
            suspension,
            stiffness,
            damping,
            friction
        ):
            return
        self._set_ready()
        orig_ori = game_object.worldOrientation
        game_object.worldOrientation = Euler((0, 0, 0), 'XYZ')
        ph_id = game_object.getPhysicsId()
        car = bge.constraints.createVehicle(ph_id)
        down = Vector((0, 0, -1))
        axle_dir = Vector((0, -1, 0))
        wheels_steering = bpy.data.collections[wheels_steering]
        wheels = bpy.data.collections[wheels]
        for wheel in wheels_steering.objects:
            wheel = check_game_object(wheel.name)
            car.addWheel(
                wheel,
                wheel.worldPosition - game_object.worldPosition,
                down,
                axle_dir,
                suspension,
                abs(wheel.worldScale.x/2),
                True
            )
        for wheel in wheels.objects:
            wheel = check_game_object(wheel.name)
            car.addWheel(
                wheel,
                wheel.worldPosition - game_object.worldPosition,
                down,
                axle_dir,
                suspension,
                abs(wheel.worldScale.x/2),
                False
            )
        for wheel in range(car.getNumWheels()):
            car.setSuspensionStiffness(stiffness, wheel)
            car.setSuspensionDamping(damping, wheel)
            car.setTyreFriction(friction, wheel)
        self.vehicle = car
        game_object.worldOrientation = orig_ori
        self.done = True


class ActionCreateVehicleFromParent(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.suspension = None
        self.stiffness = None
        self.damping = None
        self.friction = None
        self.wheel_size = None
        self.done = None
        self.vehicle = None
        self.wheels = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.VEHICLE = GEOutSocket(self, self.get_vehicle)
        self.WHEELS = GEOutSocket(self, self.get_wheels)

    def get_done(self):
        return self.done

    def get_vehicle(self):
        return self.vehicle

    def get_wheels(self):
        return self.wheels

    def evaluate(self):
        self.done = False
        game_object = self.get_socket_value(self.game_object)
        if not_met(self.get_socket_value(self.condition)):
            if game_object.get('_vconst'):
                self._set_ready()
                self.vehicle = game_object['_vconst']
            return
        suspension = self.get_socket_value(self.suspension)
        stiffness = self.get_socket_value(self.stiffness)
        damping = self.get_socket_value(self.damping)
        friction = self.get_socket_value(self.friction)
        wheel_size = self.get_socket_value(self.wheel_size)
        if is_waiting(
            game_object,
            suspension,
            stiffness,
            damping,
            friction,
            wheel_size
        ):
            return
        self._set_ready()
        orig_ori = game_object.localOrientation.copy()
        game_object.localOrientation = Euler((0, 0, 0), 'XYZ')
        ph_id = game_object.getPhysicsId()
        car = bge.constraints.createVehicle(ph_id)
        down = Vector((0, 0, -1))
        axle_dir = game_object.getAxisVect(Vector((0, -1, 0)))
        wheels = []
        cs = sorted(game_object.children, key=lambda c: c.name)
        for c in cs:
            if 'FWheel' in c.name:
                c.removeParent()
                car.addWheel(
                    c,
                    c.worldPosition - game_object.worldPosition,
                    down,
                    axle_dir,
                    suspension,
                    abs(c.worldScale.x/2) * wheel_size,
                    True
                )
                wheels.append(c)
            elif 'RWheel' in c.name:
                c.removeParent()
                car.addWheel(
                    c,
                    c.worldPosition - game_object.worldPosition,
                    down,
                    axle_dir,
                    suspension,
                    abs(c.worldScale.x/2) * wheel_size,
                    False
                )
                wheels.append(c)
        for wheel in range(car.getNumWheels()):
            car.setSuspensionStiffness(stiffness, wheel)
            car.setSuspensionDamping(damping, wheel)
            car.setTyreFriction(friction, wheel)
        game_object.localOrientation = orig_ori
        self.vehicle = game_object['_vconst'] = car
        self.wheels = wheels
        self.done = True


class VehicleApplyForce(GEActionNode):
    def __init__(self, value_type='REAR'):
        GEActionNode.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.vehicle = None
        self.wheelcount = None
        self._reset = False
        self.power = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        vehicle = self.get_socket_value(self.vehicle)
        if is_invalid(vehicle):
            return
        constraint = vehicle.get('_vconst', None)
        if not constraint:
            return
        if not_met(condition):
            if self._reset:
                for wheel in range(constraint.getNumWheels()):
                    constraint.applyEngineForce(0, wheel)
                self._reset = False
            return
        value = self.get_socket_value(self.value_type)
        wheelcount = self.get_socket_value(self.wheelcount)
        power = self.get_socket_value(self.power)
        if is_waiting(value, wheelcount, power):
            return
        self._reset = True
        self._set_ready()
        if value == 'FRONT':
            for wheel in range(wheelcount):
                constraint.applyEngineForce(power, wheel)
        if value == 'REAR':
            for wheel in range(wheelcount):
                wheel = constraint.getNumWheels() - wheel - 1
                constraint.applyEngineForce(power, wheel)
        if value == 'ALL':
            for wheel in range(constraint.getNumWheels()):
                constraint.applyEngineForce(power, wheel)
        self.done = True


class VehicleApplyBraking(GEActionNode):
    def __init__(self, value_type='REAR'):
        GEActionNode.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.vehicle = None
        self.wheelcount = None
        self._reset = False
        self.power = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        vehicle = self.get_socket_value(self.vehicle)
        if is_invalid(vehicle):
            return
        constraint = vehicle.get('_vconst', None)
        if not constraint:
            return
        if not_met(condition):
            if self._reset:
                for wheel in range(constraint.getNumWheels()):
                    constraint.applyBraking(0, wheel)
                self._reset = False
            return
        value_type = self.get_socket_value(self.value_type)
        wheelcount = self.get_socket_value(self.wheelcount)
        power = self.get_socket_value(self.power)
        if is_waiting(value_type, wheelcount, power):
            return
        self._reset = True
        self._set_ready()
        if value_type == 'FRONT':
            for wheel in range(wheelcount):
                constraint.applyBraking(power, wheel)
        if value_type == 'REAR':
            for wheel in range(wheelcount):
                wheel = constraint.getNumWheels() - wheel - 1
                constraint.applyBraking(power, wheel)
        if value_type == 'ALL':
            for wheel in range(constraint.getNumWheels()):
                constraint.applyBraking(power, wheel)
        self.done = True


class VehicleApplySteering(GEActionNode):
    def __init__(self, value_type='REAR'):
        GEActionNode.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.vehicle = None
        self.wheelcount = None
        self._reset = False
        self.power = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        vehicle = self.get_socket_value(self.vehicle)
        if is_invalid(vehicle):
            return
        constraint = vehicle.get('_vconst', None)
        if not constraint:
            return
        if not_met(condition):
            if self._reset:
                for wheel in range(constraint.getNumWheels()):
                    constraint.setSteeringValue(0, wheel)
                self._reset = False
            return
        value_type = self.get_socket_value(self.value_type)
        wheelcount = self.get_socket_value(self.wheelcount)
        power = self.get_socket_value(self.power)
        if is_waiting(value_type, wheelcount, power):
            return
        self._reset = True
        self._set_ready()
        if value_type == 'FRONT':
            for wheel in range(wheelcount):
                constraint.setSteeringValue(power, wheel)
        if value_type == 'REAR':
            for wheel in range(wheelcount):
                wheel = constraint.getNumWheels() - wheel - 1
                constraint.setSteeringValue(power, wheel)
        if value_type == 'ALL':
            for wheel in range(constraint.getNumWheels()):
                constraint.setSteeringValue(power, wheel)
        self.done = True


class VehicleSetAttributes(GEActionNode):
    def __init__(self, value_type='REAR'):
        GEActionNode.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.vehicle = None
        self.wheelcount = None
        self.set_suspension_compression = False
        self.suspension_compression = False
        self.set_suspension_stiffness = False
        self.suspension_stiffness = False
        self.set_suspension_damping = False
        self.suspension_damping = False
        self.set_tyre_friction = False
        self.tyre_friction = False
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def set_attributes(self, car, wheel, attrs, values):
        if attrs[0] is True:
            car.setSuspensionCompression(values[0], wheel)
        if attrs[1] is True:
            car.setSuspensionStiffness(values[1], wheel)
        if attrs[2] is True:
            car.setSuspensionDamping(values[2], wheel)
        if attrs[3] is True:
            car.setTyreFriction(values[3], wheel)

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        vehicle = self.get_socket_value(self.vehicle)
        value_type = self.get_socket_value(self.value_type)
        wheelcount = self.get_socket_value(self.wheelcount)
        if is_waiting(value_type, wheelcount):
            return
        if is_invalid(vehicle):
            return
        attrs_to_set = [
            self.get_socket_value(self.set_suspension_compression),
            self.get_socket_value(self.set_suspension_stiffness),
            self.get_socket_value(self.set_suspension_damping),
            self.get_socket_value(self.set_tyre_friction)
        ]
        values_to_set = [
            self.get_socket_value(self.suspension_compression),
            self.get_socket_value(self.suspension_stiffness),
            self.get_socket_value(self.suspension_damping),
            self.get_socket_value(self.tyre_friction)
        ]
        constraint = vehicle.get('_vconst', None)
        if not constraint:
            return
        self._set_ready()
        if value_type == 'FRONT':
            for wheel in range(wheelcount):
                self.set_attributes(
                    constraint,
                    wheel,
                    attrs_to_set,
                    values_to_set
                )
        if value_type == 'REAR':
            for wheel in range(wheelcount):
                wheel = constraint.getNumWheels() - wheel - 1
                self.set_attributes(
                    constraint,
                    wheel,
                    attrs_to_set,
                    values_to_set
                )
        if value_type == 'ALL':
            for wheel in range(constraint.getNumWheels()):
                self.set_attributes(
                    constraint,
                    wheel,
                    attrs_to_set,
                    values_to_set
                )
        self.done = True


class ActionSetObjectAttribute(GEActionNode):
    def __init__(self, value_type='worldPosition'):
        GEActionNode.__init__(self)
        self.value_type = str(value_type)
        self.condition = None
        self.xyz = None
        self.game_object = None
        self.attribute_value = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        xyz = self.get_socket_value(self.xyz)
        game_object = self.get_socket_value(self.game_object)
        attribute = self.get_socket_value(self.value_type)
        value = self.get_socket_value(self.attribute_value)
        if is_waiting(xyz, game_object, attribute, value):
            return

        if hasattr(value, attribute):
            value = getattr(value, attribute).copy()
        self._set_ready()
        if not hasattr(game_object, attribute):
            debug(
                'Set Object Data Node: {} has no attribute {}!'
                .format(game_object, attribute)
            )
            return
        data = getattr(game_object, attribute)
        if 'Orientation' in attribute:
            data = data.to_euler()
        for axis in xyz:
            if not xyz[axis]:
                setattr(value, axis, getattr(data, axis))
        setattr(
            game_object,
            attribute,
            value
        )
        if value == 'worldScale':
            game_object.reinstancePhysicsMesh(
                game_object,
                game_object.meshes[0]
            )
        self.done = True


class ActionInstalSubNetwork(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.target_object = None
        self.tree_name = None
        self.initial_status = None
        self._network = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def setup(self, network):
        self._network = network

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        target_object = self.get_socket_value(self.target_object)
        tree_name = self.get_socket_value(self.tree_name)
        initial_status = self.get_socket_value(self.initial_status)
        if is_waiting(
            target_object,
            tree_name,
            initial_status
        ):
            return
        self._set_ready()
        if is_invalid(target_object):
            return
        self._network.install_subnetwork(
            target_object,
            tree_name,
            initial_status
        )
        self.done = True


class ActionExecuteNetwork(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.target_object = None
        self.tree_name = None
        self._network = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def setup(self, network):
        self._network = network

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        target_object = self.get_socket_value(self.target_object)
        tree_name = self.get_socket_value(self.tree_name)
        self._set_ready()
        if is_invalid(target_object):
            return
        added_network = target_object.get(f'IGNLTree_{tree_name}', None)
        if not added_network:
            self._network.install_subnetwork(
                target_object,
                tree_name,
                False
            )
            added_network = target_object.get(f'IGNLTree_{tree_name}', None)
        if condition:
            added_network.stopped = False
        else:
            added_network.stop()
            added_network.stopped = True
            return
        self.done = True


class ActionStartLogicNetwork(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.logic_network_name = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        logic_network_name = self.get_socket_value(self.logic_network_name)
        if is_waiting(game_object, logic_network_name):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        network = game_object.get(f'IGNLTree_{logic_network_name}')
        if network is not None:
            network.stopped = False
        self.done = True


class ActionStopLogicNetwork(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.logic_network_name = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        logic_network_name = self.get_socket_value(self.logic_network_name)
        if is_waiting(game_object, logic_network_name):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        network = game_object.get(f'IGNLTree_{logic_network_name}')
        network.stop()
        self.done = True


class ActionFindObject(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.game_object = None

    def evaluate(self):
        self._set_ready()
        game_object = self.get_socket_value(self.game_object)
        self._set_value(game_object)


class ActionSendMessage(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.from_obj = None
        self.to_obj = None
        self.subject = None
        self.body = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            self._set_value(False)
            return
        from_obj = self.get_socket_value(self.from_obj)
        to_obj = self.get_socket_value(self.to_obj)
        subject = self.get_socket_value(self.subject)
        body = self.get_socket_value(self.body)
        if is_waiting(from_obj, to_obj, subject, body):
            return
        self._set_ready()
        if body and to_obj:
            from_obj.sendMessage(subject, body=body, to=to_obj)
        elif body:
            from_obj.sendMessage(subject, body=body)
        elif to_obj:
            from_obj.sendMessage(subject, to=to_obj)
        else:
            from_obj.sendMessage(subject)
        self._set_value(True)


class ActionSetGameObjectVisibility(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.visible: bool = None
        self.recursive: bool = None
        self.done: bool = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        visible: bool = self.get_socket_value(self.visible)
        recursive: bool = self.get_socket_value(self.recursive)
        if is_waiting(visible, recursive):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        if visible is None:
            return
        if recursive is None:
            return
        game_object.setVisible(visible, recursive)
        self.done = True


class SetCurvePoints(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.curve_object = None
        self.points: list = None
        self.done: bool = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        curve_object = self.get_socket_value(self.curve_object)
        points = self.get_socket_value(self.points)
        if is_waiting(points):
            return
        if is_invalid(curve_object):
            return
        self._set_ready()
        if not points:
            return
        curve = curve_object.blenderObject.data
        for spline in curve.splines:
            curve.splines.remove(spline)
        spline = curve.splines.new('NURBS')
        pos = curve_object.worldPosition
        spline.points.add(len(points))
        for p, new_co in zip(spline.points, points):
            p.co = ([new_co.x - pos.x, new_co.y - pos.y, new_co.z - pos.z] + [1.0])
        self.done = True


class ActionRayPick(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.origin = None
        self.destination = None
        self.local: bool = None
        self.property_name: str = None
        self.xray: bool = None
        self.custom_dist: bool = None
        self.distance: float = None
        self.visualize: bool = None
        self._picked_object = None
        self._point = None
        self._normal = None
        self._direction = None
        self.PICKED_OBJECT = GEOutSocket(self, self.get_picked_object)
        self.POINT = GEOutSocket(self, self.get_point)
        self.NORMAL = GEOutSocket(self, self.get_normal)
        self.DIRECTION = GEOutSocket(self, self.get_direction)
        self.network = None

    def setup(self, network):
        self.network = network

    def get_picked_object(self):
        return self._picked_object

    def get_point(self):
        return self._point

    def get_normal(self):
        return self._normal

    def get_direction(self):
        return self._direction

    def _compute_direction(self, origin, dest, local, dist):
        custom_dist = self.get_socket_value(self.custom_dist)
        start = origin.worldPosition.copy() if hasattr(origin, "worldPosition") else origin
        if hasattr(dest, "worldPosition"):
            dest = dest.worldPosition.copy()
        if local:
            dest = start + dest
        d = dest - start
        d.normalize()
        return d, dist if custom_dist else (start - dest).length, dest

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            self._normal = None
            self._object = None
            # self._point = None
            return
        origin = self.get_socket_value(self.origin)
        destination = self.get_socket_value(self.destination)
        local: bool = self.get_socket_value(self.local)
        property_name: str = self.get_socket_value(self.property_name)
        xray: bool = self.get_socket_value(self.xray)
        distance: float = self.get_socket_value(self.distance)
        visualize: bool = self.get_socket_value(self.visualize)

        if is_waiting(origin, destination, local, property_name, distance):
            return
        self._set_ready()
        caster = self.network._owner
        obj, point, normal = None, None, None
        direction, distance, destination = self._compute_direction(origin, destination, local, distance)
        if not property_name:
            obj, point, normal = caster.rayCast(
                destination,
                origin,
                distance,
                xray=xray
            )
        else:
            obj, point, normal = caster.rayCast(
                destination,
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
            bge.render.drawLine(
                origin,
                line_dest,
                [
                    1,
                    0,
                    0,
                    1
                ]
            )
            if obj:
                bge.render.drawLine(
                    origin,
                    point,
                    [
                        0,
                        1,
                        0,
                        1
                    ]
                )
        self._set_value(obj is not None)
        self._picked_object = obj
        self._point = point
        self._normal = normal
        self._direction = direction


class ProjectileRayCast(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.origin = None
        self.destination = None
        self.power: float = None
        self.resolution: float = None
        self.property_name: str = None
        self.xray: bool = None
        self.distance: float = None
        self.visualize: bool = None
        self._picked_object = None
        self._point = None
        self._normal = None
        self._parabola = None
        self.PICKED_OBJECT = GEOutSocket(self, self.get_picked_object)
        self.POINT = GEOutSocket(self, self.get_point)
        self.NORMAL = GEOutSocket(self, self.get_normal)
        self.PARABOLA = GEOutSocket(self, self.get_parabola)
        self.network = None

    def setup(self, network):
        self.network = network

    def get_picked_object(self):
        return self._picked_object

    def get_parabola(self):
        return self._parabola

    def get_point(self):
        return self._point

    def get_normal(self):
        return self._normal

    def calc_projectile(self, t, vel, pos):
        half: float = logic.getCurrentScene().gravity.z * (.5 * t * t)
        vel = vel * t
        return Vector((0,0, half)) + vel + pos

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            self._out_normal = None
            self._out_object = None
            self._out_point = None
            return
        origin = self.get_socket_value(self.origin)
        power: float = self.get_socket_value(self.power)
        destination = self.get_socket_value(self.destination)
        resolution: float = 1 - (self.get_socket_value(self.resolution) * .99)
        property_name: str = self.get_socket_value(self.property_name)
        xray: bool = self.get_socket_value(self.xray)
        distance: float = self.get_socket_value(self.distance)
        visualize: bool = self.get_socket_value(self.visualize)

        if is_waiting(origin, destination, property_name, distance):
            return
        destination.normalize(); destination *= power
        origin = getattr(origin, 'worldPosition', origin)

        points: list = []
        color: list = [1, 0, 0]
        idx = 0
        total_dist: float = 0
        found: bool = False
        owner = self.network._owner

        self._set_ready()

        while total_dist < distance:
            target = (self.calc_projectile(idx, destination, origin))
            start = origin if not points else points[-1]
            obj, point, normal = owner.rayCast(start, target, prop=property_name, xray=xray)
            total_dist += (target-start).length
            if not obj:
                points.append(target)
            else:
                points.append(point)
                color = [0, 1, 0]
                found = True
                break
            idx += resolution
        if visualize:
            for i, p in enumerate(points):
                if i < len(points) - 1:
                    bge.render.drawLine(p, points[i+1], color)
        self._set_value(points[-1] if found else None)
        self._picked_object = obj
        self._point = point
        self._normal = normal
        self._parabola = points



class ActionMousePick(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.distance = None
        self.property = None
        self.xray = None
        self.camera = None
        self._set_value(False)
        self._out_object = None
        self._out_normal = None
        self._out_point = None
        self.OUTOBJECT = GEOutSocket(self, self.get_out_object)
        self.OUTNORMAL = GEOutSocket(self, self.get_out_normal)
        self.OUTPOINT = GEOutSocket(self, self.get_out_point)

    def get_out_object(self):
        return self._out_object

    def get_out_normal(self):
        return self._out_normal

    def get_out_point(self):
        return self._out_point

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        distance = self.get_socket_value(self.distance)
        property_name = self.get_socket_value(self.property)
        xray = self.get_socket_value(self.xray)
        camera = self.get_socket_value(self.camera)
        if is_waiting(distance, property_name, xray, camera):
            return
        self._set_ready()
        if not condition:
            self._set_value(False)
            self._out_normal = None
            self._out_object = None
            self._out_point = None
            return
        if is_invalid(camera):
            return
        mpos = logic.mouse.position
        vec = 10 * camera.getScreenVect(*mpos)
        ray_target = camera.worldPosition - vec
        target, point, normal = self.network.ray_cast(
            camera,
            None,
            ray_target,
            property_name,
            xray,
            distance
        )
        self._set_value(target is not None)
        self._out_object = target
        self._out_normal = normal
        self._out_point = point


class ActionCameraPick(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.camera = None
        self.aim = None
        self.property_name = None
        self.xray = None
        self.distance = None
        self._picked_object = None
        self._picked_point = None
        self._picked_normal = None
        self.PICKED_OBJECT = GEOutSocket(self, self.get_picked_object)
        self.PICKED_POINT = GEOutSocket(self, self.get_picked_point)
        self.PICKED_NORMAL = GEOutSocket(self, self.get_picked_normal)

    def get_picked_object(self):
        return self._picked_object

    def get_picked_point(self):
        return self._picked_point

    def get_picked_normal(self):
        return self._picked_normal

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        camera = self.get_socket_value(self.camera)
        aim = self.get_socket_value(self.aim)
        property_name = self.get_socket_value(self.property_name)
        xray = self.get_socket_value(self.xray)
        distance = self.get_socket_value(self.distance)
        if is_waiting(camera, aim, property_name, xray, distance):
            return
        self._set_ready()
        if not condition:
            self._set_value(False)
            self._out_normal = None
            self._out_object = None
            self._out_point = None
            return
        if is_invalid(camera):
            return
        if is_invalid(aim):
            return
        obj, point, normal = None, None, None
        # assume screen coordinates
        if isinstance(aim, Vector) and len(aim) == 2:
            vec = 10 * camera.getScreenVect(aim[0], aim[1])
            ray_target = camera.worldPosition - vec
            aim = ray_target
        if not property_name:
            obj, point, normal = camera.rayCast(aim, None, distance)
        else:
            obj, point, normal = camera.rayCast(
                aim,
                None,
                distance,
                property_name,
                xray=xray
            )
        self._set_value(obj is not None)
        self._picked_object = obj
        self._picked_point = point
        self._picked_normal = normal


class ActionSetActiveCamera(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.camera = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        camera = self.get_socket_value(self.camera)
        if is_waiting(camera):
            return
        self._set_ready()
        if is_invalid(camera):
            return
        scene = logic.getCurrentScene()
        scene.active_camera = camera
        self.done = True


class ActionSetCameraFov(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.camera = None
        self.fov = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        camera = self.get_socket_value(self.camera)
        fov = self.get_socket_value(self.fov)
        if is_waiting(camera, fov):
            return
        self._set_ready()
        if is_invalid(camera):
            return
        camera.fov = fov
        self.done = True


class ActionSetCameraOrthoScale(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.camera = None
        self.scale = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        camera = self.get_socket_value(self.camera)
        scale = self.get_socket_value(self.scale)
        if is_waiting(camera, scale):
            return
        self._set_ready()
        if is_invalid(camera):
            return
        camera.ortho_scale = scale
        self.done = True


class ActionSetResolution(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.x_res = None
        self.y_res = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        x_res = self.get_socket_value(self.x_res)
        y_res = self.get_socket_value(self.y_res)
        if is_waiting(x_res, y_res):
            return
        self._set_ready()
        bge.render.setWindowSize(x_res, y_res)
        self.done = True


class ActionSetFullscreen(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.use_fullscreen = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        use_fullscreen = self.get_socket_value(self.use_fullscreen)
        if is_waiting(use_fullscreen):
            return
        self._set_ready()
        bge.render.setFullScreen(use_fullscreen)
        self.done = True


class GESetProfile(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.use_profile = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        use_profile = self.get_socket_value(self.use_profile)
        if is_waiting(use_profile):
            return
        self._set_ready()
        bge.render.showProfile(use_profile)
        self.done = True


class GEShowFramerate(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.use_framerate = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        use_framerate = self.get_socket_value(self.use_framerate)
        if is_waiting(use_framerate):
            return
        self._set_ready()
        bge.render.showFramerate(use_framerate)
        self.done = True


class GetVSync(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)

    def evaluate(self):
        self._set_ready()
        self._set_value(bge.render.getVsync())


class GetFullscreen(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)

    def evaluate(self):
        self._set_ready()
        self._set_value(bge.render.getFullScreen())


class GEDrawLine(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.color = None
        self.from_point = None
        self.to_point = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        from_point = self.get_socket_value(self.from_point)
        to_point = self.get_socket_value(self.to_point)
        color = self.get_socket_value(self.color)
        if is_invalid(from_point, to_point, color):
            return
        self._set_ready()
        bge.render.drawLine(
            from_point,
            to_point,
            [
                color.x,
                color.y,
                color.z,
                1
            ]
        )
        self._set_value(True)


class GetResolution(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.width = None
        self.height = None
        self.res = None
        self.WIDTH = GEOutSocket(self, self.get_width)
        self.HEIGHT = GEOutSocket(self, self.get_height)
        self.RES = GEOutSocket(self, self.get_res)

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_res(self):
        return self.res

    def evaluate(self):
        self._set_ready()
        self.width = bge.render.getWindowWidth()
        self.height = bge.render.getWindowHeight()
        self.res = Vector((self.width, self.height))


class ActionSetVSync(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.vsync_mode = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        vsync_mode = self.get_socket_value(self.vsync_mode)
        if is_waiting(vsync_mode):
            return
        self._set_ready()
        bge.render.setVsync(vsync_mode)
        self.done = True


class InitEmptyDict(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.dict = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.DICT = GEOutSocket(self, self.get_dict)

    def get_done(self):
        return self.done

    def get_dict(self):
        return self.dict

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        self.dict = {}
        self.done = True


class InitNewDict(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.dict = None
        self.key = None
        self.val = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.DICT = GEOutSocket(self, self.get_dict)

    def get_done(self):
        return self.done

    def get_dict(self):
        return self.dict

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        key = self.get_socket_value(self.key)
        value = self.get_socket_value(self.val)
        if is_waiting(key, value):
            return
        if not condition:
            return
        self._set_ready()
        self.dict = {str(key): value}
        self.done = True


class SetDictKeyValue(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.dict = None
        self.key = None
        self.val = None
        self.new_dict = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.DICT = GEOutSocket(self, self.get_dict)

    def get_done(self):
        return self.done

    def get_dict(self):
        return self.new_dict

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        dictionary = self.get_socket_value(self.dict)
        key = self.get_socket_value(self.key)
        val = self.get_socket_value(self.val)
        if is_waiting(dictionary, key, val):
            return
        self._set_ready()
        dictionary[key] = val
        self.new_dict = dictionary
        self.done = True


class SetDictDelKey(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.dict = None
        self.key = None
        self.new_dict = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.DICT = GEOutSocket(self, self.get_dict)

    def get_done(self):
        return self.done

    def get_dict(self):
        return self.new_dict

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        dictionary = self.get_socket_value(self.dict)
        key = self.get_socket_value(self.key)
        if is_waiting(dictionary, key):
            return
        self._set_ready()
        if key in dictionary:
            del dictionary[key]
        else:
            debug("Dict Delete Key Node: Key '{}' not in Dict!".format(key))
            return
        self.new_dict = dictionary
        self.done = True


class InitEmptyList(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.length = None
        self.items = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.LIST = GEOutSocket(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.items

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        length = self.get_socket_value(self.length)
        if is_waiting(length):
            return
        self._set_ready()
        self.items = [None for x in range(length)]
        self.done = True


class InitNewList(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.value = None
        self.value2 = None
        self.value3 = None
        self.value4 = None
        self.value5 = None
        self.value6 = None
        self.items: list = None
        self.LIST = GEOutSocket(self, self.get_list)

    def get_list(self):
        return self.items

    def evaluate(self):
        value = self.get_socket_value(self.value)
        value2 = self.get_socket_value(self.value2)
        value3 = self.get_socket_value(self.value3)
        value4 = self.get_socket_value(self.value4)
        value5 = self.get_socket_value(self.value5)
        value6 = self.get_socket_value(self.value6)
        values = [value, value2, value3, value4, value5, value6]
        self.items = []
        self._set_ready()
        for val in values:
            if not is_waiting(val) and not is_invalid(val):
                self.items.append(val)


class AppendListItem(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.items: list = None
        self.val = None
        self.new_list: list = None
        self.done: bool = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.LIST = GEOutSocket(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.new_list

    def evaluate(self):
        self.done: bool = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        list_d: list = self.get_socket_value(self.items)
        val = self.get_socket_value(self.val)
        if is_waiting(list_d, val):
            return
        self._set_ready()
        list_d.append(val)
        self.new_list = list_d
        self.done = True


class SetListIndex(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.items: list = None
        self.index: int = None
        self.val = None
        self.new_list: list = None
        self.done: bool = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.LIST = GEOutSocket(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.new_list

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        list_d: list = self.get_socket_value(self.items)
        index: int = self.get_socket_value(self.index)
        val = self.get_socket_value(self.val)
        if is_invalid(list_d, index, val):
            return
        self._set_ready()
        list_d[index] = val
        self.new_list = list_d
        self.done = True


class RemoveListValue(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.items = None
        self.val = None
        self.new_list = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.LIST = GEOutSocket(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.new_list

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        list_d = self.get_socket_value(self.items)
        val = self.get_socket_value(self.val)
        if is_invalid(list_d, val):
            return
        self._set_ready()
        if val in list_d:
            list_d.remove(val)
        else:
            debug("List Remove Value Node: Item '{}' not in List!".format(val))
            return
        self.new_list = list_d
        self.done = True


class RemoveListIndex(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.items = None
        self.idx = None
        self.new_list = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.LIST = GEOutSocket(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.new_list

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        list_d = self.get_socket_value(self.items)
        idx = self.get_socket_value(self.idx)
        if is_invalid(list_d, idx):
            return
        self._set_ready()
        if len(list_d) > idx:
            del list_d[idx]
        else:
            debug("List Index exceeds length!")
            return
        self.new_list = list_d
        self.done = True


class ActionSetParent(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.child_object = None
        self.parent_object = None
        self.compound = True
        self.ghost = True
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        child_object = self.get_socket_value(self.child_object)
        parent_object = self.get_socket_value(self.parent_object)
        compound = self.get_socket_value(self.compound)
        ghost = self.get_socket_value(self.ghost)
        self._set_ready()
        if is_invalid(child_object, parent_object, compound, ghost):
            return
        if child_object.parent is parent_object:
            return
        child_object.setParent(parent_object, compound, ghost)
        self.done = True


class ActionRemoveParent(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.child_object = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        child_object = self.get_socket_value(self.child_object)
        if is_waiting(child_object):
            return
        self._set_ready()
        if is_invalid(child_object):
            return
        if not child_object.parent:
            return
        child_object.removeParent()
        self.done = True


class ActionPerformanceProfile(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.network = None
        self.print_profile = False
        self.check_evaluated_cells = False
        self.check_average_cells_per_sec = False
        self.check_cells_per_tick = False
        self.done = None
        self.data = ''
        self.OUT = GEOutSocket(self, self.get_done)
        self.DATA = GEOutSocket(self, self.get_data)

    def get_done(self):
        return self.done

    def get_data(self):
        return self.data

    def setup(self, network):
        self.network = network

    def evaluate(self):
        self.done = False
        self.data = '----------------------------------Start Profile\n'
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        print_profile = self.get_socket_value(
            self.print_profile
        )
        check_evaluated_cells = self.get_socket_value(
            self.check_evaluated_cells
        )
        check_average_cells_per_sec = self.get_socket_value(
            self.check_average_cells_per_sec
        )
        check_cells_per_tick = self.get_socket_value(
            self.check_cells_per_tick
        )
        if is_waiting(
            print_profile,
            check_evaluated_cells,
            check_average_cells_per_sec,
            check_cells_per_tick
        ):
            self._set_ready()
            return
        self._set_ready()
        if check_evaluated_cells:
            self.data += 'Evaluated Nodes:\t{}\n'.format(
                self.network.evaluated_cells
            )
        if check_average_cells_per_sec:
            self.data += 'Nodes per Sec (avg):\t{}\n'.format(
                self.network.evaluated_cells / self.network.timeline
            )
        if check_cells_per_tick:
            self.data += 'Nodes per Tick:\t{}\n'.format(
                len(self.network._cells)
            )
        self.data += '----------------------------------End Profile'
        if print_profile:
            print(self.data)
        self.done = True


class GESetBoneConstraintInfluence(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.armature = None
        self.bone = None
        self.constraint = None
        self.influence = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        armature = self.get_socket_value(self.armature)
        bone = self.get_socket_value(self.bone)
        constraint = self.get_socket_value(self.constraint)
        influence = self.get_socket_value(self.influence)
        if is_waiting(
            armature,
            bone,
            constraint,
            influence
        ):
            return
        self._set_ready()
        if is_invalid(armature):
            return
        armature.blenderObject.pose.bones[bone].constraints[constraint].influence = influence
        self.done = True


class GESetBoneConstraintTarget(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.armature = None
        self.bone = None
        self.constraint = None
        self.target = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        armature = self.get_socket_value(self.armature)
        bone = self.get_socket_value(self.bone)
        constraint = self.get_socket_value(self.constraint)
        target = self.get_socket_value(self.target)
        if is_waiting(
            armature,
            bone,
            constraint,
            target
        ):
            return
        self._set_ready()
        if is_invalid(armature):
            return
        armature.blenderObject.pose.bones[bone].constraints[constraint].target = target.blenderObject
        self.done = True


class GESetBoneConstraintAttribute(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.armature = None
        self.bone = None
        self.constraint = None
        self.attribute = None
        self.value = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        armature = self.get_socket_value(self.armature)
        bone = self.get_socket_value(self.bone)
        constraint = self.get_socket_value(self.constraint)
        attribute = self.get_socket_value(self.attribute)
        value = self.get_socket_value(self.value)
        if is_waiting(
            armature,
            bone,
            constraint,
            attribute,
            value
        ):
            return
        self._set_ready()
        if is_invalid(armature):
            return
        setattr(armature.blenderObject.pose.bones[bone].constraints[constraint], attribute, value)
        self.done = True


class ActionEditBone(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.armature = None
        self.bone_name = None
        self.set_translation = None
        self.set_orientation = None
        self.set_scale = None
        self.translate = None
        self.rotate = None
        self.scale = None
        self._eulers = Euler((0, 0, 0), "XYZ")
        self._vector = Vector((0, 0, 0))
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def _convert_orientation(self, ch, xyzrot):
        eulers = self._eulers
        eulers[:] = xyzrot
        if ch.rotation_mode is logic.ROT_MODE_QUAT:
            return eulers.to_quaternion()
        else:
            return xyzrot

    def _set_orientation(self, ch, rot):
        orientation = self._convert_orientation(ch, rot)
        if ch.rotation_mode is logic.ROT_MODE_QUAT:
            ch.rotation_quaternion = orientation
        else:
            ch.rotation_euler = orientation

    def _rotate(self, ch, xyzrot):
        orientation = self._convert_orientation(ch, xyzrot)
        if ch.rotation_mode is logic.ROT_MODE_QUAT:
            ch.rotation_quaternion = (
                Quaternion(ch.rotation_quaternion) * orientation
            )
        else:
            ch.rotation_euler = ch.rotation_euler.rotate(orientation)

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        armature = self.get_socket_value(self.armature)
        bone_name = self.get_socket_value(self.bone_name)
        set_translation = self.get_socket_value(self.set_translation)
        set_orientation = self.get_socket_value(self.set_orientation)
        set_scale = self.get_socket_value(self.set_scale)
        translate = self.get_socket_value(self.translate)
        rotate = self.get_socket_value(self.rotate)
        scale = self.get_socket_value(self.scale)
        if is_waiting(
            armature,
            bone_name,
            set_translation,
            set_orientation,
            set_scale,
            translate,
            rotate,
            scale
        ):
            return
        self._set_ready()
        if is_invalid(armature):
            return
        if not bone_name:
            return
        # TODO cache the bone index
        bone_channel = armature.channels[bone_name]
        if set_translation is not None:
            bone_channel.location = set_translation
        if set_orientation is not None:
            self._set_orientation(bone_channel, set_orientation)
        if set_scale is not None:
            bone_channel.scale = set_scale
        if translate is not None:
            vec = self._vector
            vec[:] = translate
            bone_channel.location = bone_channel.location + vec
        if scale is not None:
            vec = self._vector
            vec[:] = scale
            bone_channel.scale = bone_channel.scale + vec
        if rotate is not None:
            self._rotate(bone_channel, rotate)
        armature.update()
        self.done = True


class ActionSetBonePos(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.armature = None
        self.bone_name = None
        self.set_translation = None
        self._eulers = Euler((0, 0, 0), "XYZ")
        self._vector = Vector((0, 0, 0))
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        armature = self.get_socket_value(self.armature)
        bone_name = self.get_socket_value(self.bone_name)
        set_translation = self.get_socket_value(self.set_translation)
        self._set_ready()
        if is_invalid(armature, bone_name, set_translation):
            return
        if not bone_name:
            return
        # TODO cache the bone index
        bone_channel = armature.channels[bone_name]
        if set_translation is not None:
            bone_channel.location = set_translation
        else:
            debug('Set Bone Node: Position is None!')
        armature.update()
        self.done = True


class ActionTimeFilter(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.delay = None
        self._triggered = False
        self._triggered_time = None
        self._trigger_delay = None

    def evaluate(self):
        if self._triggered is True:
            self._set_ready()
            delta = self.network.timeline - self._triggered_time
            if delta < self._trigger_delay:
                self._set_value(False)
                return
        condition = self.get_socket_value(self.condition)
        delay = self.get_socket_value(self.delay)
        if is_waiting(condition, delay):
            return
        self._set_ready()
        self._set_value(False)
        if delay is None:
            return
        if condition is None:
            return
        if condition:
            self._triggered = True
            self._triggered_time = self.network.timeline
            self._trigger_delay = delay
            self._set_value(True)


class GEBarrier(GEActionNode):
    consumed: bool
    trigger: float

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.time = None
        self.consumed = False
        self.trigger = 0

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        time = self.get_socket_value(self.time)
        if is_waiting(time):
            return

        self._set_ready()

        now = self.network.timeline

        if not not_met(condition):
            if not self.consumed:
                self.consumed = True
                self.trigger = now + time

            if now >= self.trigger:
                self._set_value(True)

        else:
            self._set_value(False)
            self.consumed = False


class ActionTimeDelay(GEActionNode):
    consumed: bool
    triggers: list

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.delay = None
        self.triggers = []

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        delay = self.get_socket_value(self.delay)
        if is_invalid(delay):
            return
        self._set_ready()

        now = self.network.timeline

        if not not_met(condition):
            self.triggers.append(now + delay)

        if not self.triggers:
            self._set_value(False)
            return
        t = self.triggers[0]
        if now >= t:
            self._set_value(True)
            self.triggers.remove(t)
            return
        self._set_value(False)


class ActionSetDynamics(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.activate = False
        self.ghost = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        ghost = self.get_socket_value(self.ghost)
        activate = self.get_socket_value(self.activate)
        if is_waiting(game_object, ghost, activate):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if activate:
            game_object.restoreDynamics()
        else:
            game_object.suspendDynamics(ghost)
        self.done = True


class ActionSetPhysics(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.activate = False
        self.free_const = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        activate = self.get_socket_value(self.activate)
        free_const = self.get_socket_value(self.free_const)
        if is_waiting(game_object, free_const, activate):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if activate:
            game_object.restorePhysics()
        else:
            game_object.suspendPhysics(free_const)
        self.done = True


class ActionSetRigidBody(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.activate = False
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        activate = self.get_socket_value(self.activate)
        if is_waiting(game_object, activate):
            return
        if is_invalid(game_object):
            return
        self._set_ready()
        if activate:
            game_object.enableRigidBody()
        else:
            game_object.disableRigidBody()
        self.done = True


class ActionEndObject(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.scene = None
        self.game_object = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        game_object = self.get_socket_value(self.game_object)
        if not_met(condition):
            return
        if is_waiting(game_object):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if game_object is self.network._owner:
            self.network._do_remove = True
        game_object.endObject()
        self.done = True


class ActionSetTimeScale(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.scene = None
        self.timescale = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        timescale = self.get_socket_value(self.timescale)
        if is_waiting(timescale):
            return
        self._set_ready()
        if is_invalid(timescale):
            return
        logic.setTimeScale(timescale)
        self.done = True


class ActionSetGravity(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.scene = None
        self.gravity = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        gravity = self.get_socket_value(self.gravity)
        if is_waiting(gravity):
            return
        self._set_ready()
        if is_invalid(gravity):
            return
        logic.setGravity(gravity)
        self.done = True


class ActionApplyGameObjectValue(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.movement = None
        self.rotation = None
        self.force = None
        self.torque = None
        self.local = False

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        if is_waiting(game_object):
            return
        movement = self.get_socket_value(self.movement)
        rotation = self.get_socket_value(self.rotation)
        force = self.get_socket_value(self.force)
        torque = self.get_socket_value(self.torque)
        local = self.local
        if is_waiting(movement, rotation, force, torque, local):
            return
        self._set_ready()
        if not condition:
            return
        if is_invalid(game_object):
            return
        if movement:
            game_object.applyMovement(movement, local)
        if rotation:
            if len(rotation) == 3:
                game_object.applyRotation(rotation, local)
            else:
                game_object.applyRotation(rotation.to_euler("XYZ"), local)
        if force:
            game_object.applyForce(force, local)
        if torque:
            game_object.applyTorque(torque, local)


class ActionApplyLocation(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.movement = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        movement = self.get_socket_value(self.movement)
        local = self.local
        if is_waiting(game_object, movement, local):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if movement:
            game_object.applyMovement(movement, local)
        self.done = True


class ActionApplyRotation(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.rotation = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        rotation = self.get_socket_value(self.rotation)
        local = self.local
        if is_waiting(game_object, rotation, local):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if rotation:
            if len(rotation) == 3:
                game_object.applyRotation(rotation, local)
            else:
                game_object.applyRotation(rotation.to_euler("XYZ"), local)
        self.done = True


class ActionApplyForce(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.force = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        force = self.get_socket_value(self.force)
        local = self.local
        if is_waiting(game_object, force):
            return
        self._set_ready()
        game_object.applyForce(force, local)
        self.done = True


class ActionApplyImpulse(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.point = None
        self.impulse = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        point = self.get_socket_value(self.point)
        impulse = self.get_socket_value(self.impulse)
        local = self.local
        if hasattr(point, 'worldPosition'):
            point = point.worldPosition
        if is_waiting(point, impulse) or is_invalid(game_object):
            return
        self._set_ready()
        if impulse:
            game_object.applyImpulse(point, impulse, local)
        self.done = True


class GamepadLook(GEActionNode):
    def __init__(self, axis=0):
        GEActionNode.__init__(self)
        self.axis: int = axis
        self.condition = None
        self.main_obj: GameObject = None
        self.head_obj: GameObject = None
        self.inverted: bool = None
        self.index: int = None
        self.sensitivity: float = None
        self.exponent: float = None
        self.use_cap_x: bool = None
        self.cap_x: Vector = None
        self.use_cap_y: bool = None
        self.cap_y: Vector = None
        self.threshold: float = None
        self.done: bool = None
        self.DONE = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        axis: int = self.get_socket_value(self.axis)
        condition: GameObject = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        main_obj: GameObject = self.get_socket_value(self.main_obj)
        head_obj: GameObject = self.get_socket_value(self.head_obj)
        if is_invalid(head_obj):
            head_obj = main_obj
        if is_invalid(axis):
            debug('Gamepad Sticks Node: Invalid Controller Stick!')
            return
        inverted: bool = self.get_socket_value(self.inverted)
        index: int = self.get_socket_value(self.index)
        sensitivity: float = self.get_socket_value(self.sensitivity)
        exponent: float = self.get_socket_value(self.exponent)
        threshold: float = self.get_socket_value(self.threshold)
        use_cap_x: Vector = self.get_socket_value(self.use_cap_x)
        cap_x: Vector = self.get_socket_value(self.cap_x)
        uppercapX: float = cap_x.x
        lowercapX: float = -cap_x.y
        use_cap_y: Vector = self.get_socket_value(self.use_cap_y)
        cap_y: Vector = self.get_socket_value(self.cap_y)
        uppercapY: float = cap_y.x
        lowercapY: float = -cap_y.y

        self._set_ready()
        if logic.joysticks[index]:
            joystick = logic.joysticks[index]
        else:
            debug('Gamepad Sticks Node: No Joystick at that Index!')
            return
        if is_invalid(joystick):
            return
        raw_values = joystick.axisValues
        if axis == 0:
            x, y = raw_values[0] , raw_values[1]
        elif axis == 1:
            x, y = raw_values[2], raw_values[3]
        neg_x = -1 if x < 0 else 1
        neg_y = -1 if y < 0 else 1

        if -threshold < x < threshold:
            x = 0
        else:
            x = abs(x) ** exponent

        if -threshold < y < threshold:
            y = 0
        else:
            y = abs(y) ** exponent
        if x == y == 0:
            self.done = True
            return

        x *= neg_x
        y *= neg_y

        x = -x if inverted['x'] else x
        y = -y if inverted['y'] else y

        x *= sensitivity
        if use_cap_x:
            objectRotation = main_obj.localOrientation.to_euler()
            if objectRotation.z + x > uppercapX:
                x = 0
                objectRotation.z = uppercapX
                main_obj.localOrientation = objectRotation.to_matrix()

            if objectRotation.z + x < lowercapX:
                x = 0
                objectRotation.z = lowercapX
                main_obj.localOrientation = objectRotation.to_matrix()

        y *= sensitivity
        if use_cap_y:
            objectRotation = head_obj.localOrientation.to_euler()
            if objectRotation.y + y > uppercapY:
                y = 0
                objectRotation.y = uppercapY
                head_obj.localOrientation = objectRotation.to_matrix()

            if objectRotation.y + y < lowercapY:
                y = 0
                objectRotation.y = lowercapY
                head_obj.localOrientation = objectRotation.to_matrix()

        main_obj.applyRotation(Vector((0, 0, x)), True)
        head_obj.applyRotation(Vector((0, y, 0)), True)
        self.done = True


class ActionCharacterJump(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        if is_waiting(game_object):
            return
        physics = bge.constraints.getCharacter(game_object)
        self._set_ready()
        if is_invalid(game_object):
            return
        physics.jump()

        self.done = True


class SetCharacterJumpSpeed(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.force = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        force = self.get_socket_value(self.force)
        if is_waiting(game_object):
            return
        physics = bge.constraints.getCharacter(game_object)
        self._set_ready()
        if is_invalid(game_object):
            return
        physics.jumpSpeed = force
        self.done = True


class SetCollisionGroup(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.slots = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        slots = self.get_socket_value(self.slots)
        if is_waiting(game_object, slots):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        game_object.collisionGroup = slots

        self.done = True


class SetCollisionMask(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.slots = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        slots = self.get_socket_value(self.slots)
        if is_waiting(game_object, slots):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        game_object.collisionMask = slots

        self.done = True


class ActionSaveVariable(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.name = None
        self.val = None
        self.path = ''
        self.file_name = ''
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def write_to_json(self, path, name, val):
        data = None
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if os.path.isfile(path):
            f = open(path, 'r')
            data = json.load(f)
            data[name] = val
            f.close()
            f = open(path, 'w')
            json.dump(data, f, indent=2)
        else:
            debug('Variable file does not exist - creating...')
            f = open(path, 'w')
            data = {name: val}
            json.dump(data, f, indent=2)
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        name = self.get_socket_value(self.name)
        val = self.get_socket_value(self.val)
        if is_waiting(name, val):
            return
        self._set_ready()

        cust_path = self.get_custom_path(self.path)
        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )

        os.makedirs(path, exist_ok=True)

        self.write_to_json(path, name, val)
        self.done = True


class ActionSaveVariables(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.val = None
        self.path = ''
        self.file_name = ''
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def write_to_json(self, path, val):
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if os.path.isfile(path):
            f = open(path, 'w')
            json.dump(val, f, indent=2)
        else:
            debug('file does not exist - creating...')
            f = open(path, 'w')
            json.dump(val, f, indent=2)
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        val = self.get_socket_value(self.val)
        if is_waiting(val):
            return
        self._set_ready()

        cust_path = self.get_custom_path(self.path)
        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.write_to_json(path, val)
        self.done = True


class ActionLoadVariable(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.name = None
        self.path = ''
        self.file_name = ''
        self.var = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.VAR = GEOutSocket(self, self.get_var)

    def get_done(self):
        return self.done

    def get_var(self):
        return self.var

    def read_from_json(self, path, name):
        self.done = False
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if path:
            f = open(path, 'r')
            data = json.load(f)
            if name not in data:
                debug('"{}" is not a saved Variabe!')
            self.var = data[name]
            f.close()
        else:
            debug('No saved variables!')

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        name = self.get_socket_value(self.name)
        if is_waiting(name):
            return
        self._set_ready()
        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.read_from_json(path, name)
        self.done = True


class ActionLoadVariables(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.path = ''
        self.file_name = ''
        self.var = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.VAR = GEOutSocket(self, self.get_var)

    def get_done(self):
        return self.done

    def get_var(self):
        return self.var

    def read_from_json(self, path):
        self.done = False
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if not os.path.isfile(path):
            debug('No Saved Variables!')
            return
        f = open(path, 'r')
        data = json.load(f)
        self.var = data
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.read_from_json(path)
        self.done = True


class ActionRemoveVariable(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.name = None
        self.path = ''
        self.file_name = ''
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def write_to_json(self, path, name):
        data = None
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if os.path.isfile(path):
            f = open(path, 'r')
            data = json.load(f)
            if name in data:
                del data[name]
            f.close()
            f = open(path, 'w')
            json.dump(data, f, indent=2)
            f.close()
        else:
            debug('File does not exist!')

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        name = self.get_socket_value(self.name)
        if is_waiting(name):
            return
        self._set_ready()

        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.write_to_json(path, name)
        self.done = True


class ActionClearVariables(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.path = ''
        self.file_name = ''
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def write_to_json(self, path):
        data = None
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if os.path.isfile(path):
            data = {}
            f = open(path, 'w')
            json.dump(data, f, indent=2)
        else:
            debug('File does not exist - creating...')
            f = open(path, 'w')
            data = {}
            json.dump(data, f, indent=2)
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        self._set_ready()
        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.write_to_json(path)
        self.done = True


class ActionListVariables(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.print_list = None
        self.path = ''
        self.file_name = ''
        self.done = None
        self.items = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.LIST = GEOutSocket(self, self.get_list)

    def get_done(self):
        return self.done

    def get_list(self):
        return self.items

    def write_to_json(self, path, p_l):
        data = None
        if not path.endswith('.json'):
            path = path + f'{self.file_name}.json'
        if os.path.isfile(path):
            f = open(path, 'r')
            data = json.load(f)
            if len(data) == 0:
                debug('There are no saved variables')
                return
            li = []
            for x in data:
                if p_l:
                    print('{}\t->\t{}'.format(x, data[x]))
                li.append(x)
            self.items = li
        else:
            debug('There are no saved variables')
        f.close()

    def get_custom_path(self, path):
        if not path.endswith('/') and not path.endswith('json'):
            path = path + '/'
        return path

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        print_list = self.get_socket_value(self.print_list)
        if is_waiting(print_list):
            return
        self._set_ready()
        cust_path = self.get_custom_path(self.path)

        path = (
            bpy.path.abspath('//Data/')
            if self.path == ''
            else bpy.path.abspath(cust_path)
        )
        os.makedirs(path, exist_ok=True)

        self.write_to_json(path, print_list)
        self.done = True


class ActionSetCharacterJump(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.max_jumps = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        max_jumps = self.get_socket_value(self.max_jumps)
        if is_waiting(game_object, max_jumps):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        physics = bge.constraints.getCharacter(game_object)
        physics.maxJumps = max_jumps
        self.done = True


class ActionSetCharacterGravity(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.gravity = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        gravity = self.get_socket_value(self.gravity)
        if is_waiting(gravity):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        physics = bge.constraints.getCharacter(game_object)
        if physics:
            physics.gravity = gravity
        else:
            game_object.gravity = gravity
        self.done = True


class ActionSetCharacterWalkDir(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.walkDir = None
        self.local = False
        self.active = False
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            if self.active:
                game_object = self.get_socket_value(self.game_object)
                physics = bge.constraints.getCharacter(game_object)
                physics.walkDirection = Vector((0, 0, 0))
                self.active = False
            return
        elif not self.active:
            self.active = True
        game_object = self.get_socket_value(self.game_object)
        local = self.local
        walkDir = self.get_socket_value(self.walkDir)
        if is_waiting(game_object, local, walkDir):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if local:
            walkDir = game_object.worldOrientation @ walkDir
        physics = bge.constraints.getCharacter(game_object)
        physics.walkDirection = walkDir / bpy.data.scenes[bge.logic.getCurrentScene().name].game_settings.physics_step_sub
        self.done = True


class ActionSetCharacterVelocity(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.vel = None
        self.time = None
        self.local = False
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        if is_waiting(game_object):
            return
        local = self.local
        physics = bge.constraints.getCharacter(game_object)
        vel = self.get_socket_value(self.vel)
        time = self.get_socket_value(self.time)
        self._set_ready()
        if is_invalid(game_object):
            return
        physics.setVelocity(vel, time, local)
        self.done = True


class ParameterGetCharacterInfo(GEParameterNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.game_object = None
        self.max_jumps = None
        self.cur_jump = None
        self.gravity = None
        self.walk_dir = None
        self.on_ground = None
        self.local = False
        self.MAX_JUMPS = GEOutSocket(self, self.get_max_jumps)
        self.CUR_JUMP = GEOutSocket(self, self.get_current_jump)
        self.GRAVITY = GEOutSocket(self, self.get_gravity)
        self.WALKDIR = GEOutSocket(self, self.get_walk_dir)
        self.ON_GROUND = GEOutSocket(self, self.get_on_ground)

    def get_max_jumps(self):
        return self.max_jumps

    def get_current_jump(self):
        return self.cur_jump

    def get_gravity(self):
        return self.gravity

    def get_walk_dir(self):
        return self.walk_dir

    def get_on_ground(self):
        return self.on_ground

    def evaluate(self):
        game_object = self.get_socket_value(self.game_object)
        if is_invalid(game_object):
            return
        physics = bge.constraints.getCharacter(game_object)
        local = self.local
        self._set_ready()
        self.max_jumps = physics.maxJumps
        self.cur_jump = physics.jumpCount
        self.gravity = physics.gravity
        self.walk_dir = physics.walkDirection @ game_object.worldOrientation if local else physics.walkDirection
        self.on_ground = physics.onGround



class ActionApplyTorque(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.torque = None
        self.local = False
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        torque = self.get_socket_value(self.torque)
        local = self.local
        if is_waiting(game_object, torque):
            return
        self._set_ready()
        if torque:
            game_object.applyTorque(torque, local)
        self.done = True


class ActionPlayAction(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.action_name = None
        self.stop = None
        self.frames = None
        self.start_frame = None
        self.end_frame = None
        self.layer = None
        self.priority = None
        self.play_mode = None
        self.layer_weight = None
        self.old_layer_weight = None
        self.speed = None
        self.old_speed = None
        self.blendin = None
        self.blend_mode = None
        self._started = False
        self._running = False
        self._finished = False
        self._frame = 0.0
        self._finish_notified = False
        self.STARTED = GEOutSocket(self, self._get_started)
        self.FINISHED = GEOutSocket(self, self._get_finished)
        self.RUNNING = GEOutSocket(self, self._get_running)
        self.FRAME = GEOutSocket(self, self._get_frame)

    def _get_started(self):
        return self._started

    def _get_finished(self):
        return self._finished

    def _get_running(self):
        return self._running

    def _get_frame(self):
        return self._frame

    def _reset_subvalues(self):
        self._started = False
        self._finished = False
        self._running = False
        self._frame = 0.0
        self._finish_notified = False

    def _notify_finished(self, obj, layer):
        if not self._finish_notified and self.stop:
            self._finish_notified = True
            self._finished = True
            obj.stopAction(layer)
        else:
            self._finished = False

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        game_object = self.get_socket_value(self.game_object)
        action_name = self.get_socket_value(self.action_name)
        start_frame = self.get_socket_value(self.start_frame)
        end_frame = self.get_socket_value(self.end_frame)
        layer = self.get_socket_value(self.layer)
        priority = self.get_socket_value(self.priority)
        play_mode = self.get_socket_value(self.play_mode)
        layer_weight = self.get_socket_value(self.layer_weight)
        speed = self.get_socket_value(self.speed)
        blendin = self.get_socket_value(self.blendin)
        blend_mode = self.get_socket_value(self.blend_mode)
        if is_invalid(
            game_object,
            action_name,
            start_frame,
            end_frame,
            layer,
            priority,
            play_mode,
            layer_weight,
            speed,
            blendin,
            blend_mode
        ):
            return
        if play_mode > 2:
            if not_met(condition):
                self._notify_finished(game_object, layer)
                return
            else:
                play_mode -= 3
        if layer_weight <= 0:
            layer_weight = 0.0
        elif layer_weight >= 1:
            layer_weight = 1.0
        if speed <= 0:
            speed = 0.01
        self._set_ready()
        if is_invalid(game_object):  # can't play
            debug("Play Action Node: Invalid Game Object!")
            self._reset_subvalues()
        else:
            # Condition might be false and the animation running
            # because it was started in a previous evaluation
            playing_action = game_object.getActionName(layer)
            playing_frame = game_object.getActionFrame(layer)
            min_frame = start_frame
            max_frame = end_frame
            if end_frame < start_frame:
                min_frame = end_frame
                max_frame = max_frame
            if (
                (playing_action == action_name) and
                (playing_frame >= min_frame) and
                (playing_frame <= max_frame)
            ):
                self._started = False
                self._running = True
                is_near_end = False
                self._frame = playing_frame
                if (
                    layer_weight != self.old_layer_weight or
                    speed != self.old_speed
                ):
                    reset_frame = start_frame if play_mode == bge.logic.KX_ACTION_MODE_LOOP else end_frame
                    next_frame = (
                        playing_frame + speed
                        if
                        playing_frame + speed <= end_frame
                        else
                        reset_frame
                    )
                    game_object.stopAction(layer)
                    game_object.playAction(
                        action_name,
                        start_frame,
                        end_frame,
                        layer=layer,
                        priority=priority,
                        blendin=blendin,
                        play_mode=play_mode,
                        speed=speed,
                        layer_weight=1 - layer_weight,
                        blend_mode=blend_mode)
                    game_object.setActionFrame(next_frame, layer)
                # TODO: the meaning of start-end depends
                # also on the action mode
                if end_frame > start_frame:  # play 0 to 100
                    is_near_end = (playing_frame >= (end_frame - 0.5))
                else:  # play 100 to 0
                    is_near_end = (playing_frame <= (end_frame + 0.5))
                if is_near_end:
                    self._notify_finished(game_object, layer)
            elif condition:  # start the animation if the condition is True
                is_playing = game_object.isPlayingAction(layer)
                same_action = game_object.getActionName(layer) == action_name
                if not same_action and is_playing:
                    game_object.stopAction(layer)
                if not (is_playing or same_action):
                    game_object.playAction(
                        action_name,
                        start_frame,
                        end_frame,
                        layer=layer,
                        priority=priority,
                        blendin=blendin,
                        play_mode=play_mode,
                        speed=speed,
                        layer_weight=1-layer_weight,
                        blend_mode=blend_mode)
                    self._started = True
                    self._frame = start_frame
                self._running = True
                self._finished = False
                self._finish_notified = False
            else:  # game_object is existing and valid but condition is False
                self._reset_subvalues()
        self.old_layer_weight = layer_weight
        self.old_speed = speed


class ActionStopAnimation(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.action_layer = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not condition:
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        action_layer = self.get_socket_value(self.action_layer)
        if is_waiting(game_object, action_layer):
            return
        self._set_ready()
        if is_invalid(game_object):
            return
        if is_invalid(action_layer):
            return
        game_object.stopAction(action_layer)
        self.done = True


class ActionSetAnimationFrame(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.action_layer = None
        self.action_frame = None
        self.freeze = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not condition:
            self._set_ready()
            return
        game_object = self.get_socket_value(self.game_object)
        action_layer = self.get_socket_value(self.action_layer)
        action_frame = self.get_socket_value(self.action_frame)
        freeze = self.get_socket_value(self.freeze)
        action_name = self.get_socket_value(self.action_name)
        layer_weight = self.get_socket_value(self.layer_weight)
        self._set_ready()
        if is_invalid(
            game_object,
            action_layer,
            action_frame,
            layer_weight
        ):
            debug('Set Animation Frame Node: Invalid Parameters!')
            return
        is_playing = game_object.isPlayingAction(action_layer)
        same_action = game_object.getActionName(action_layer) == action_name
        action = bpy.data.actions[action_name]
        start_frame = action.frame_range[0]
        end_frame = action.frame_range[1]
        finished = game_object.getActionFrame(action_layer) >= end_frame
        if not (is_playing or same_action) or finished:
            game_object.stopAction(action_layer)
            speed = .000000000000000001 if freeze else 1
            game_object.playAction(
                action_name,
                start_frame,
                end_frame,
                action_layer,
                layer_weight=1-layer_weight,
                speed=speed
            )
        game_object.setActionFrame(action_frame, action_layer)
        self.done = True


class ActionFindScene(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.query = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def has_status(self, status):
        found_scene = self.get_value()
        if (
            (self.condition is None) and
            (found_scene is not None) and
            (not found_scene.invalid) and
            (found_scene is not None)
        ):
            return status is STATUS_READY
        else:
            return GEActionNode.has_status(self, status)

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        query = self.get_socket_value(self.query)
        if is_waiting(query):
            return
        self._set_ready()
        if self.condition is None:
            scene = _name_query(logic.getSceneList(), query)
            self._set_value(scene)
        scene = _name_query(logic.getSceneList(), query)
        self._set_value(scene)
        self.done = True


class ActionStart3DSoundAdv(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.sound = None
        self.occlusion = None
        self.transition = None
        self.cutoff = None
        self.speaker = None
        self.device = None
        self.loop_count = None
        self.pitch = None
        self.volume = None
        self.attenuation = None
        self.distance_ref = None
        self.cone_angle = None
        self.cone_outer_volume = None
        self.done = None
        self.on_finish = False
        self._clear_sound = 1
        self._sustained = 1
        self._handle = None
        self._handles = {}
        self.DONE = GEOutSocket(self, self.get_done)
        self.ON_FINISH = GEOutSocket(self, self.get_on_finish)
        self.HANDLE = GEOutSocket(self, self.get_handle)

    def get_handle(self):
        return self._handle

    def get_on_finish(self):
        return self.on_finish

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        self.on_finish = False
        audio_system = self.network.audio_system
        speaker = self.get_socket_value(self.speaker)
        handles = self._handles
        occlusion = self.get_socket_value(self.occlusion)
        volume = self.get_socket_value(self.volume)
        cone_outer_volume = self.get_socket_value(self.cone_outer_volume)
        pitch = self.get_socket_value(self.pitch) * logic.getTimeScale()
        attenuation = self.get_socket_value(self.attenuation)
        to_remove = []
        for i, sound in enumerate(handles):
            if not handles[sound][1]:
                to_remove.append(sound)
            for handle in handles[sound][1]:
                if len(handles[sound][1]) <= i:
                    continue
                if handle.status:
                    self._set_ready()
                    handle.pitch = pitch
                    hspeaker = handles[sound][0]
                    handle.location = hspeaker.worldPosition
                    handle.orientation = (
                        hspeaker
                        .worldOrientation
                        .to_quaternion()
                    )
                    if hspeaker.mass:
                        handle.velocity = getattr(
                            hspeaker,
                            'worldLinearVelocity',
                            Vector((0, 0, 0))
                        )
                    if occlusion:
                        transition = self.get_socket_value(
                            self.transition
                        )
                        cam = bge.logic.getCurrentScene().active_camera
                        occluder, point, normal = cam.rayCast(
                            hspeaker.worldPosition,
                            cam.worldPosition,
                            compute_distance(hspeaker, cam),
                            xray=False
                        )
                        occluded = False
                        penetration = 1
                        while occluder:
                            if occluder is hspeaker:
                                break
                            sound_occluder = occluder.blenderObject.get(
                                'sound_occluder',
                                True
                            )
                            if sound_occluder:
                                occluded = True
                                block = occluder.blenderObject.get(
                                    'sound_blocking',
                                    .1
                                )
                                if penetration > 0:
                                    penetration -= block
                                else:
                                    penetration = 0
                                # attenuation *= 1 + block / 2
                            occluder, point, normal = occluder.rayCast(
                                speaker.worldPosition,
                                point,
                                compute_distance(speaker, point),
                                xray=False
                            )
                        cs = self._clear_sound
                        if occluded and cs > 0:
                            self._clear_sound -= transition
                        elif not occluded and cs < 1:
                            self._clear_sound += transition
                        if self._clear_sound < 0:
                            self._clear_sound = 0
                        sustained = self._sustained
                        if sustained > penetration:
                            self._sustained -= transition / 10
                        elif sustained < penetration:
                            self._sustained += transition / 10
                        mult = (
                            cs * sustained
                            if not i
                            else (1 - cs) * sustained
                        )
                        # handles[sound][ind].attenuation = attenuation
                        handles[sound][1][i].volume = volume * mult
                        handles[sound][1][i].cone_volume_outer = (
                            cone_outer_volume *
                            volume *
                            mult
                        )
                    else:
                        handles[sound][1][i].volume = volume
                        handles[sound][1][i].cone_volume_outer = (
                            cone_outer_volume *
                            volume
                        )
                elif handle in audio_system.active_sounds:
                    for handle in handles[sound][1]:
                        audio_system.active_sounds.remove(handle)
                        handles[sound][1].remove(handle)
                    continue
        else:
            self._handle = None
        for sound in to_remove:
            self.on_finish = True
            self._handles.pop(sound)
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        if not self.device:
            self.device = audio_system.device
        cutoff = self.get_socket_value(self.cutoff)
        sound = self.get_socket_value(self.sound)
        loop_count = self.get_socket_value(self.loop_count)
        distance_ref = self.get_socket_value(self.distance_ref)
        cone_angle = self.get_socket_value(self.cone_angle)
        cone_inner_angle = cone_angle.x
        cone_outer_angle = cone_angle.y
        self._set_ready()

        if is_invalid(sound):
            return
        soundpath = logic.expandPath(sound)
        soundfile = aud.Sound(soundpath)
        handle = self._handle = self.device.play(soundfile)
        if occlusion:
            soundlow = aud.Sound.lowpass(soundfile, 4000*cutoff, .5)
            handlelow = self.device.play(soundlow)
            self._handles[soundfile] = [speaker, [handle, handlelow]]
        else:
            self._handles[soundfile] = [speaker, [handle]]
        for handle in self._handles[soundfile][1]:
            handle.relative = False
            handle.location = speaker.worldPosition
            if speaker.mass:
                handle.velocity = getattr(
                    speaker,
                    'worldLinearVelocity',
                    Vector((0, 0, 0))
                )
            handle.attenuation = attenuation
            handle.orientation = speaker.worldOrientation.to_quaternion()
            handle.pitch = pitch
            handle.loop_count = loop_count
            handle.volume = volume
            handle.distance_reference = distance_ref
            handle.distance_maximum = 1000
            handle.cone_angle_inner = cone_inner_angle
            handle.cone_angle_outer = cone_outer_angle
            handle.cone_volume_outer = cone_outer_volume * volume
            audio_system.active_sounds.append(handle)
        self.done = True


class ActionStartSound(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.sound = None
        self.loop_count = None
        self.pitch = None
        self.volume = None
        self.done = None
        self.device = None
        self.on_finish = False
        self._handle = None
        self._handles = []
        self.DONE = GEOutSocket(self, self.get_done)
        self.ON_FINISH = GEOutSocket(self, self.get_on_finish)
        self.HANDLE = GEOutSocket(self, self.get_handle)

    def get_handle(self):
        return self._handle

    def get_on_finish(self):
        return self.on_finish

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        self.on_finish = False
        audio_system = self.network.audio_system
        if not self.device:
            self.device = audio_system.device
        handles = self._handles
        pitch = self.get_socket_value(self.pitch)
        volume = self.get_socket_value(self.volume)
        self._set_ready()
        if handles:
            for handle in handles:
                if not handle.status and handle in audio_system.active_sounds:
                    self._handles.remove(handle)
                    audio_system.active_sounds.remove(handle)
                    self.on_finish = True
                    return
                handle.volume = volume
                handle.pitch = pitch
            if handles:
                self._handle = handles[-1]
            else:
                self._handle = None
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        sound = self.get_socket_value(self.sound)
        loop_count = self.get_socket_value(self.loop_count)
        #  self._set_ready()

        if is_invalid(sound):
            return
        soundpath = bge.logic.expandPath(sound)
        soundfile = aud.Sound(soundpath)
        handle = self.device.play(soundfile)
        handle.relative = True
        handle.pitch = pitch
        handle.loop_count = loop_count
        handle.volume = volume
        audio_system.active_sounds.append(handle)
        self._handles.append(handle)
        self._handle = handle
        self.done = True


class ActionStopSound(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.sound = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        sound = self.get_socket_value(self.sound)
        if is_waiting(sound):
            return
        self._set_ready()
        if sound is None:
            return
        sound.stop()


class ActionStopAllSounds(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        if not hasattr(bpy.types.Scene, 'nl_aud_system'):
            debug('No Audio System to close.')
            return
        self._set_ready()
        bpy.types.Scene.nl_aud_system.device.stopAll()


class ActionPauseSound(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.sound = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        sound = self.get_socket_value(self.sound)
        if is_waiting(sound):
            return
        self._set_ready()
        if sound is None:
            return
        sound.pause()


class ActionResumeSound(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.sound = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        sound = self.get_socket_value(self.sound)
        if is_waiting(sound):
            return
        self._set_ready()
        if sound is None:
            return
        sound.resume()


class ParameterGetGlobalValue(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.data_id = None
        self.key = None
        self.default = None

    def evaluate(self):
        data_id = self.get_socket_value(self.data_id)
        key = self.get_socket_value(self.key)
        default = self.get_socket_value(self.default)
        if isinstance(default, Invalid):
            default = None
        if is_waiting(data_id, key, default):
            return
        self._set_ready()
        db = GlobalDB.retrieve(data_id)
        self._set_value(db.get(key, default))


class ActionListGlobalValues(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.condition = None
        self.data_id = None
        self.print_d = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        data_id = self.get_socket_value(self.data_id)
        print_d = self.get_socket_value(self.print_d)
        if is_waiting(data_id, print_d):
            return
        self._set_ready()
        db = GlobalDB.retrieve(data_id)
        if print_d:
            print(f'[Logic Nodes] Global category "{data_id}":')
            for e in db.data:
                print('{}\t->\t{}'.format(e, db.data[e]))
            print('END ------------------------------------')
        self._set_value(db.data)


class ParameterFormattedString(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.format_string = None
        self.value_a = None
        self.value_b = None
        self.value_c = None
        self.value_d = None

    def evaluate(self):
        format_string = self.get_socket_value(self.format_string)
        value_a = self.get_socket_value(self.value_a)
        value_b = self.get_socket_value(self.value_b)
        value_c = self.get_socket_value(self.value_c)
        value_d = self.get_socket_value(self.value_d)
        if is_waiting(format_string, value_a, value_b, value_c, value_d):
            return
        self._set_ready()
        if format_string is None:
            return
        result = format_string.format(value_a, value_b, value_c, value_d)
        self._set_value(result)


class ActionSetGlobalValue(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.data_id = None
        self.key = None
        self.value = None
        self.persistent = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        data_id = self.get_socket_value(self.data_id)
        persistent = self.get_socket_value(self.persistent)
        key = self.get_socket_value(self.key)
        value = self.get_socket_value(self.value)
        if is_waiting(data_id, persistent, key, value):
            return
        self._set_ready()
        if self.condition is None or condition:
            if data_id is None:
                return
            if persistent is None:
                return
            if key is None:
                return
            db = GlobalDB.retrieve(data_id)
            db.put(key, value, persistent)
            if self.condition is None:
                self.deactivate()
        self.done = True


class ActionRandomInt(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.max_value = None
        self.min_value = None
        self.OUT_A = GEOutSocket(self, self._get_output)

    def _get_output(self):
        min_value = self.get_socket_value(self.min_value)
        max_value = self.get_socket_value(self.max_value)
        if is_waiting(max_value, min_value):
            return STATUS_WAITING
        if min_value > max_value:
            min_value, max_value = max_value, min_value
        if min_value == max_value:
            min_value = -sys.maxsize
            max_value = sys.maxsize

        return random.randint(min_value, max_value)

    def evaluate(self):
        self._set_ready()


class ActionRandomFloat(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.max_value = None
        self.min_value = None
        self.OUT_A = GEOutSocket(self, self._get_output)

    def _get_output(self):
        min_value = self.get_socket_value(self.min_value)
        max_value = self.get_socket_value(self.max_value)
        if is_waiting(min_value, max_value):
            return STATUS_WAITING
        if min_value > max_value:
            min_value, max_value = max_value, min_value
        if min_value == max_value:
            min_value = sys.float_info.min
            max_value = sys.float_info.max

        delta = max_value - min_value
        return min_value + (delta * random.random())

    def evaluate(self):
        self._set_ready()


class GERandomVect(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.xyz = None
        self.OUT_A = GEOutSocket(self, self._get_output)

    def _get_output(self):
        xyz = self.get_socket_value(self.xyz)
        if is_waiting(xyz):
            return
        vmin, vmax = -999999999, 999999999
        delta = vmax - vmin
        x = vmin + (delta * random.random()) if xyz['x'] else 0
        y = vmin + (delta * random.random()) if xyz['y'] else 0
        z = vmin + (delta * random.random()) if xyz['z'] else 0
        return Vector((x, y, z))

    def evaluate(self):
        self._set_ready()


class ActionTranslate(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.moving_object = None
        self.local = None
        self.vect = None
        self.speed = None
        self._t = None
        self._old_values = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        moving_object = self.get_socket_value(self.moving_object)
        vect = self.get_socket_value(self.vect)
        dx = vect.x
        dy = vect.y
        dz = vect.z
        speed = self.get_socket_value(self.speed)
        local = self.get_socket_value(self.local)
        if is_waiting(
            vect,
            dx,
            dy,
            dz,
            speed,
            local
        ):
            return
        if is_invalid(moving_object):
            return
        self._set_ready()
        if dx is None:
            return
        if dy is None:
            return
        if dz is None:
            return
        if speed is None:
            return
        if local is None:
            return
        new_values = (moving_object, dx, dy, dz, speed, local)
        if new_values != self._old_values:
            start_pos = (
                moving_object.localPosition if
                local else moving_object.worldPosition
            )
            end_pos = Vector((
                start_pos.x + dx, start_pos.y + dy, start_pos.z + dz
            ))
            distance = (start_pos - end_pos).length
            time_to_destination = distance / speed
            t_speed = 1.0 / time_to_destination
            self._old_values = new_values
            self._start_pos = start_pos.copy()
            self._end_pos = end_pos.copy()
            self._d_pos = (end_pos - start_pos)
            self._t_speed = t_speed
            self._t = 0.0
        t = self._t
        dt = self._t_speed * self.network.time_per_frame
        t += dt
        if t >= 1.0:
            self._set_value(True)
            self._t = 0.0
            if local:
                moving_object.localPosition = self._end_pos.copy()
            else:
                moving_object.worldPosition = self._end_pos.copy()
        else:
            npos = self._start_pos + (self._d_pos * t)
            if local:
                moving_object.localPosition = npos
            else:
                moving_object.worldPosition = npos
            self._t = t
            self._set_value(False)


class SetGamma(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[
            scene.name
        ].view_settings.gamma = value
        self.done = True


class SetExposure(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[
            scene.name
        ].view_settings.exposure = value
        self.done = True


class SetEeveeAO(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[scene.name].eevee.use_gtao = value
        self.done = True


class SetEeveeBloom(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[scene.name].eevee.use_bloom = value
        self.done = True


class SetEeveeSSR(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[scene.name].eevee.use_ssr = value
        self.done = True


class SetEeveeVolumetrics(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[
            scene.name
        ].eevee.use_volumetric_lights = value
        self.done = True


class SetEeveeSMAA(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[scene.name].eevee.use_eevee_smaa = value
        self.done = True


class SetEeveeSMAAQuality(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.value = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        value = self.get_socket_value(self.value)
        if is_invalid(value):
            return
        self._set_ready()
        scene = logic.getCurrentScene()
        bpy.data.scenes[scene.name].eevee.use_eevee_smaa = value
        self.done = True


class SetLightEnergy(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.lamp = None
        self.energy = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        lamp = self.get_socket_value(self.lamp)
        energy = self.get_socket_value(self.energy)
        if is_waiting(lamp, energy):
            return
        self._set_ready()
        light = lamp.blenderObject.data
        light.energy = energy
        self.done = True


class GEMakeUniqueLight(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.light = None
        self.done = None
        self._light = None
        self.OUT = GEOutSocket(self, self.get_done)
        self.LIGHT = GEOutSocket(self, self.get_light)

    def get_done(self):
        return self.done

    def get_light(self):
        return self._light

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        old_lamp_ge = self.get_socket_value(self.light)
        if is_waiting(old_lamp_ge):
            return
        self._set_ready()

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
            'size_y'
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
            'shadow_cascade_exponent',
        ]

        types = {
            'POINT': 'Point',
            'AREA': 'Area',
            'SPOT': 'Spot',
            'SUN': 'Sun'
        }

        light_type = old_lamp.data.type
        bpy.ops.object.light_add(type=light_type, location=old_lamp_ge.worldPosition, rotation=old_lamp_ge.worldOrientation.to_euler())
        index = 1
        light = None
        while light is None:
            if types[light_type] in bpy.data.objects[-index].name:
                light = bpy.data.objects[-index]
            index += 1
        for attr in settings:
            try:
                setattr(light.data, attr, getattr(old_lamp.data, attr))
            except:
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

        self.done = True


class SetLightShadow(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.lamp = None
        self.use_shadow = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        lamp = self.get_socket_value(self.lamp)
        use_shadow = self.get_socket_value(self.use_shadow)
        if is_waiting(lamp, use_shadow):
            return
        self._set_ready()
        light = lamp.blenderObject.data
        light.use_shadow = use_shadow
        self.done = True


class SetLightColor(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.lamp = None
        self.color = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_value(False)
            return self._set_ready()
        lamp = self.get_socket_value(self.lamp)
        color = self.get_socket_value(self.color)
        if is_waiting(lamp, color):
            return
        if len(color) > 3:
            color = color[:-1]
        self._set_ready()
        light = lamp.blenderObject.data
        light.color = color
        self.done = True


class GetLightEnergy(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.lamp = None
        self.energy = 0
        self.ENERGY = GEOutSocket(self, self.get_energy)

    def get_energy(self):
        return self.energy

    def evaluate(self):
        lamp = self.get_socket_value(self.lamp)
        if is_waiting(lamp):
            return
        self._set_ready()
        light = lamp.blenderObject.data
        self.energy = light.energy


class GetLightColor(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        self.lamp = None
        self.color = 0
        self.COLOR = GEOutSocket(self, self.get_color)

    def get_color(self):
        return self.color

    def evaluate(self):
        lamp = self.get_socket_value(self.lamp)
        if is_waiting(lamp):
            return
        self._set_ready()
        light = lamp.blenderObject.data
        self.color = light.color


# Action "Move To": an object will follow a point
class ActionMoveTo(GEActionNode):

    def __init__(self):
        GEActionNode.__init__(self)
        # list of parameters of this action
        self.condition = None
        self.moving_object = None
        self.destination_point = None
        self.speed = None
        self.dynamic = None
        self.distance = None

    def evaluate(self):  # the actual execution of this cell
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        moving_object = self.get_socket_value(self.moving_object)
        destination_point = self.get_socket_value(self.destination_point)
        speed = self.get_socket_value(self.speed)
        distance = self.get_socket_value(self.distance)
        dynamic = self.get_socket_value(self.dynamic)
        if hasattr(destination_point, 'worldPosition'):
            destination_point = destination_point.worldPosition
        if is_waiting(
            moving_object,
            destination_point,
            speed,
            distance,
            dynamic
        ):
            return
        self._set_ready()
        self._set_value(move_to(
            moving_object,
            destination_point,
            speed,
            self.network.time_per_frame,
            dynamic,
            distance))


class ActionTrackTo(GEActionNode):
    def __init__(self):
        self.condition = None
        self.moving_object = None
        self.target_object = None
        self.rot_axis = 2
        self.front_axis = 0
        self.speed = 20

    def evaluate(self):
        self._set_value(False)
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return self._set_ready()
        moving_object = self.get_socket_value(self.moving_object)
        target_object = self.get_socket_value(self.target_object)
        speed = self.get_socket_value(self.speed)
        rot_axis = self.get_socket_value(self.rot_axis)
        front_axis = self.get_socket_value(self.front_axis)
        if is_waiting(speed, rot_axis, front_axis):
            return
        if is_invalid(moving_object):
            return
        if is_invalid(target_object):
            return
        self._set_ready()
        if rot_axis is None:
            return
        if front_axis is None:
            return
        if rot_axis == 0:
            self._set_value(
                xrot_to(
                    moving_object,
                    target_object.worldPosition,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )
        elif rot_axis == 1:
            self._set_value(
                yrot_to(
                    moving_object,
                    target_object.worldPosition,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )
        elif rot_axis == 2:
            self._set_value(
                zrot_to(
                    moving_object,
                    target_object.worldPosition,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )


class ActionRotateTo(GEActionNode):
    def __init__(self):
        self.condition = None
        self.moving_object = None
        self.target_point = None
        self.speed = None
        self.rot_axis = 2
        self.front_axis = 0

    def evaluate(self):
        self._set_value(False)
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        moving_object = self.get_socket_value(self.moving_object)
        target_point = self.get_socket_value(self.target_point)
        speed = self.get_socket_value(self.speed)
        if hasattr(target_point, 'worldPosition'):
            target_point = target_point.worldPosition
        rot_axis = self.get_socket_value(self.rot_axis)
        front_axis = self.get_socket_value(self.front_axis)
        if is_waiting(moving_object, target_point, speed, rot_axis, front_axis):
            return
        self._set_ready()
        if rot_axis == 0:
            self._set_value(
                xrot_to(
                    moving_object,
                    target_point,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )
        elif rot_axis == 1:
            self._set_value(
                yrot_to(
                    moving_object,
                    target_point,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )
        elif rot_axis == 2:
            self._set_value(
                zrot_to(
                    moving_object,
                    target_point,
                    front_axis,
                    speed,
                    self.network.time_per_frame
                )
            )


class ActionNavigateWithNavmesh(GEActionNode):

    class MotionPath(object):
        def __init__(self):
            self.points = []
            self.cursor = 0
            self.destination = None

        def next_point(self):
            if self.cursor < len(self.points):
                return self.points[self.cursor]
            else:
                return None

        def destination_changed(self, new_destination):
            return self.destination != new_destination

        def advance(self):
            self.cursor += 1
            return self.cursor < len(self.points)

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.moving_object = None
        self.rotating_object = None
        self.navmesh_object = None
        self.destination_point = None
        self.move_dynamic = None
        self.linear_speed = None
        self.reach_threshold = None
        self.look_at = None
        self.rot_axis = None
        self.front_axis = None
        self.rot_speed = None
        self.visualize = None
        self._motion_path = None

    def evaluate(self):
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            self._set_ready()
            return
        moving_object = self.get_socket_value(self.moving_object)
        rotating_object = self.get_socket_value(self.rotating_object)
        navmesh_object = self.get_socket_value(self.navmesh_object)
        destination_point = self.get_socket_value(self.destination_point)
        move_dynamic = self.get_socket_value(self.move_dynamic)
        linear_speed = self.get_socket_value(self.linear_speed)
        reach_threshold = self.get_socket_value(self.reach_threshold)
        look_at = self.get_socket_value(self.look_at)
        rot_axis = self.get_socket_value(self.rot_axis)
        front_axis = self.get_socket_value(self.front_axis)
        rot_speed = self.get_socket_value(self.rot_speed)
        visualize = self.get_socket_value(self.visualize)
        if is_invalid(
            destination_point,
            move_dynamic,
            linear_speed,
            reach_threshold,
            look_at,
            rot_axis,
            front_axis,
            rot_speed,
            visualize
        ):
            return
        if is_invalid(moving_object, navmesh_object):
            return
        if is_invalid(rotating_object):
            rotating_object = None
        self._set_ready()
        if (
            (self._motion_path is None) or
            (self._motion_path.destination_changed(destination_point))
        ):
            points = navmesh_object.findPath(
                moving_object.worldPosition,
                destination_point
            )
            motion_path = ActionNavigateWithNavmesh.MotionPath()
            motion_path.points = points[1:]
            motion_path.destination = destination_point
            self._motion_path = motion_path
        next_point = self._motion_path.next_point()
        if visualize:
            points = [moving_object.worldPosition.copy()]
            points.extend(self._motion_path.points[self._motion_path.cursor:])
            points.append(self._motion_path.destination)
            for i, p in enumerate(points):
                if i < len(points) - 1:
                    bge.render.drawLine(
                        p, points[i + 1], [1, 0, 0, 1]
                    )
        if next_point:
            tpf = self.network.time_per_frame
            if look_at and (rotating_object is not None):
                rot_to(
                    rot_axis,
                    rotating_object,
                    next_point,
                    front_axis,
                    rot_speed,
                    tpf
                )
            ths = reach_threshold # if next_point == self._motion_path.destination else .1
            reached = move_to(
                moving_object,
                next_point,
                linear_speed,
                tpf,
                move_dynamic,
                ths
            )
            if reached:
                has_more = self._motion_path.advance()
                if not has_more:
                    self._set_value(True)


class ActionFollowPath(GEActionNode):
    class MotionPath(object):
        def __init__(self):
            self.points = []
            self.cursor = 0
            self.loop = False
            self.loop_start = 0

        def next_point(self):
            if self.cursor < len(self.points):
                return self.points[self.cursor]
            else:
                return None

        def advance(self):
            self.cursor += 1
            if self.cursor < len(self.points):
                return True
            else:
                if self.loop:
                    self.cursor = self.loop_start
                    return True
                return False

    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.moving_object = None
        self.rotating_object = None
        self.path_points = None
        self.loop = None
        self.path_continue = None
        self.navmesh_object = None
        self.move_dynamic = None
        self.linear_speed = None
        self.reach_threshold = None
        self.look_at = None
        self.rot_speed = None
        self.rot_axis = None
        self.front_axis = None
        self._motion_path = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        path_continue = self.get_socket_value(self.path_continue)
        if not_met(condition):
            if not path_continue:
                self._motion_path = None
            self._set_ready()
            return
        moving_object = self.get_socket_value(self.moving_object)
        rotating_object = self.get_socket_value(self.rotating_object)
        path_points = self.get_socket_value(self.path_points)
        navmesh_object = self.get_socket_value(self.navmesh_object)
        move_dynamic = self.get_socket_value(self.move_dynamic)
        linear_speed = self.get_socket_value(self.linear_speed)
        reach_threshold = self.get_socket_value(self.reach_threshold)
        look_at = self.get_socket_value(self.look_at)
        rot_axis = self.get_socket_value(self.rot_axis)
        front_axis = self.get_socket_value(self.front_axis)
        rot_speed = self.get_socket_value(self.rot_speed)
        loop = self.get_socket_value(self.loop)
        if is_invalid(
            path_points,
            move_dynamic,
            linear_speed,
            reach_threshold,
            look_at,
            rot_axis,
            front_axis,
            loop
        ):
            return
        if is_invalid(rot_speed):
            rot_speed = 0
        if loop is None:
            return
        if is_invalid(moving_object):
            return
        if is_invalid(navmesh_object):
            navmesh_object = None
        self._set_ready()
        self._set_value(False)
        if (self._motion_path is None) or (self._motion_path.loop != loop):
            self.generate_path(
                moving_object.worldPosition,
                path_points,
                navmesh_object,
                loop
            )
        next_point = self._motion_path.next_point()
        if next_point:
            tpf = self.network.time_per_frame
            if look_at:
                rot_to(
                    rot_axis,
                    rotating_object,
                    next_point,
                    front_axis,
                    rot_speed,
                    tpf
                )
            reached = move_to(
                moving_object,
                next_point,
                linear_speed,
                tpf,
                move_dynamic,
                reach_threshold
            )
            if reached:
                has_more = self._motion_path.advance()
                if not has_more:
                    self._set_value(True)
                    self.done = True

    def generate_path(self, start_position, path_points, navmesh_object, loop):
        if not path_points:
            return self._motion_path.points.clear()
        path = ActionFollowPath.MotionPath()
        path.loop = loop
        points = path.points
        self._motion_path = path
        if not navmesh_object:
            points.append(Vector(start_position))
            if loop:
                path.loop_start = 1
            for p in path_points:
                points.append(Vector(p))
        else:
            last = path_points[-1]
            mark_loop_position = loop
            for p in path_points:
                subpath = navmesh_object.findPath(
                    start_position,
                    Vector(p)
                )
                if p is last:
                    points.extend(subpath)
                else:
                    points.extend(subpath[:-1])
                if mark_loop_position:
                    path.loop_start = len(points)
                    mark_loop_position = False
                start_position = Vector(p)
            if loop:
                subpath = navmesh_object.findPath(
                    Vector(last),
                    Vector(path_points[0])
                )
                points.extend(subpath[1:])


class ParameterDistance(GEParameterNode):
    def __init__(self):
        GEParameterNode.__init__(self)
        self.parama = None
        self.paramb = None

    def evaluate(self):
        parama = self.get_socket_value(self.parama)
        paramb = self.get_socket_value(self.paramb)
        if is_waiting(parama, paramb):
            return
        self._set_ready()
        self._set_value(compute_distance(parama, paramb))


class ActionReplaceMesh(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.target_game_object = None
        self.new_mesh_name = None
        self.use_display = None
        self.use_physics = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        self._set_ready()
        if not condition:
            return
        target = self.get_socket_value(self.target_game_object)
        mesh = self.get_socket_value(self.new_mesh_name)
        display = self.get_socket_value(self.use_display)
        physics = self.get_socket_value(self.use_physics)
        if is_invalid(target):
            return
        if mesh is None:
            return
        if display is None:
            return
        if physics is None:
            return
        target.replaceMesh(mesh, display, physics)
        if physics:
            target.reinstancePhysicsMesh()
        self.done = True


class RemovePhysicsConstraint(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.object = None
        self.name = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not condition:
            return
        obj = self.get_socket_value(self.object)
        if is_invalid(obj):
            return
        name = self.get_socket_value(self.name)
        if is_invalid(name):
            return
        self._set_ready()
        bge.constraints.removeConstraint(obj[name].getConstraintId())
        self.done = True


class AddPhysicsConstraint(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.target = None
        self.child = None
        self.name = None
        self.constraint = None
        self.use_world = None
        self.pivot = None
        self.use_limit = None
        self.axis_limits = None
        self.linked_col = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not_met(condition):
            return
        target = self.get_socket_value(self.target)
        child = self.get_socket_value(self.child)
        name = self.get_socket_value(self.name)
        constraint = self.get_socket_value(self.constraint)
        pivot = self.get_socket_value(self.pivot)
        use_limit = self.get_socket_value(self.use_limit)
        use_world = self.get_socket_value(self.use_world)
        axis_limits = self.get_socket_value(self.axis_limits)
        linked_col = self.get_socket_value(self.linked_col)
        if is_invalid(
            target,
            child,
            name,
            constraint,
            pivot,
            use_limit,
            use_world,
            axis_limits,
            linked_col
        ):
            return
        self._set_ready()
        flag = 0 if linked_col else 128
        if use_world:
            pivot.x -= target.localPosition.x
            pivot.y -= target.localPosition.y
            pivot.z -= target.localPosition.z
        if use_limit:
            target[name] = bge.constraints.createConstraint(
                target.getPhysicsId(),
                child.getPhysicsId(),
                constraint,
                pivot_x=pivot.x,
                pivot_y=pivot.y,
                pivot_z=pivot.z,
                axis_x=axis_limits.x,
                axis_y=axis_limits.y,
                axis_z=axis_limits.z,
                flag=flag
            )
        else:
            target[name] = bge.constraints.createConstraint(
                target.getPhysicsId(),
                child.getPhysicsId(),
                constraint,
                pivot_x=pivot.x,
                pivot_y=pivot.y,
                pivot_z=pivot.z,
                flag=flag
            )
        self.done = True


class ActionAlignAxisToVector(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.game_object = None
        self.vector = None
        self.axis = None
        self.factor = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        self._set_ready()
        if not_met(condition):
            return
        game_object = self.get_socket_value(self.game_object)
        v = self.get_socket_value(self.vector)
        axis = self.get_socket_value(self.axis)
        factor = self.get_socket_value(self.factor)
        if is_invalid(game_object):
            return
        if axis is None:
            return
        if factor is None:
            return
        v = getattr(v, 'worldPosition', v).copy()
        if not self.local:
            v -= game_object.worldPosition
        if axis > 2:
            matvec = v.copy()
            matvec.negate()
            v = matvec
            axis -= 3
        game_object.alignAxisToVect(v, axis, factor)
        self.done = True


class ActionUpdateBitmapFontQuads(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.game_object = None
        self.text = None
        self.grid_size = None
        self.condition = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):  # no status waiting, test
        self.done = False
        condition = self.get_socket_value(self.condition)
        if not condition:
            return self._set_ready()
        self._set_ready()
        game_object = self.get_socket_value(self.game_object)
        text = eval(self.get_socket_value(self.text))
        grid_size = self.get_socket_value(self.grid_size)
        if is_invalid(game_object):
            return
        if text is None:
            text = ""
        if grid_size is None:
            return
        uv_size = 1.0 / grid_size
        mesh = game_object.meshes[0]
        quad_count = int(mesh.getVertexArrayLength(0) / 4)
        text_size = len(text)
        char_index = 0
        ASCII_START = 32
        for i in range(0, quad_count):
            row = 0
            column = 0
            if char_index < text_size:
                ascii_code = ord(text[char_index])
                grid_code = ascii_code - ASCII_START
                row = int(grid_code / grid_size)
                column = int(grid_code % grid_size)
                char_index += 1
            v0 = mesh.getVertex(0, i * 4)
            v1 = mesh.getVertex(0, i * 4 + 1)
            v2 = mesh.getVertex(0, i * 4 + 2)
            v3 = mesh.getVertex(0, i * 4 + 3)
            xmin = uv_size * column
            xmax = uv_size * (column + 1)
            ymax = 1.0 - (uv_size * row)
            ymin = 1.0 - (uv_size * (row + 1))
            v0.u = xmin
            v0.v = ymin
            v1.u = xmax
            v1.v = ymin
            v2.u = xmax
            v2.v = ymax
            v3.u = xmin
            v3.v = ymax
        self.done = True


class ActionSetCurrentScene(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.condition = None
        self.scene_name = None
        self.done = None
        self.OUT = GEOutSocket(self, self.get_done)

    def get_done(self):
        return self.done

    def evaluate(self):
        self.done = False
        condition = self.get_socket_value(self.condition)
        self._set_ready()
        if not condition:
            return
        scene_name = self.get_socket_value(self.scene_name)
        if scene_name is None:
            return
        current_scene = logic.getCurrentScene()
        current_scene_name = current_scene.name
        if current_scene_name != scene_name:
            logic.addScene(scene_name)
            current_scene.end()
        self.done = True


class ActionStringOp(GEActionNode):
    def __init__(self):
        GEActionNode.__init__(self)
        self.opcode = None
        self.condition = None
        self.input_string = None
        self.input_param_a = None
        self.input_param_b = None

    def evaluate(self):
        self._set_ready()
        code = self.get_socket_value(self.opcode)
        condition = self.get_socket_value(self.condition)
        input_string = self.get_socket_value(self.input_string)
        input_param_a = self.get_socket_value(self.input_param_a)
        input_param_b = self.get_socket_value(self.input_param_b)
        if not condition:
            return
        if input_string is None:
            return
        input_string = str(input_string)
        if code == 0:  # postfix
            self._set_value(input_string + str(input_param_a))
        elif code == 1:  # prefix
            self._set_value(str(input_param_a) + input_string)
        elif code == 2:  # infix
            self._set_value(
                str(input_param_a) +
                input_string +
                str(input_param_b)
            )
        elif code == 3:  # remove last
            self._set_value(input_string[:-1])
        elif code == 4:  # remove first
            self._set_value(input_string[1:])
        elif code == 5:  # replace a with b in string
            self._set_value(
                input_string.replace(
                    str(input_param_a),
                    str(input_param_b)
                )
            )
        elif code == 6:  # upper case
            self._set_value(input_string.upper())
        elif code == 7:  # lower case
            self._set_value(input_string.lower())
        elif code == 8:  # remove range
            self._set_value(
                input_string[:input_param_a] +
                input_string[input_param_b:]
            )
        elif code == 9:  # insert at
            self._set_value(
                input_string[:input_param_b] +
                str(input_param_a) +
                input_string[input_param_b:]
            )
        elif code == 10:  # length
            self._set_value(len(input_string))
        elif code == 11:  # substring
            self._set_value(input_string[input_param_a:input_param_b])
        elif code == 12:  # first index of
            self._set_value(input_string.find(str(input_param_a)))
        elif code == 13:  # last index of
            self._set_value(input_string.rfind(str(input_param_a)))
        pass
    pass


class ParameterMathFun(GEParameterNode):

    @classmethod
    def signum(cls, a): return (a > 0) - (a < 0)

    @classmethod
    def curt(cls, a):
        if a > 0:
            return a**(1./3.)
        else:
            return -(-a)**(1./3.)

    def __init__(self):
        GEParameterNode.__init__(self)
        self.a = None
        self.b = None
        self.formula = ""
        self._previous_values = [None, None]
        self._formula_globals = globals()
        self._formula_locals = {
            "exp": math.exp,
            "pow": math.pow,
            "log": math.log,
            "log10": math.log10,
            "acos": math.acos,
            "asin": math.asin,
            "atan": math.atan,
            "atan2": math.atan2,
            "cos": math.cos,
            "hypot": math.hypot,
            "sin": math.sin,
            "tan": math.tan,
            "degrees": math.degrees,
            "radians": math.radians,
            "acosh": math.acosh,
            "asinh": math.asinh,
            "atanh": math.atanh,
            "cosh": math.cosh,
            "sinh": math.sinh,
            "tanh": math.tanh,
            "pi": math.pi,
            "e": math.e,
            "ceil": math.ceil,
            "sign": ParameterMathFun.signum,
            "abs": math.fabs,
            "floor": math.floor,
            "mod": math.fmod,
            "sqrt": math.sqrt,
            "curt": ParameterMathFun.curt,
            "str": str,
            "int": int,
            "float": float
        }

    def evaluate(self):
        self._set_ready()
        a = self.get_socket_value(self.a)
        b = self.get_socket_value(self.b)
        olds = self._previous_values
        do_update = (
            (a != olds[0]) or
            (b != olds[1])
        )
        if do_update:
            formula_locals = self._formula_locals
            formula_locals["a"] = a
            formula_locals["b"] = b
            out = eval(self.formula, self._formula_globals, formula_locals)
            olds[0] = a
            olds[1] = b
            self._set_value(out)