import traceback
import collections
import datetime


def exception_to_string(
    exception: Exception,
    project_name: str = None,
    task_name: str = None,
    *args,
    **kwargs
) -> str:
    """
    Convert exception to string.
    :param exception: Exception to convert.
    :return: String representation of exception.
    """

    ordered_dict = collections.OrderedDict()
    ordered_dict['project'] = project_name
    if task_name:
        ordered_dict['task'] = task_name
    ordered_dict['args'] = args
    ordered_dict['kwargs'] = kwargs
    ordered_dict['exception'] = str(exception)
    ordered_dict['traceback'] = "".join(
        traceback.format_tb(exception.__traceback__)
    )
    ordered_dict['time'] = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    return "\n\n".join(
        [
            f"{key}: {value}"
            for key, value in ordered_dict.items()
        ]
    ), ordered_dict
