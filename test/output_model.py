
class OutputModel:
    def __init__(self, x=None, y=None):
        if x is None:
            x = set()
        if y is None:
            y = set()
        self._x = x
        self._y = y

    def load(self, strx, stry):
        # parts = str.strip().replace(' ', '').split(';\n')
        self._x = set(strx.replace('X:', '').split(','))
        self._y = set(stry.replace('A:', '').split(','))

    def x(self):
        return self._x

    def y(self):
        return self._y

    def __key(self):
        return ';\n'.join([','.join([str(x) for x in self._x]), ','.join([str(y) for y in self._y])])

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, OutputModel):
            return self._x == other._x and self._y == other._y
        return NotImplemented

    def __repr__(self):
        lis_x = [str(x) for x in self._x]
        lis_y = [str(y) for y in self._y]
        lis_x.sort()
        lis_y.sort()
        return "X:" + ','.join(lis_x) + ";\nA:" + ','.join(lis_y) + ";\n"


class Output:
    def __init__(self, models=None):
        if models is None:
            models = set()
        self._models = models

    def add(self, model):
        self._models.add(model)

    def load(self, str):
        lines = str.splitlines()
        for i in range(len(lines)):
            if lines[i].startswith('X'):
                model = OutputModel()
                model.load(lines[i], lines[i+1])
                self._models.add(model)

    def count(self):
        return len(self._models)

    def __eq__(self, other):
        if isinstance(other, Output):
            set_mod = set([str(m) for m in self._models])
            set_other = set([str(m) for m in other._models])
            return set_mod == set_other
        return NotImplemented

