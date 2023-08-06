"""conftest.py for stepseries."""


from queue import Empty, Queue
from typing import Dict, Tuple

import pytest

from stepseries.commands import OSCCommand, OSCGetCommand
from stepseries.responses import OSCResponse
from stepseries.stepXXX import STEPXXX

# store history of failures per test class name and per index in parametrize (if parametrize used)
_test_failed_incremental: Dict[str, Dict[Tuple[int, ...], str]] = {}


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        # incremental marker is used
        if call.excinfo is not None and call.excinfo.typename != "Skipped":
            # the test has failed
            # retrieve the class name of the test
            cls_name = str(item.cls)
            # retrieve the index of the test
            # (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the test function
            test_name = item.originalname or item.name
            # store in _test_failed_incremental the original name of the failed test
            _test_failed_incremental.setdefault(cls_name, {}).setdefault(
                parametrize_index, test_name
            )


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        # retrieve the class name of the test
        cls_name = str(item.cls)
        # check if a previous test has failed for this class
        if cls_name in _test_failed_incremental:
            # retrieve the index of the test
            # (if parametrize is used in combination with incremental)
            parametrize_index = (
                tuple(item.callspec.indices.values())
                if hasattr(item, "callspec")
                else ()
            )
            # retrieve the name of the first test function to fail for this class name and index
            test_name = _test_failed_incremental[cls_name].get(parametrize_index, None)
            # if name found, test has failed for the combination of class name & test name
            if test_name is not None:
                pytest.xfail("previous test failed ({})".format(test_name))


@pytest.fixture(scope="package")
def wait_for() -> None:
    def wrapper(
        device: STEPXXX, command: OSCCommand, response_cls: OSCResponse, timeout=10
    ):
        # A device that allows us to return the response from the device
        waiter = Queue()

        # The callback responsible for intercepting the correct response
        def callback(message: OSCResponse) -> None:
            waiter.put(message)

        # Register the callback
        device.on(response_cls, callback)

        # Send the command
        if isinstance(command, OSCGetCommand):
            device.get(command, wait=False)
        else:
            device.set(command)

        try:
            # Wait for the response until timeout
            return waiter.get(timeout=timeout)
        except Empty:
            raise TimeoutError("no response was returned")
        finally:
            # Regardless if the response is received, unregister the
            # callback
            device.remove(callback)

    return wrapper
