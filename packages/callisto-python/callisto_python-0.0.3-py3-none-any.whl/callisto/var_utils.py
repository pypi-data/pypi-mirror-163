import json
import math
import sys
import traceback

KB = float(1024)
MB = float(KB ** 2)  # 1,048,576
GB = float(KB ** 3)  # 1,073,741,824
TB = float(KB ** 4)  # 1,099,511,627,776

DEFAULT_ABBREV_LEN = 50


def human_bytes(B):
    """Return the given bytes as a human friendly KB, MB, GB, or TB string"""
    B = float(B)

    if B < KB:
        return "{0} {1}".format(B, "Bytes" if B > 1 else "Byte")
    elif KB <= B < MB:
        return "{0:.2f} KB".format(B / KB)
    elif MB <= B < GB:
        return "{0:.2f} MB".format(B / MB)
    elif GB <= B < TB:
        return "{0:.2f} GB".format(B / GB)
    elif TB <= B:
        return "{0:.2f} TB".format(B / TB)


def make_multi_dict(
    row_names, column_names, data, total_row_count=None, total_column_count=None
):
    """
    column_count and row_count should be values for the whole data structure
    column_names and row_names are values for the possibly abbreviated structure
    """
    if type(column_names) == str:
        column_names = [column_names]
    if type(row_names) == str:
        row_names == [row_names]
    value = {
        "column_count": total_column_count
        if total_column_count is not None
        else len(column_names),
        "row_count": total_row_count if total_row_count is not None else len(row_names),
        "column_names": column_names,
        "row_names": row_names,
        "data": data,
    }
    return {"multi_value": value}


def validate_value(value, no_preview=False):
    if value is None and no_preview:
        return None
    if list(value.keys()) == ["single_value"]:
        return {"single_value": str(value["single_value"])}
    elif list(value.keys()) == ["multi_value"]:
        val = value["multi_value"]
        val["column_names"] = list(map(str, val["column_names"]))
        val["row_names"] = list(map(str, val["row_names"]))
        # double map through the nested arrays in 'data'
        val["data"] = list(map(lambda x: list(map(str, x)), val["data"]))
        return {"multi_value": val}
    else:
        msg = (
            "Value should be single entry dict with a key of "
            "'single_value' or 'multi_value'."
        )
        msg += f" Found keys: {tuple(value.keys())}"
        raise ValueError(msg)


def get_list_var(obj, name, abbrev_len=DEFAULT_ABBREV_LEN, no_preview=False):
    summary = f"Length: {len(obj)}"
    abbrev = False
    preview = None
    if not no_preview:
        abbrev = len(obj) > abbrev_len if abbrev_len is not None else False
        obj_pre = obj[0:abbrev_len] if abbrev else obj
        data = tuple(map(lambda x: [str(x)], obj_pre))
        row_names = list(range(len(obj_pre)))
        preview = make_multi_dict(row_names, name, data, total_row_count=len(obj))
    return (
        summary,
        abbrev,
        preview,
    )


def get_dict_var(obj, abbrev_len=DEFAULT_ABBREV_LEN, no_preview=False):
    summary = f"Length: {len(obj)}"
    abbrev = False
    preview = None
    if not no_preview:
        abbrev = len(obj) > abbrev_len if abbrev_len is not None else False
        obj_pre = {
            key: val
            for i, (key, val) in enumerate(obj.items())
            if not abbrev or i < abbrev_len
        }
        data = tuple(map(lambda x: [str(x[0]), str(x[1])], obj_pre.items()))
        row_names = list(range(len(obj_pre)))
        preview = make_multi_dict(
            row_names, ["Key", "Value"], data, total_row_count=len(obj)
        )
    return (
        summary,
        abbrev,
        preview,
    )


def get_numpy_2d_var(obj, abbrev_len=DEFAULT_ABBREV_LEN, no_preview=False):
    summary = f"Size: {obj.shape[0]}x{obj.shape[1]} Memory: {human_bytes(obj.nbytes)}"
    abbrev = False
    preview = None
    if not no_preview:
        abbrev = obj.size > abbrev_len if abbrev_len is not None else False
        obj_pre = obj[0 : math.ceil(abbrev_len / obj.shape[1])] if abbrev else obj
        data = obj_pre.tolist()
        row_names = list(range(obj_pre.shape[0]))
        column_names = list(range(obj_pre.shape[1]))
        preview = make_multi_dict(
            row_names, column_names, data, obj.shape[0], obj.shape[1]
        )
    return (
        summary,
        abbrev,
        preview,
    )


def get_numpy_1d_var(obj, name, abbrev_len=DEFAULT_ABBREV_LEN, no_preview=False):
    summary = f"Length: {obj.shape[0]} Memory: {human_bytes(obj.nbytes)}"
    abbrev = False
    preview = None
    if not no_preview:
        abbrev = obj.size > abbrev_len if abbrev_len is not None else False
        obj_pre = obj[0:abbrev_len] if abbrev else obj
        data = tuple(map(lambda x: [str(x)], obj_pre.tolist()))
        row_names = list(range(obj_pre.shape[0]))
        column_names = name
        preview = make_multi_dict(
            row_names, column_names, data, total_row_count=obj.shape[0]
        )
    return (
        summary,
        abbrev,
        preview,
    )


def get_pandas_dataframe_var(obj, abbrev_len=DEFAULT_ABBREV_LEN, no_preview=False):
    summary = (
        f"Size: {obj.shape[0]}x{obj.shape[1]}"
        + f" Memory: {human_bytes(obj.memory_usage(deep=True).sum())}"
    )
    abbrev = False
    preview = None
    if not no_preview:
        abbrev = obj.size > abbrev_len if abbrev_len is not None else False
        obj_pre = obj.iloc[0 : math.ceil(abbrev_len / obj.shape[1])] if abbrev else obj
        data = obj_pre.to_numpy().tolist()
        row_names = tuple(map(lambda x: str(x), obj_pre.index.to_list()))
        column_names = obj_pre.columns.to_list()
        preview = make_multi_dict(
            row_names, column_names, data, obj.shape[0], obj.shape[1]
        )
    return (
        summary,
        abbrev,
        preview,
    )


def get_pandas_series_var(obj, name, abbrev_len=DEFAULT_ABBREV_LEN, no_preview=False):
    summary = f"Length: {len(obj)} Memory: {human_bytes(obj.memory_usage(deep=True))}"
    abbrev = False
    preview = None
    if not no_preview:
        abbrev = obj.size > abbrev_len if abbrev_len is not None else False
        obj_pre = obj.iloc[0:abbrev_len] if abbrev else obj
        data = tuple(map(lambda x: [str(x)], obj_pre.to_list()))
        row_names = tuple(map(lambda x: str(x), obj_pre.index.to_list()))
        preview = make_multi_dict(row_names, name, data, total_row_count=obj.size)
    return (
        summary,
        abbrev,
        preview,
    )


def get_var_details(obj, name, abbrev_len=DEFAULT_ABBREV_LEN, no_preview=False):
    """
    Get formatted info for a specific var. Pass abbrev_len=None
    to get non-abbreviated variable info. Pass no_preview=True to exclude the
    preview of the var's data
    """
    obj_type = type(obj)
    summary = ""
    value = None
    # Is the var big enough to be abbreviated
    abbrev = False

    # check custom values (careful not to call summary / value on
    # the Class object, only on the instances)
    if (
        obj_type != type
        and hasattr(obj, "jupyter_d1_summary")
        and callable(getattr(obj, "jupyter_d1_summary"))
    ):
        summary = obj.jupyter_d1_summary()
        if hasattr(obj, "jupyter_d1_value") and callable(
            getattr(obj, "jupyter_d1_value")
        ):
            value = obj.jupyter_d1_value()
        else:
            value = None

    # single valued intrinsics
    elif obj_type.__name__ in ["int", "str", "float", "bool", "complex"]:
        summary = obj
        value = {"single_value": str(obj)}

    # list
    elif obj_type.__name__ == "list" or obj_type.__name__ == "tuple":
        summary, abbrev, value = get_list_var(obj, name, abbrev_len, no_preview)

    # dictionary
    elif obj_type.__name__ == "dict":
        summary, abbrev, value = get_dict_var(obj, abbrev_len, no_preview)

    # numpy 2D array
    elif obj_type.__name__ == "ndarray" and obj.ndim == 2:
        summary, abbrev, value = get_numpy_2d_var(obj, abbrev_len, no_preview)

    # numpy 1D array
    elif obj_type.__name__ == "ndarray" and obj.ndim == 1:
        summary, abbrev, value = get_numpy_1d_var(obj, name, abbrev_len, no_preview)

    # pandas data frame
    elif obj_type.__name__ == "DataFrame":
        summary, abbrev, value = get_pandas_dataframe_var(obj, abbrev_len, no_preview)

    # pandas series
    elif obj_type.__name__ == "Series":
        summary, abbrev, value = get_pandas_series_var(
            obj, name, abbrev_len, no_preview
        )

    # if all else fails, fall back to single value string representation
    else:
        summary = str(obj)
        value = {"single_value": str(obj)}

    return {
        "name": name,
        "type": obj_type.__name__,
        "abbreviated": bool(abbrev),
        "summary": str(summary)[:140],  # limit summary length
        "value": validate_value(value, no_preview),
    }


def create_exception_var(e):
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback_lines = traceback.format_exception(exc_type, exc_value, exc_tb)
    return {
        "name": "Introspection Error",
        "type": type(e).__name__,
        "summary": str(e),
        "abbreviated": str(False),
        "value": {
            "multi_value": {
                "column_count": 1,
                "row_count": len(traceback_lines),
                "column_names": "Traceback",
                "row_names": list(range(len(traceback_lines))),
                "data": tuple(map(lambda x: [x], traceback_lines)),
            }
        },
    }


def format_vars(vars_output, abbrev_len=DEFAULT_ABBREV_LEN, no_preview=False, **kwargs):
    """
    Get string containing json representation of currently defined vars
    (pass the output of `vars()` to this function)

    kwargs currently only serve to make this API a little bit future-proof
    """
    try:
        current_vars = []
        for item in tuple(vars_output.items()):
            name = item[0]
            obj = item[1]
            if name.startswith("__") or name.startswith("@py_assert"):
                continue
            obj_type = type(obj)
            if obj_type.__name__ in ["type", "module", "function"]:
                continue

            var_details = get_var_details(obj, name, abbrev_len, no_preview=no_preview)

            current_vars.append(var_details)

    except Exception as e:
        current_vars = [create_exception_var(e)]

    return json.dumps(current_vars)


def format_var(obj, name, abbrev_len=DEFAULT_ABBREV_LEN, **kwargs):
    """Get string containing json representation of a var"""
    try:
        var_details = get_var_details(obj, name, abbrev_len)
        return json.dumps(var_details)
    except Exception as e:
        var_details = create_exception_var(e)

    return json.dumps(var_details)
