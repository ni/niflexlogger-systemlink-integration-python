"""Create a FlexLogger output channel and watch for value changes made in the FlexLogger GUI."""

import sys
import time
from typing import List, Optional

from _helpers import get_http_config, get_tag_prefix
from systemlink.clients import tag as sl_tag


def _main(*args: str) -> int:
    if len(args) != 2:
        print('Usage: python {} "CHANNEL GROUP" "CHANNEL NAME"'.format(sys.argv[0]))
        return 2

    mgr = sl_tag.TagManager(get_http_config())

    channel_tag = create_output_channel(mgr, args[0], args[1], sl_tag.DataType.DOUBLE)

    print("Created output channel; watching for updates")
    print(" * Hit Ctrl-C to exit")
    print()

    # Read the initial value.
    reader = mgr.get_tag_reader(channel_tag.path, channel_tag.data_type)
    read_result = reader.read()

    value = read_result.value if read_result is not None else None
    print("Initial value is {}".format(value))

    # The value can be set, too. But usually it will just be set from within FlexLogger.
    # In fact, as soon as FlexLogger finishes creating the tag, it'll set its value back
    # to 0.0.
    target_value = 2.0
    print("Changing value to {}".format(target_value))
    writer = mgr.create_writer(buffer_size=10)
    writer.write(channel_tag.path, channel_tag.data_type, target_value)
    writer.send_buffered_writes()

    # We can also watch for changes to any tag value.
    wait_forever_for_tag_changes(mgr, [channel_tag])

    return 0


def create_output_channel(
    mgr: sl_tag.TagManager, group: str, name: str, data_type: sl_tag.DataType
) -> sl_tag.TagData:
    """Create a FlexLogger output channel."""
    # "Import" the channel into FlexLogger.
    full_name = get_tag_prefix() + ".Import.Setpoint.{}.{}".format(group, name)
    mgr.open(full_name, data_type, create=True)

    # Once FlexLogger creates the channel, we'll interact with it as an "export" channel
    # (for both reads and writes).
    full_name = get_tag_prefix() + ".Export.Setpoint.{}".format(name)
    # Go ahead and pre-create the output channel, for ease-of-use. Otherwise, when
    # trying to read its value, we'd have to be prepared for an ApiException complaining
    # that the tag doesn't exist.
    mgr.open(full_name, data_type, create=True)
    return sl_tag.TagData(full_name, data_type)


def wait_forever_for_tag_changes(
    mgr: sl_tag.TagManager, tags: List[sl_tag.TagData]
) -> None:
    """Watch for tag changes, and print any updates to the console.

    This method will never return.
    """

    def on_tag_changed(
        tag: sl_tag.TagData, reader: Optional[sl_tag.TagValueReader]
    ) -> None:
        if reader is not None:
            read_result = reader.read()
            value = read_result.value if read_result is not None else None
            print("Value changed to {}".format(value))

    with mgr.create_selection(tags) as selection:
        with selection.create_subscription() as subscription:
            subscription.tag_changed += on_tag_changed

            try:
                while True:
                    time.sleep(100)
            except KeyboardInterrupt:
                return


if __name__ == "__main__":
    sys.exit(_main(*sys.argv[1:]))
