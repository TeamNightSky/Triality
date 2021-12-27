import logging
import sys
import typing as t

from discord import (
    ExtensionAlreadyLoaded,
    ExtensionFailed,
    ExtensionNotFound,
    NoEntryPointError,
)
from discord.ext.commands import Bot  # type: ignore[attr-defined]

from .storage import StorageClient


class Triality(Bot):
    log: logging.Logger
    extensions: t.List[str] = []

    def __init__(self, *args, **kwargs) -> None:
        self.log = logging.getLogger("triality")
        self.setup_logger()
        self.setup_other_loggers()
        super().__init__(*args, **kwargs)

        self.storage = StorageClient(self)
        for extension in self.extensions:
            self.init_extension(extension)

    async def on_ready(self):
        items = await self.storage.all_items()
        print(items)

    def init_extension(self, ext: str) -> None:
        try:
            self.load_extension(ext)
        except (
            ExtensionNotFound,
            ExtensionAlreadyLoaded,
            NoEntryPointError,
            ExtensionFailed,
        ) as error:
            self.log.critical("Error loading extension", exc_info=error)

    def setup_logger(self) -> None:
        formatter = logging.Formatter(
            fmt="[%(asctime)s][%(levelname)s][%(module)6s.%(funcName)-8s]: %(message)s",
            datefmt="%y-%m-%dT%I:%M:%S",
        )
        stdout = logging.StreamHandler(sys.stdout)
        stdout.setFormatter(formatter)
        self.log.addHandler(stdout)
        self.log.setLevel(logging.DEBUG)
        self.log.propagate = False

    def setup_other_loggers(self) -> None:
        discord_log = logging.getLogger("discord")
        discord_log.setLevel(logging.CRITICAL)
