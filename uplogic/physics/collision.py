from bge import logic


class ULCollision():
    target = None
    point = None
    normal = None
    tap = False
    consumed = False
    active = False
    _objects = []
    done_objs = []

    def __init__(self, game_object, callback, prop, mat, tap):
        self.callback = callback
        self.prop = prop
        self.mat = mat
        self.tap = tap
        self.game_object = game_object
        self.register()

    def collision(self, obj, point, normal):
        if self.tap and self.consumed:
            self.active = True
            return
        self._objects.append(obj)
        material = self.mat
        prop = self.prop
        bo = obj.blenderObject
        if material:
            if material not in [
                slot.material.name for
                slot in
                bo.material_slots
            ]:
                return
        if prop:
            for obj in self._objects:
                if prop not in obj:
                    return

        self.active = True
        if obj not in self.done_objs:
            self.callback(obj, point, normal)
            self.done_objs.append(obj)

    def update(self, cam):
        self.done_objs = []
        if not self.consumed and self.active:
            self.consumed = True
        elif self.consumed and not self.active:
            self.consumed = False
        self.active = False

    def register(self):
        if self.collision not in self.game_object.collisionCallbacks:
            self.game_object.collisionCallbacks.append(self.collision)
        logic.getCurrentScene().pre_draw.append(self.update)

    def unregister(self):
        self.game_object.collisionCallbacks.remove(self.collision)
        logic.getCurrentScene().pre_draw.remove(self.update)


def on_collision(obj, callback, property='', material='', tap=False):
    return ULCollision(obj, callback, property, material, tap)
