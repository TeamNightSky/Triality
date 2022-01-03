"""
Copyright (C) 2021, Zebulon Taylor and Nate Larsen.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
"""

import datetime
import logging
import sys
import typing as t
from dataclasses import asdict

from discord import Color, Embed, Interaction
from discord.commands import ApplicationContext  # type: ignore
from discord.embeds import _EmptyEmbed
from discord.errors import (
    ExtensionAlreadyLoaded,
    ExtensionFailed,
    ExtensionNotFound,
    NoEntryPointError,
)
from discord.ext.commands import Bot  # type: ignore[attr-defined]
from discord.ext.pages import Paginator  # type: ignore[attr-defined]
from discord.ui import Button

from triality import const
from triality.core.manager import StorageManager
from triality.utils import Field


class Triality(Bot):
    log: logging.Logger

    def __init__(self, *args, **kwargs) -> None:
        self.log = logging.getLogger("triality")
        self.setup_logger()
        self.setup_other_loggers()
        super().__init__(*args, **kwargs)

        self.storage = StorageManager(self)
        for extension in const.EXTENSIONS:
            self.log.info(f"Loading {extension}")
            self.init_extension(extension)

        self.log.info("Finished loading bot")

    async def on_ready(self) -> None:
        self.log.info("Logged in as %s ID: %s", self.user, self.user.id)

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
            fmt="[%(asctime)s][%(levelname)s][%(module)s.%(funcName)s]: %(message)s",
            datefmt="%y-%m-%dT%I:%M:%S",
        )
        stdout = logging.StreamHandler(sys.stdout)
        stdout.setFormatter(formatter)
        self.log.addHandler(stdout)
        self.log.setLevel(logging.INFO)

    def setup_other_loggers(self) -> None:
        discord_log = logging.getLogger("discord")
        discord_log.setLevel(logging.DEBUG)

    async def embed_response(
        self,
        ctx: ApplicationContext,
        title: t.Union[str, _EmptyEmbed] = Embed.Empty,
        content: t.Union[str, _EmptyEmbed] = Embed.Empty,
        fields: t.Iterable[Field] = [],
        footer: t.Union[str, _EmptyEmbed] = Embed.Empty,
        image_url: t.Union[str, _EmptyEmbed] = Embed.Empty,
        footer_icon_url: t.Union[str, _EmptyEmbed] = Embed.Empty,
        success: bool = True,
        edit: bool = False,
        follow_up=False,
        dry=False,
    ) -> t.Union[Interaction, Embed]:
        if success:
            color = ctx.user.color
        else:
            color = Color.red()

        embed = Embed(
            color=color,
            title=title,
            description=content,
            timestamp=datetime.datetime.utcnow(),
        )
        embed.set_author(name=self.user.display_name, icon_url=self.user.avatar.url)

        if footer is not None:
            embed.set_footer(text=footer)
        if image_url is not None:
            embed.set_image(url=image_url)

        for field in fields:
            embed.add_field(**asdict(field))
        if dry:
            return embed
        elif edit:
            await ctx.response.edit_message(embed=embed)
            return ctx.interaction
        elif follow_up:
            return await ctx.followup(embed=embed)
        else:
            return await ctx.respond(embed=embed)

    async def page_response(
        self,
        ctx: ApplicationContext,
        pages: t.List[Embed],
        buttons: t.List[Button],
        ephemeral=False,
    ):
        await ctx.defer()
        paginator = Paginator(pages=pages, show_indicator=True, show_disabled=False)
        await paginator.respond(ctx.interaction, ephemeral=ephemeral)
