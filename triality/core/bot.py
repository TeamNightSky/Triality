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
    extensions: t.List[str] = [
        "triality.core.cogs.money",
        "triality.core.cogs.items",
        "triality.core.cogs.sudo",
    ]

    def __init__(self, *args, **kwargs) -> None:
        self.log = logging.getLogger("triality")
        self.setup_logger()
        self.setup_other_loggers()
        super().__init__(*args, **kwargs)

        self.storage = StorageClient(self)
        for extension in self.extensions:
            self.init_extension(extension)

        self.log.info("Finished loading bot")

    async def on_ready(self) -> None:
        print("Logged in as", self.user, "ID:", self.user.id)

    def init_extension(self, ext: str) -> None:
        try:
            self.load_extension(ext)
            self.log.info("Loaded %s", ext)
        except (
            ExtensionNotFound,
            ExtensionAlreadyLoaded,
            NoEntryPointError,
            ExtensionFailed,
        ) as error:
            self.log.critical("Error loading extension", exc_info=error)

    def setup_logger(self) -> None:
        formatter = logging.Formatter(
            fmt="[%(asctime)s][%(levelname)s][%(module)s.%(funcName)s]: %(message)s",
            datefmt="%y-%m-%dT%I:%M:%S",
        )
        stdout = logging.StreamHandler(sys.stdout)
        stdout.setFormatter(formatter)
        self.log.addHandler(stdout)
        self.log.setLevel(logging.INFO)
        self.log.propagate = False

    def setup_other_loggers(self) -> None:
        discord_log = logging.getLogger("discord")
        discord_log.setLevel(logging.CRITICAL)
