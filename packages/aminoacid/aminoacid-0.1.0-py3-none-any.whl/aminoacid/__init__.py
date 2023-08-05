#!/usr/bin/env python
from __future__ import annotations

import asyncio
from functools import wraps
from importlib.util import find_spec
from logging import Logger, getLogger
from shlex import split
from time import asctime
from typing import Any, Callable, Coroutine, Dict, Optional, TypeVar

from aiohttp import ClientResponse, ClientSession

from ._socket import SocketClient
from .abc import Context, Message, User
from .client import ApiClient
from .exceptions import CommandNotFound
from .util import (
    HelpCommand,
    UserCommand,
    __version__,
    deserialize_session,
    get_headers,
    json,
)

__author__ = "okok7711"

_ORJSON = find_spec("orjson")

T = TypeVar("T")

json_serialize = (
    lambda obj, *args, **kwargs: json.dumps(obj).decode()
    if _ORJSON
    else json.dumps(obj)
)


class Bot(ApiClient):
    r"""Bot client class, this is the interface for doing anything

    Parameters
    ----------
    key : bytes
        The key to use for signing requests. This has to be supplied in kwargs otherwise the Bot will not work
    device : str
        The deviceId to use. This is also needed for the bot to run
    prefix : str, optional
        The prefix the bot should listen to. By default "/"
    help_command : UserCommand, optional
        The help_command to use, if not supplied a standard Help Command will be used.
    v : bytes, optional
        The version of the signing algorithm. This is currently \x42
    session : str, optional
        If given, the bot will not auth via login but will use the given session instead
    """
    loop: asyncio.AbstractEventLoop
    profile: User

    def __init__(
        self, prefix: str = "/", help_command: Optional[UserCommand] = None, **kwargs
    ) -> None:
        self.prefix = prefix
        self.__command_map__: Dict[str, UserCommand] = {
            "help": help_command or HelpCommand()
        }
        self.events: Dict[str, Callable[..., Coroutine[Any, Any, T]]] = {}
        self.logger = getLogger(__name__)
        self._http = HttpClient(logger=self.logger, **kwargs)
        super().__init__()

    def command(self, name=""):
        """Wrapper to register commands to the bot

        Parameters
        ----------
        name : str, optional
            Name that the command should listen on, by default the name of the function
        """

        def wrap(f: Callable):
            @wraps(f)
            def func(*args, **kwargs):
                if (name or f.__name__) in self.__command_map__:
                    return
                self.__command_map__[name or f.__name__] = UserCommand(
                    func=f, command_name=name
                )

            return func()

        return wrap

    def event(self, name=""):
        """Wrapper to add events the bot should listen to

        Parameters
        ----------
        name : str, optional
            Name that the event should listen on, by default the name of the function
        """
        # TODO: Add list of available events for documentation

        def wrap(f: Callable):
            @wraps(f)
            def func(*args, **kwargs):
                if (name or f.__name__) in self.events:
                    return
                self.events[name or f.__name__] = f

            return func()

        return wrap

    def run(
        self,
        email: Optional[str] = "",
        password: Optional[str] = "",
        *,
        session: str = "",
        **kwargs,
    ):
        """Run the `main_loop()` of the bot and initiate authentication

        Parameters
        ----------
        email : str, optional
            email of the account to use
        password : str, optional
            password of the account to use
        session : str, optional
            session to use instead of email password combination
        """
        if not any((email, password, session)):
            raise Exception("No Auth")
        self.loop = asyncio.get_event_loop()
        self.loop.run_until_complete(
            self.main_loop(email=email, password=password, session=session)
        )

    async def main_loop(
        self,
        email: Optional[str],
        password: Optional[str],
        *,
        session: Optional[str] = "",
    ):
        """Main loop of the Bot, this authenticates and sets the session

        Parameters
        ----------
        email : Optional[str]
            Email of the account to login
        password : Optional[str]
            Password of the account to login
        session : Optional[str], optional
            Session of the Account, by default ""
        """
        if not session:
            await self.login(email=email, password=password)
        else:
            self._http.session = f"sid={session}"
            self.profile = await self.fetch_user(deserialize_session(session)["2"])
        sock = SocketClient(self)
        try:
            await sock.run_loop()
        finally:
            await self.cleanup_loop()

    async def handle_command(self, message: Message):
        """Handles a command for the supplied message

        Parameters
        ----------
        message : Message
            The message to handle
        """
        if not message.startswith(self.prefix):
            return
        args = split(message.content[len(self.prefix) :])
        if args[0] in self.__command_map__:
            await self.__command_map__[args.pop(0)](
                Context(client=self, message=message), *args
            )
        else:
            print(self.__command_map__)
            self.logger.exception(CommandNotFound(message))

    async def cleanup_loop(self):
        """Cleans up, closes sessions, etc."""
        # TODO: maybe make better cleanup
        await self._http.close()


class HttpClient(ClientSession):
    session: str

    def __init__(self, logger: Logger, *args, **kwargs) -> None:
        self.base: str = kwargs.pop("base_uri", "https://service.narvii.com/api/v1")
        self.key: bytes = kwargs.pop(
            "key",
        )
        self.device: str = kwargs.pop(
            "device",
        )
        self.v: bytes = kwargs.pop("v", b"\x42")

        self.logger = logger

        self.session = ""
        super().__init__(*args, **kwargs, json_serialize=json_serialize)

    async def request(self, method: str, url: str, *args, **kwargs) -> ClientResponse:
        """Execute a request

        Parameters
        ----------
        method : str
            Method of the request
        url : str
            url to be appended to the base

        Returns
        -------
        ClientResponse
            Response the server returned
        """

        headers = kwargs.pop("headers", {}) or get_headers(
            data=json_serialize(kwargs.get("json", {})).encode(),
            device=self.device,
            key=self.key,
            v=self.v,
        )
        if self.session:
            headers["NDCAUTH"] = self.session
        response = await super().request(
            method,
            url=(self.base + url if not "wss" in url else url),
            headers=headers,
            *args,
            **kwargs,
        )
        self.log_request(response, self.logger)
        return response

    @staticmethod
    def log_request(response: ClientResponse, logger: Logger) -> None:
        """Logs a request and its response with info level

        Parameters
        ----------
        response : ClientResponse
            the response object that the request returned
        """
        logger.info(
            f"{response.request_info.method} [{asctime()}] -> {response.url}: {response.status} [{response.content_type}] "
            f"Received Headers: {response.headers}, Sent Headers: {response.request_info.headers}"
        )
