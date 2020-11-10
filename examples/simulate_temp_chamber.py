"""Create FlexLogger channels and write simulated data to them."""

import datetime
import random
import time

from _helpers import get_http_config, get_tag_prefix
from systemlink.clients import tag as sl_tag


def _main() -> None:
    mgr = sl_tag.TagManager(get_http_config())

    print("Starting simulation; hit Ctrl-C to stop")
    _simulate_temp_chamber(mgr)


def create_channel(
    mgr: sl_tag.TagManager, group: str, name: str, data_type: sl_tag.DataType
) -> sl_tag.TagData:
    """Create a FlexLogger channel."""
    tag_path = get_tag_prefix() + ".Import.{}.{}".format(group, name)
    return mgr.open(tag_path, data_type, create=True)


def _simulate_temp_chamber(mgr: sl_tag.TagManager) -> None:  # noqa: D103
    # fl = flexlogger.Client()
    # .buffered_channel_writer is a thin wrapper around systemlink.tag.BufferedTagWriter
    #  - this wrapper takes TagData objects instead of `path` and `datatype` parameters
    #  - maybe I'll instead modify systemlink.tag.BufferedTagWriter to accept a TagData
    writer = mgr.create_writer(buffer_size=10)
    chans = [
        create_channel(mgr, "Temperature Chamber", "Ceiling", sl_tag.DataType.DOUBLE),
        create_channel(mgr, "Temperature Chamber", "Door", sl_tag.DataType.DOUBLE),
        create_channel(mgr, "Temperature Chamber", "Floor", sl_tag.DataType.DOUBLE),
    ]
    vals = [78.0, 76.0, 74.0]
    try:
        while True:
            now = datetime.datetime.now()
            for chan, val in zip(chans, vals):
                writer.write(chan.path, chan.data_type, val, timestamp=now)
            writer.send_buffered_writes()

            time.sleep(0.1)
            vals = [v + random.normalvariate(0, 0.2) for v in vals]
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    _main()
