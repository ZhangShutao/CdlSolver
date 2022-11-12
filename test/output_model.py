
class OutputModel:
    def __init__(self, x=None, y=None):
        if x is None:
            x = set()
        if y is None:
            y = set()
        self._x = x
        self._y = y

    def load(self, str):
        parts = str.strip().replace(' ', '').split(';')
        self._x = set(parts[0].replace('x:', '').split(','))
        self._y = set(parts[1].replace('y:', '').split(','))

    def __key(self):
        return ';'.join([','.join([str(x) for x in self._x]), ','.join([str(y) for y in self._y])])

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
        return "x:" + ','.join(lis_x) + ";y:" + ','.join(lis_y) + ";"


class Output:
    def __init__(self, models=None):
        if models is None:
            models = set()
        self._models = models

    def add(self, model):
        self._models.add(model)

    def load(self, str):
        for line in str.splitlines():
            if line.startswith('x'):
                model = OutputModel()
                model.load(line)
                self._models.add(model)

    def count(self):
        return len(self._models)

    def __eq__(self, other):
        if isinstance(other, Output):
            set_mod = set([str(m) for m in self._models])
            set_other = set([str(m) for m in other._models])
            return set_mod == set_other
        return NotImplemented

