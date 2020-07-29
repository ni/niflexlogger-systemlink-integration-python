"""Get a list of all tags exported by FlexLogger on the local machine."""

import datetime
from typing import Any, Union

from _helpers import get_http_config, get_tag_prefix
from systemlink.clients import tag as sl_tag


def _main() -> None:
    mgr = sl_tag.TagManager(get_http_config())

    print_tags(mgr)


def print_tags(mgr: sl_tag.TagManager, prefix="") -> None:
    """Print FlexLogger tags that have the given prefix.

    By default, no prefix is included, so all FlexLogger tags are printed. To restrict
    it to just tags *exported* by FlexLogger, use prefix="Export.".
    """
    tag_prefix = get_tag_prefix() + "." + prefix
    with mgr.open_selection([tag_prefix + "*"]) as channels:
        # # Uncomment to hide system tags, such as IsTestSessionRunning
        # chan_names = [name for name in chan_names if ".Export.System." not in name]

        # Hide the tag prefix
        chan_names = [name.replace(tag_prefix, "") for name in channels.values]

        if len(chan_names) == 0:
            print("No channels reported to NI SystemLink; check your project settings")
            return

        max_name_len = max(len(name) for name in chan_names)

        def format_row(
            name: str,
            typ: Union[str, None],
            value: Any,
            timestamp: Union[datetime.datetime, str, None],
        ) -> str:
            columns = (
                name.ljust(max_name_len),
                str(timestamp).ljust(32),
                str(typ).ljust(9),
                str(value).ljust(9),
            )
            return " ".join(columns)

        print(format_row("Name", "Type", "Value", "Timestamp"))

        for name in sorted(chan_names, key=str.casefold):
            reader = channels.values[tag_prefix + name]
            read_result = reader.read(include_timestamp=True)
            value = read_result.value if read_result is not None else None
            data_type = read_result.data_type.name if read_result is not None else None
            timestamp = read_result.timestamp if read_result is not None else None

            print(format_row(name, data_type, value, timestamp))


if __name__ == "__main__":
    _main()
