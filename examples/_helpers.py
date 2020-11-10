"""Helpers for reading FlexLogger data via the local NI SystemLink web API."""

import os
import pathlib

import systemlink.clients.core as sl_core


__all__ = ["ApiException", "get_http_config", "get_tag_prefix"]

ApiException = sl_core.ApiException

__tag_prefix = None


def get_http_config() -> sl_core.HttpConfiguration:
    """Get an HttpConfiguration class for use when constructing a TagManager.

    FlexLogger specifically requires a localhost config, for performance reasons.
    """
    try:
        return sl_core.HttpConfigurationManager.get_configuration(
            sl_core.HttpConfigurationManager.HTTP_LOCALHOST_CONFIGURATION_ID
        )
    except ApiException as ex:
        raise ApiException(
            "FlexLogger requires a local NI SystemLink install and the NI Web Server running on localhost",
            inner=ex,
        ) from None


def get_tag_prefix() -> str:
    """Get the tag path prefix used by FlexLogger on this machine.

    The tag path format will be f"{prefix}.Export.**" or f"{prefix}.Import.**", etc.
    """
    global __tag_prefix
    if __tag_prefix is not None:
        return __tag_prefix

    if os.name == "nt":
        from systemlink.clients.core._internal import _winpaths

        # Get the ProgramData directory. NI SystemLink has a handy internal library for
        # querying this value from the Windows API.
        programdata_dir = pathlib.Path(
            _winpaths.get_path(_winpaths.FOLDERID.ProgramData)
        )
        minion_id_file = programdata_dir / "National Instruments/salt/conf/minion_id"
    else:
        minion_id_file = pathlib.Path("/etc/salt/minion_id")

    if minion_id_file.exists():
        __tag_prefix = minion_id_file.open().read().strip() + ".FlexLogger"
    else:
        __tag_prefix = ".FlexLogger"

    return __tag_prefix
