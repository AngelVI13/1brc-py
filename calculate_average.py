from ipdb import set_trace as breakpoint
from typing import Callable, TypedDict
from dataclasses import dataclass

NOT_SET = 200.0


def run(filename: str):
    DataType = dict[str, dict[str, float | int]]

    def get_or_default(data: DataType, key: str) -> dict[str, float | int]:
        v = data.get(key)
        if v is None:
            new_v = {"min": 200.0, "mean": 200.0, "max": 200.0, "n": 0.0}
            data[key] = new_v
            return new_v

        return v

    data: DataType = {}
    count = 0

    f = open(filename, "r")
    for line in f:
        count += 1
        if count % 50_000_000 == 0:
            print(count)
            break

        name, temp = line.split(";")
        temp_f = float(temp)

        d = get_or_default(data, name)
        d_min = d["min"]
        if temp_f < d_min or d_min == NOT_SET:
            d["min"] = temp_f

        d_max = d["max"]
        if temp_f > d_max or d_max == NOT_SET:
            d["max"] = temp_f

        d["mean"] += temp_f
        d["n"] += 1

    f.close()
    print("done processing")

    for k in sorted(data):
        d = data[k]
        print(f"{k}={d['min']}/{d['mean']/d['n']}/{d['max']}")


def run_typed_dict(filename: str):
    class Data(TypedDict):
        min: float
        mean: float
        max: float
        n: float

    def get_or_default(data: dict[str, Data], key: str) -> Data:
        v = data.get(key)
        if v is None:
            new_v: Data = {"min": 200.0, "mean": 200.0, "max": 200, "n": 0.0}
            data[key] = new_v
            return new_v

        return v

    data: dict[str, Data] = {}
    count = 0

    f = open(filename, "r")
    for line in f:
        count += 1
        if count % 50_000_000 == 0:
            print(count)
            break

        name, temp = line.split(";")
        temp_f = float(temp)

        d = get_or_default(data, name)
        d_min = d["min"]
        if temp_f < d_min or d_min == NOT_SET:
            d["min"] = temp_f

        d_max = d["max"]
        if temp_f > d_max or d_max == NOT_SET:
            d["max"] = temp_f

        d["mean"] += temp_f
        d["n"] += 1

    f.close()
    print("done processing")

    for k in sorted(data):
        d = data[k]
        print(f"{k}={d['min']}/{d['mean']/d['n']}/{d['max']}")


def run2(filename: str):
    class Data:
        def __init__(self):
            self.min = NOT_SET
            self.mean = 0.0
            self.max = NOT_SET
            self.n = 0

    data: dict[str, Data] = {}
    count = 0

    f = open(filename, "r")
    for line in f:
        count += 1
        if count % 50_000_000 == 0:
            print(count)
            break

        name, temp = line.split(";")
        temp_f = float(temp)

        d = data.get(name)
        if d is None:
            d = Data()
            data[name] = d

        if temp_f < d.min or d.min == NOT_SET:
            d.min = temp_f

        if temp_f > d.max or d.max == NOT_SET:
            d.max = temp_f

        d.mean += temp_f
        d.n += 1

    f.close()
    print("done processing")

    for k in sorted(data):
        d = data[k]
        print(f"{k}={d.min}/{d.mean/d.n}/{d.max}")


def run2_slots(filename: str):
    class Data:
        __slots__ = ["min", "mean", "max", "n"]

        def __init__(self):
            self.min: float = NOT_SET
            self.mean: float = 0.0
            self.max: float = NOT_SET
            self.n: int = 0

    data: dict[str, Data] = {}
    count = 0

    f = open(filename, "r")
    for line in f:
        count += 1
        if count % 50_000_000 == 0:
            print(count)
            break

        name, temp = line.split(";")
        temp_f = float(temp)

        d = data.get(name)
        if d is None:
            d = Data()
            data[name] = d

        if temp_f < d.min or d.min == NOT_SET:
            d.min = temp_f

        if temp_f > d.max or d.max == NOT_SET:
            d.max = temp_f

        d.mean += temp_f
        d.n += 1

    f.close()
    print("done processing")

    for k in sorted(data):
        d = data[k]
        print(f"{k}={d.min}/{d.mean/d.n}/{d.max}")


def run2_slots_less_cond(filename: str):
    class Data:
        __slots__ = ["min", "mean", "max", "n"]

        def __init__(self):
            self.min: float = 200
            self.mean: float = 0.0
            self.max: float = -200
            self.n: int = 0

    data: dict[str, Data] = {}
    count = 0

    f = open(filename, "r")
    for line in f:
        count += 1
        if count % 50_000_000 == 0:
            print(count)
            break

        name, temp = line.split(";")
        # TODO: maybe create my own float convertions that assumes correct input
        temp_f = float(temp)

        d = data.get(name)
        if d is None:
            d = Data()
            data[name] = d

        d.n += 1
        d.mean += temp_f
        if temp_f < d.min:
            d.min = temp_f
            continue

        if temp_f > d.max:
            d.max = temp_f

    f.close()
    print("done processing")

    # TODO: is data.items() better than data[k]
    for k in sorted(data):
        d = data[k]
        # TODO: string builder ?
        # TODO: only print once in the end?
        print(f"{k}={d.min}/{d.mean/d.n}/{d.max}")


if __name__ == "__main__":
    from time import time as t

    filename = "../1brc/measurements.txt"
    out: list[str] = []

    @dataclass
    class InData:
        fn: Callable[[str], None]
        label: str

    inputs = (
        InData(run, "run(dict)"),
        InData(run_typed_dict, "run_typed_dict(dict)"),
        InData(run2, "run2(class)"),
        InData(run2_slots, "run2_slots(class)"),
        InData(run2_slots_less_cond, "run2_slots_less_cond(class)"),
        # TODO: what about tuples ?
        # TODO: what about sorting while storing, knowing that keys are city names
    )
    # TODO: what about preallocate a dict as follows
    """
    d = {
            "A": [""] * 100
            "B": [""] * 100
            ...
            "Z": [""] * 100
    }
    and then just sort the smaller lists? maybe even pass a cmp fn to check
    from name[1:] since they will all start with the same name?

    there still will be some cities that start with special chars but those
    lists can be added dynamically

    also maybe for keys we can use chr(name[0]) cause that can simplify hashing ?

    also 1 char strings as keys might be good because of str interning
    """

    # TODO: looks at performance tools: cperf? timeit? something that shows flamegraphs?

    for in_ in inputs:
        start = t()
        in_.fn(filename)
        out.append(f"---{in_.label}: {t()-start}")

    for l in out:
        print(l)
