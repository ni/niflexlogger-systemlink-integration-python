"""Start and stop a FlexLogger test session."""

import datetime
import time

from _helpers import get_http_config, get_tag_prefix
from systemlink.clients import tag as sl_tag


def _main() -> None:
    mgr = sl_tag.TagManager(get_http_config())

    time_before_start = datetime.datetime.now(datetime.timezone.utc)
    start_test_session(mgr)

    print("Sent start request; waiting for acknowledgement")
    wait_for_test_session_start(mgr, time_before_start)

    print("Test started; press Ctrl-C to stop it")
    try:
        while True:
            time.sleep(100)
    except KeyboardInterrupt:
        print("Stopping test session")
        stop_test_session(mgr)


def start_test_session(mgr: sl_tag.TagManager) -> None:
    """Start a FlexLogger test session."""
    writer = mgr.create_writer(buffer_size=1)
    path = get_tag_prefix() + ".Export.System.IsTestSessionRunning"
    already_running = mgr.read(path)
    if already_running is not None and already_running.value is True:
        raise RuntimeError("There is already a test session running")
    writer.write(path, sl_tag.DataType.BOOLEAN, True)


def wait_for_test_session_start(
    mgr: sl_tag.TagManager, after_time: datetime.datetime = None
) -> None:
    """Wait for a recently-started FlexLogger test session to actually start."""
    if after_time is None:
        after_time = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(
            seconds=-2
        )

    # Wait for LastTestSessionStart to be updated by FlexLogger
    tag_path = get_tag_prefix() + ".Export.System.LastTestSessionStart"
    tag_reader = mgr.get_tag_reader(tag_path, sl_tag.DataType.DATE_TIME)
    while True:
        read_result = tag_reader.read(include_timestamp=True)
        if read_result is not None and read_result.value > after_time:
            assert read_result.timestamp is not None
            last_start = read_result.timestamp
            break
        time.sleep(0.5)

    # In FlexLogger 2020 R3+, the timestamps of the two values will be the same. In
    # older versions, IsTestSessionRunning is updated second.
    tag_path = get_tag_prefix() + ".Export.System.IsTestSessionRunning"
    tag_reader2 = mgr.get_tag_reader(tag_path, sl_tag.DataType.BOOLEAN)
    while True:
        read_result2 = tag_reader2.read(include_timestamp=True)
        if read_result2 is not None and read_result2.value is True:
            assert read_result2.timestamp is not None
            if read_result2.timestamp >= last_start:
                return
        time.sleep(0.5)


def stop_test_session(mgr: sl_tag.TagManager) -> None:
    """Stop the current FlexLogger test session."""
    writer = mgr.create_writer(buffer_size=1)
    path = get_tag_prefix() + ".Export.System.IsTestSessionRunning"
    writer.write(path, sl_tag.DataType.BOOLEAN, False)


if __name__ == "__main__":
    _main()
