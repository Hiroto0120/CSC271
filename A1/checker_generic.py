import sys
import subprocess
import importlib
import pandas as pd

from pandas.testing import assert_frame_equal, assert_series_equal
from typing import Tuple, Callable, Any, Dict

PYTHON_TA_VERSION = '2.12.0'
TARGET_LEN = 79
SEP = '='


def python_ta_installed() -> bool:
    """Return True if PythonTA is installed."""
    try:
        import python_ta
        importlib.reload(python_ta)
        installed_version = python_ta.__version__
        return installed_version == PYTHON_TA_VERSION
    except:
        return False


def install_python_ta():
    """Tries to install PythonTA."""
    if not python_ta_installed():
        print("[Installing the style checker] Attempt #1 ...")
        try:
            subprocess.Popen(
                f'python3 -m pip install python-ta=={PYTHON_TA_VERSION}',
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except:
            pass

    if not python_ta_installed():
        print("[Installing the style checker] Attempt #2 ...")
        try:
            subprocess.check_call(
                [sys.executable, '-m', 'pip', 'install',
                f'python-ta=={PYTHON_TA_VERSION}'],
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL
            )
        except:
            pass


def run_pyta(filename: str, config_file: str) -> None:
    """Run PYTA with configuration config_file on the file named filename.
    """
    import json
    install_python_ta()

    error_message = '\nCould not install or run the style checker correctly.\n' \
                    'Please try to re-run the checker once.\n' \
                    'If you have already tried to re-run it, please go to office hours\n' \
                    'in order to resolve this.' \
                    'For now, you may upload your code to MarkUs and run the self-test\n' \
                    'to see the style checker results.'

    try:
        import python_ta
        with open(config_file) as cf:
            config_dict = json.loads(cf.read())
            config_dict['output-format'] = 'pyta-plain'

        python_ta.check_all(filename, config=config_dict)
    except:
        print(error_message)

def check_type(func: Callable, args: list, expected: type) -> Tuple[bool, Any]:
    """Check if func(args) returns a result of type expected.

    Return (True, result-of-call) if the check succeeds.
    Return (False, error-or-failure-message) if anything goes wrong.
    """
    try:
        returned = func(*args)
    except Exception as exn:
        return False, _error_message(func, args, exn)

    if isinstance(returned, expected):
        return True, returned

    return False, _type_error_message(func, expected, returned)

def check_constants(name2value: Dict[str, object], mod: Any) -> None:
    """Check that, for each (name, value) pair in name2value, the value of
    a variable named name in module mod is value.

    Args:
        name2value: Dictionary mapping constant names to expected values
        mod: Module containing the constants to check
    """

    for name, expected in name2value.items():
        actual = getattr(mod, name)
        msg = 'The value of constant {} should be {} but is {}.'.format(
            name, expected, actual)
        if expected != actual:
            return False, msg
    return True, ""


def check_mutation(func: Callable, df_before: pd.DataFrame,
                   df_expected: pd.DataFrame, args: list = None) -> Tuple[bool, str]:
    """Check if func mutates df_before to match df_expected.

    Args:
        func: Function to test
        df_before: DataFrame to mutate
        df_expected: Expected DataFrame after mutation
        args: Additional arguments to pass to func after df_before

    Return (True, "") if the check succeeds.
    Return (False, error-message) if anything goes wrong.
    """
    if args is None:
        args = []

    try:
        result = func(df_before, *args)
    except Exception as exn:
        return False, _error_message(func, [df_before] + args, exn)

    try:
        assert_frame_equal(df_before, df_expected)
    except AssertionError as e:
        return False, f"{func.__name__} did not mutate DataFrame correctly: {str(e)}"

    if result is not None:
        return False, f"{func.__name__} should return None but returned {result}"

    return True, ""

def check_output(func: Callable, args: list, expected_output: Any,
                 comparison_func: Callable = None) -> Tuple[bool, str]:
    """Check if func(args) produces the expected output.

    Args:
        func: Function to test
        args: Arguments to pass to func
        expected_output: Expected return value
        comparison_func: Custom comparison function (default: assert_frame_equal or assert_series_equal)

    Return (True, "") if the check succeeds.
    Return (False, error-message) if anything goes wrong.
    """
    try:
        result = func(*args)
    except Exception as exn:
        return False, _error_message(func, args, exn)

    try:
        if comparison_func:
            comparison_func(result, expected_output)
        elif isinstance(expected_output, pd.DataFrame):
            assert_frame_equal(result, expected_output)
        elif isinstance(expected_output, pd.Series):
            assert_series_equal(result, expected_output)
        else:
            assert result == expected_output
    except AssertionError as e:
        return False, f"{func.__name__} output does not match expected: {str(e)}"

    return True, ""

def _type_error_message(func: Callable, expected: type, got: object) -> str:
    """Return an error message for function func returning got, where the
    correct return type is expected.
    """
    return '{} should return a {}, but returned {}'.format(
        func.__name__, expected.__name__, got)

def _error_message(func: Callable, args: list, error: Exception) -> str:
    """Return an error message: func(args) raised an error."""
    args_str = ', '.join(str(arg)[:50] + '...' if len(str(arg)) > 50 else str(arg)
                         for arg in args)
    return 'The call {}({}) caused an error: {}'.format(
        func.__name__, args_str, error)
