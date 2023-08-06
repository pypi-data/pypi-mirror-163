from __future__ import annotations
from abc import (
    ABCMeta,
    abstractmethod,
)
import codecs
import inspect
import io
import json
import os
import typing as t
from urllib.parse import parse_qs

from .api.base import ApiData
from .asgi import (
    ASGIHTTPEvents,
    WebSocketAccept_t,
    WebSocketClose_t,
    WebSocketRecvMsg_t,
    WebSocketSendMsg_t,
)
from .error import DEFAULT_NOT_FOUND_ERROR
from .http import (
    ContentType,
    DEFAULT_CONTENT_TYPE_PLAIN,
    HTTPMethods,
    HTTPStatus,
    MediaTypes,
    file2mime,
)
from .io import (
    BufferedConcatIterator,
    BufferedFileIterator,
)
from .util.deco import (
    awaitable_property,
    awaitable_cached_property,
    cached_property,
)
from .util.header import make_header


if t.TYPE_CHECKING:
    from .app import (
        AppBase,
        WSGIApp,
        ASGIHTTPApp,
    )

    App_t = t.TypeVar("App_t", bound=AppBase)


class EndpointBase(metaclass=ABCMeta):
    """Base class of Endpoint to define logic to requests.

    Endpoint is one of the core concept of Bamboo, and this class defines
    its basic behavior. All endpoints must inherit this class.

    Note:
        This class is an abstract class. Consider using its subclasses.
    """

    def __init__(
        self,
        app: App_t,
        flexible_locs: t.Tuple[str, ...],
    ) -> None:
        """
        Note:
            DO NOT generate its instance. Its object will be initialized
            by application object.

        Args:
            app: Application object which routes the endpoint.
            flexible_locs: Flexible locations requested.
        """
        self._app = app
        self._flexible_locs = flexible_locs

    def setup(self, *parcel) -> None:
        """Execute setup of the endpoint object.

        This method will execute at initialization of the object by specifying
        parcel. The parcel is sent with `set_parcel()` method of
        the application object which has included the object as one of
        the its endpoints. This method can be used as a substitute for
        the `__init__` method.

        This method is useful in some cases like below:

        - Making an endpoint class a reusable component
        - Injecting environmental dependencies using something like a
            setting file

        Args:
            *parcel: Parcel sent via application object.

        Examples:
            ```python
            app = WSGIApp()

            @app.route("hello")
            class HelloEndpoint(WSGIEndpoint):

                def setup(self, server_name: str) -> None:
                    self._server_name = server_name

                def do_GET(self) -> None:
                    self.send_body(f"Hello from {self._server_name}".encode())

            if __name__ == "__main__":
                SERVER_NAME = "awesome_server"
                app.set_parcel(HelloEndpoint, SERVER_NAME)

                WSGITestExecutor.debug(app, "", 8000)
            ```
        """
        pass

    @property
    def app(self) -> App_t:
        """Application object handling the endpoint.
        """
        return self._app

    @property
    def flexible_locs(self) -> t.Tuple[str, ...]:
        """Flexible locations extracted from requested URI.
        """
        return self._flexible_locs

    @property
    @abstractmethod
    def http_version(self) -> str:
        """HTTP Version on communication.
        """
        pass

    @property
    @abstractmethod
    def scheme(self) -> str:
        """Scheme of requested URI.
        """
        pass

    @abstractmethod
    def get_client_addr(self) -> t.Tuple[t.Optional[str], t.Optional[int]]:
        """Retrieve client address, pair of its IP address and port.

        Note:
            IP address and port may be None if retrieving the address from
            server application would fail, so it is recommended to confirm
            your using server application's spec.

        Returns:
            Pair of IP and port of client.
        """
        pass

    @abstractmethod
    def get_server_addr(self) -> t.Tuple[t.Optional[str], t.Optional[int]]:
        """Retrive server address, pair of its IP address and port.

        Note:
            IP address and port may be None if retrieving the address from
            server application would fail, so it is recommended to confirm
            your using server application's spec.

        Returns:
            Pair of IP and port of server.
        """
        pass

    @abstractmethod
    def get_host_addr(self) -> t.Tuple[t.Optional[str], t.Optional[int]]:
        """Retrive host name and port from requested headers.

        Returns:
            Pair of host name and port.
        """
        pass

    @abstractmethod
    def get_header(self, name: str) -> t.Optional[str]:
        """Retrive header value from requested headers.

        Args:
            name: Header name.

        Returns:
            Value of header if existing, None otherwise.
        """
        pass

    @property
    @abstractmethod
    def path(self) -> str:
        """Path of requested URI.
        """
        pass

    @cached_property
    @abstractmethod
    def queries(self) -> t.Dict[str, t.List[str]]:
        """Query parameters specified to requested URI.
        """
        pass

    def get_queries(self, name: str) -> t.List[str]:
        """Get values of query parameter.

        Args:
            name: Key name of the parameter

        Returns:
            Value of the parameter. The value of list may have multiple
            items if client specifies the parameter in several times.
        """
        query = self.queries.get(name)
        if query:
            return query
        return []

    @cached_property
    @abstractmethod
    def content_type(self) -> t.Optional[ContentType]:
        """Content type of request body.

        Returns:
            Content type if existing, None otherwise.
        """
        pass


class WSGIEndpointBase(EndpointBase):
    """Base class of endpoints compliant with the WSGI.

    This class implements abstract methods of `EndpointBase` with the WSGI.
    However, this class doesn't implement some methods to structure responses.

    Note:
        DO NOT use this class as the super class of your endpoints. Consider
        to use subclasses of the class like `WSGIEndpoint`.
    """

    def __init__(
        self,
        app: WSGIApp,
        environ: t.Dict[str, t.Any],
        flexible_locs: t.Tuple[str, ...],
    ) -> None:
        """
        Args:
            environ: environ variable received from WSGI server.
            flexible_locs: flexible locations requested.
        """
        self._environ = environ
        super().__init__(app, flexible_locs)

    @property
    def environ(self) -> t.Dict[str, t.Any]:
        """environ variable received from WSGI server.
        """
        return self._environ

    @property
    def wsgi_version(self) -> str:
        """WSGI version number.
        """
        version = self._environ.get("wsgi.version")
        return ".".join(map(str, version))

    @property
    def server_software(self) -> str:
        """Software name of WSGI server.
        """
        return self._environ.get("SERVER_SOFTWARE")

    @property
    def http_version(self) -> str:
        version = self._environ.get("SERVER_PROTOCOL")
        return version.split("/")[1]

    @property
    def scheme(self) -> str:
        return self._environ.get("wsgi.url_scheme")

    def get_client_addr(self) -> t.Tuple[t.Optional[str], t.Optional[int]]:
        client = self._environ.get("REMOTE_ADDR")
        port = self._environ.get("REMOTE_PORT")
        if port:
            port = int(port)
        return (client, port)

    def get_server_addr(self) -> t.Tuple[t.Optional[str], t.Optional[int]]:
        server = self._environ.get("SERVER_NAME")
        port = self._environ.get("SERVER_PORT")
        if port:
            port = int(port)
        return (server, port)

    def get_host_addr(self) -> t.Tuple[t.Optional[str], t.Optional[int]]:
        http_host = self._environ.get("HTTP_HOST")
        if http_host:
            http_host = http_host.split(":")
            if len(http_host) == 1:
                return (http_host[0], None)
            else:
                host, port = http_host
                port = int(port)
                return (host, port)
        return (None, None)

    def get_header(self, name: str) -> t.Optional[str]:
        name = name.upper().replace("-", "_")
        if name == "CONTENT_TYPE":
            return self.content_type
        if name == "CONTENT_LENGTH":
            return self._environ.get("CONTENT_LENGTH")

        name = "HTTP_" + name
        return self._environ.get(name)

    @property
    def path(self) -> str:
        return self._environ.get("PATH_INFO")

    @cached_property
    def queries(self) -> t.Dict[str, t.List[str]]:
        return parse_qs(self._environ.get("QUERY_STRING"))

    @cached_property
    def content_type(self) -> t.Optional[ContentType]:
        raw = self._environ.get("CONTENT_TYPE")
        if raw:
            return ContentType.parse(raw)
        return None


class ASGIEndpointBase(EndpointBase):
    """Base class of endpoints compliant with the ASGI.

    This class implements abstract methods of `EndpointBase` with the ASGI.
    However, this class doesn't implement some methods to structure responses.

    Note:
        DO NOT use this class as the super class of your endpoints. Consider
        to use subclasses of the class like `ASGIHTTPEndpoint`.
    """

    def __init__(
        self,
        app: App_t,
        scope: t.Dict[str, t.Any],
        flexible_locs: t.Tuple[str, ...],
    ) -> None:
        """
        Args:
            scope: scope variable received from ASGI server.
            flexible_locs: Flexible locations requested.
        """
        self._scope = scope

        # TODO
        #   Consider not mapping in this method.
        req_headers = scope.get("headers")
        self._req_headers = {}
        if req_headers:
            req_headers = [map(codecs.decode, h) for h in req_headers]
            self._req_headers.update(dict(req_headers))

        super().__init__(app, flexible_locs)

    @property
    def scope(self) -> t.Dict[str, t.Any]:
        """scope variable received from ASGI server.
        """
        return self._scope

    @property
    def scope_type(self) -> str:
        """Scope type on ASGI.
        """
        return self._scope.get("type")

    @property
    def asgi_version(self) -> str:
        """ASGI version.
        """
        return self._scope.get("asgi").get("version")

    @property
    def spec_version(self) -> str:
        """Spec version on ASGI.
        """
        return self._scope.get("asgi").get("spec_version")

    @property
    def raw_path(self) -> bytes:
        """The original HTTP path received from client.
        """
        return self._scope.get("raw_path")

    @property
    def root_path(self) -> str:
        """The root path ASGI application is mounted at.
        """
        return self._scope.get("root_path")

    @property
    def http_version(self) -> str:
        return self._scope.get("http_version")

    @property
    def scheme(self) -> str:
        return self._scope.get("scheme")

    def get_client_addr(self) -> t.Tuple[t.Optional[str], t.Optional[str]]:
        client = self._scope.get("client")
        if client:
            return tuple(client)
        return (None, None)

    def get_server_addr(self) -> t.Tuple[t.Optional[str], t.Optional[str]]:
        server = self._scope.get("server")
        if server:
            return tuple(server)
        return (None, None)

    def get_host_addr(self) -> t.Tuple[t.Optional[str], t.Optional[int]]:
        http_host = self.get_header("host")
        if http_host:
            http_host = http_host.split(":")
            if len(http_host) == 1:
                return (http_host[0], None)
            else:
                host, port = http_host
                port = int(port)
                return (host, port)
        return (None, None)

    def get_header(self, name: str) -> t.Optional[str]:
        name = name.lower().replace("_", "-")
        return self._req_headers.get(name)

    @property
    def headers(self) -> t.Dict[str, str]:
        """Request headers.
        """
        return self._req_headers

    @property
    def path(self) -> str:
        return self._scope.get("path")

    @cached_property
    def queries(self) -> t.Dict[str, t.List[str]]:
        return parse_qs(self._scope.get("query_string").decode())

    @cached_property
    def content_type(self) -> t.Optional[ContentType]:
        raw = self.get_header("Content-Type")
        if raw:
            return ContentType.parse(raw)
        return None


class StatusCodeAlreadySetError(Exception):
    """Raised if response status code has already been set."""
    pass


_AVAILABLE_RES_METHODS = {
    "CONNECT",
    "DELETE",
    "GET",
    "HEAD",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
    "TRACE",
}
_PREFIX_RESPONSE = "do_"
_PREFIX_PRE_RESPONSE = "pre_"


def set_pre_response_method(
    endpoint: t.Type[HTTPMixIn],
    http_method: str,
    callback: t.Callable[[HTTPMixIn], None],
) -> None:
    http_method = http_method.upper()
    if http_method not in HTTPMethods:
        raise ValueError(f"{http_method} is not available as a HTTP method.")

    setattr(endpoint, _PREFIX_PRE_RESPONSE + http_method, callback)
    endpoint._pre_methods[http_method] = callback


def set_response_method(
    endpoint: t.Type[HTTPMixIn],
    http_method: str,
    callback: t.Callable[[HTTPMixIn], None],
) -> None:
    http_method = http_method.upper()
    if http_method not in HTTPMethods:
        raise ValueError(f"{http_method} is not available as a HTTP method.")

    setattr(endpoint, _PREFIX_RESPONSE + http_method, callback)
    endpoint._res_methods[http_method] = callback


class HTTPMixIn(metaclass=ABCMeta):
    """Mixin class for HTTP endpoints.

    This class assumes that endpoint classes inherit this class for HTTP.
    So, this class do not work alone.

    Note:
        DO NOT use this class alone. This class work correctly by inheriting
        it, implementing its abstract methods, and call its `__init__()`
        method in the one of the subclass.
    """
    _pre_methods: t.Dict[str, t.Callable[[HTTPMixIn], None]]
    _res_methods: t.Dict[str, t.Callable[[HTTPMixIn], None]]

    bufsize = 8192

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        cls._pre_methods = {}
        cls._res_methods = {}

        # Check if bufsize is positive
        if not (cls.bufsize > 0 and isinstance(cls.bufsize, int)):
            raise ValueError(
                f"{cls.__name__}.bufsize must be positive integer"
            )

        # Check pre & response methods
        for method in _AVAILABLE_RES_METHODS:
            name_pre_method = _PREFIX_PRE_RESPONSE + method
            name_res_method = _PREFIX_RESPONSE + method

            if hasattr(cls, name_pre_method):
                pre_method = getattr(cls, name_pre_method)
                cls._pre_methods[method] = pre_method

            if hasattr(cls, name_res_method):
                res_method = getattr(cls, name_res_method)
                cls._res_methods[method] = res_method


    @classmethod
    def _get_pre_response_method(
        cls,
        method: str
    ) -> t.Optional[t.Callable[[EndpointBase], None]]:
        """Retrieve pre-response method corresponding with given HTTP method.

        Args:
            method: HTTP method

        Returns:
            Pre-response method with given name.
        """
        return cls._pre_methods.get(method, None)

    @classmethod
    def _get_response_method(
        cls,
        method: str
    ) -> t.Optional[t.Callable[[EndpointBase], None]]:
        """Retrieve response methods with given HTTP method.

        Args:
            method: HTTP method

        Returns:
            Callback with given name.
        """
        return cls._res_methods.get(method, None)

    def __init__(self) -> None:
        self._res_status: t.Optional[HTTPStatus] = None
        self._res_headers: t.List[t.Tuple[str, str]] = []
        self._res_body = BufferedConcatIterator(bufsize=self.bufsize)

    @property
    @abstractmethod
    def content_length(self) -> t.Optional[int]:
        """Content length of request body if existing.
        """
        pass

    @property
    @abstractmethod
    def method(self) -> str:
        """HTTP method requested from client.
        """
        pass

    def add_header(
        self,
        name: str,
        value: str,
        **params: str
    ) -> None:
        """Add response header with MIME parameters.

        Args:
            name: Field name of the header.
            value: Value of the field.
            **params: Directives added to the field.
        """
        self._res_headers.append(make_header(name, value, **params))

    def add_headers(self, *headers: t.Tuple[str, str]) -> None:
        """Add response headers at once.

        Note:
            This method would be used as a shortcut to register multiple
            headers. If it requires adding MIME parameters, developers
            can use the 'add_header' method.

        Args:
            **headers: Header's info whose header is the field name.
        """
        for name, val in headers:
            self.add_header(name, val)

    def add_content_type(self, content_type: ContentType) -> None:
        """Add Content-Type header of response.

        Args:
            content_type: Information of Content-Type header.
        """
        self.add_header(*content_type.to_header())

    def add_content_length(self, length: int) -> None:
        """Add Content-Length header of response.

        Args:
            length: Size of response body.
        """
        self.add_header("Content-Length", str(length))

    def add_content_length_body(self, body: bytes) -> None:
        """Add Content-Length header of response by response body.

        Args:
            body: Response body.
        """
        self.add_header("Content-Length", str(len(body)))

    def _set_status_safely(self, status: HTTPStatus) -> None:
        """Check if response status code already exists.

        Raises:
            StatusCodeAlreadySetError: Raised if response status code has
                already been set.
        """
        if self._res_status:
            raise StatusCodeAlreadySetError(
                "Response status code has already been set."
            )
        self._res_status = status

    def send_only_status(self, status: HTTPStatus = HTTPStatus.OK) -> None:
        """Set specified status code to one of response.

        This method can be used if a callback doesn't need to send response
        body.

        Args:
            status: HTTP status of the response.
        """
        self._set_status_safely(status)

    def send_body(
        self,
        body: t.Union[bytes, t.Iterable[bytes]],
        *others: t.Union[bytes, t.Iterable[bytes]],
        content_type: t.Optional[ContentType] = DEFAULT_CONTENT_TYPE_PLAIN,
        status: HTTPStatus = HTTPStatus.OK
    ) -> None:
        """Set given binary to the response body.

        Note:
            If the parameter `content_type` is specified, then
            the `Content-Type` header is to be added.

            `DEFAULT_CONTENT_TYPE_PLAIN` has its MIME type of `text/plain`,
            and the other attributes are `None`. If another value of
            `Content-Type` is needed, then you should generate new
            `ContentType` instance with attributes you want.

        Args:
            body: Binary to be set to the response body.
            content_type: `Content-Type` header to be sent.
            status: HTTP status of the response.

        Raises:
            StatusCodeAlreadySetError: Raised if response status code has
                already been set.
        """
        self._set_status_safely(status)

        bodies = [body]
        bodies.extend(others)

        is_all_bytes = True
        not_empty = False
        for chunk in bodies:
            is_all_bytes &= isinstance(chunk, bytes)
            if is_all_bytes:
                not_empty |= len(chunk) > 0
            self._res_body.append(chunk)

        if content_type:
            self.add_content_type(content_type)

        # Content-Length if avalidable
        if is_all_bytes and not_empty:
            length = sum(map(len, bodies))
            self.add_content_length(length)

    def send_api(
        self,
        api: ApiData,
        status: HTTPStatus = HTTPStatus.OK,
    ) -> None:
        """Set given api data to the response body.

        Args:
            api: ApiData object to be sent.
            status: HTTP status of the response.

        Raises:
            StatusCodeAlreadySetError: Raised if response status code
                has already been set.
        """
        self.send_body(
            api.__extract__(),
            content_type=api.__content_type__,
            status=status,
        )

    def send_json(
        self,
        body: t.Dict[str, t.Any],
        status: HTTPStatus = HTTPStatus.OK,
        encoding: str = "UTF-8"
    ) -> None:
        """Set given json data to the response body.

        Args:
            body: Json data to be set to the response body.
            status: HTTP status of the response.
            encoding: Encoding of the Json data.

        Raises:
            StatusCodeAlreadySetError: Raised if response status code
                has already been set.
        """
        body = json.dumps(body).encode(encoding=encoding)
        content_type = ContentType(MediaTypes.json, encoding)
        self.send_body(body, content_type=content_type, status=status)

    def send_file(
        self,
        path: str,
        fname: t.Optional[str] = None,
        content_type: str = DEFAULT_CONTENT_TYPE_PLAIN,
        status: HTTPStatus = HTTPStatus.OK
    ) -> None:
        """Set file to be sent as response.

        Args:
            path: File path.
            fname: File name to be sent.
            content_type: Content type of the response.
            status: HTTP status of the response.
        """
        file_iter = BufferedFileIterator(path)
        self.send_body(file_iter, content_type=content_type, status=status)

        length = os.path.getsize(path)
        self.add_header("Content-Length", str(length))
        if fname:
            self.add_header(
                "Content-Disposition",
                "attachment",
                filename=fname
            )


class WSGIEndpoint(WSGIEndpointBase, HTTPMixIn):
    """HTTP endpoint class compliant with the WSGI.

    This class is a complete class of endpoints, communicating on HTTP.
    This class has all attributes of `WSGIEndpointBase` and `HTTPMixIn`,
    and you can define its subclass and use them in your response methods.

    Examples:
        ```python
        app = WSGIApp()

        @app.route("hello")
        class HelloEndpoint(WSGIEndpoint):

            # RECOMMEND to use `data_format` decorator
            def do_GET(self) -> None:
                response = {"greeting": "Hello, Client!"}
                self.send_json(response)

            def do_POST(self) -> None:
                req_body = self.body
                print(req_body)
        ```
    """

    def __init__(
        self,
        app: WSGIApp,
        environ: t.Dict[str, t.Any],
        flexible_locs: t.Tuple[str, ...],
    ) -> None:
        """
        Args:
            app: Application object which routes the endpoint.
            environ: Environ variable received from WSGI server.
            flexible_locs: Flexible locations requested.
        """
        WSGIEndpointBase.__init__(self, app, environ, flexible_locs)
        HTTPMixIn.__init__(self)

    def get_req_body_stream(self) -> io.BufferedIOBase:
        """Fetch the stream with which request body can be received.

        Returns:
            The stream with request body.
        """
        return self._environ.get("wsgi.input")

    def get_req_body_iter(
        self,
        bufsize: int = 8192,
        cache: bool = False,
    ) -> t.Generator[bytes, None, None]:
        """Make an access to the request body as an iterator.

        Note:
            If the flag `cache` is `True`, the request body data is to be
            cached into the property `body`, i.e. one always can access
            to the request body even after the iteration. On the other hand,
            if the `cache` is `False`, caching is not conducted and
            access to the `body` will be failed.

        Args:
            bufsize: Chunk size of each item.
            cache: If the request body is to be cached or not.

        Returns:
            Iterator with binary of the request body.
        """
        stream = self.get_req_body_stream()
        cacher = self.__class__.body
        length = self.content_length
        remain = length

        while True:
            if length is None:
                chunk = stream.read(bufsize)
            elif remain <= 0:
                break
            else:
                counts = remain if remain < bufsize else bufsize
                chunk = stream.read(counts)
                remain -= len(chunk)

            if not chunk:
                break
            yield chunk

            # TODO
            #   Seek more efficient ways
            if cache:
                if cacher._has_cache(self):
                    chunk = cacher._get_cache(self) + chunk

                cacher._set_cache(self, chunk)

    @cached_property
    def body(self) -> bytes:
        """Request body received from client.
        """
        buffer = io.BytesIO()
        for chunk in self.get_req_body_iter():
            buffer.write(chunk)

        buffer.flush()
        data = buffer.getvalue()
        buffer.close()
        return data

    @property
    def content_length(self) -> t.Optional[int]:
        length = self._environ.get("CONTENT_LENGTH")
        if length:
            return int(length)
        return None

    @property
    def method(self) -> str:
        return self._environ.get("REQUEST_METHOD")


class ASGIHTTPEndpoint(ASGIEndpointBase, HTTPMixIn):
    """HTTP endpoint class compliant with the ASGI.

    This class is a complete class of endpoints, communicating on HTTP.
    This class has all attributes of `ASGIEndpointBase` and `HTTPMixIn`,
    and you can define its subclass and use them in your response methods.

    Examples:
        ```python
        app = ASGIHTTPApp()

        @app.route("hello")
        class HelloEndpoint(ASGIHTTPEndpoint):

            # RECOMMEND to use `data_format` decorator
            async def do_GET(self) -> None:
                response = {"greeting": "Hello, Client!"}
                self.send_json(response)

            async def do_POST(self) -> None:
                req_body = async self.body
                print(req_body)
        ```
    """

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()

        # NOTE
        #   All response methods of its subclass must be awaitables.
        for method in HTTPMethods:
            callback = cls._get_response_method(method)
            if callback and not inspect.iscoroutinefunction(callback):
                raise TypeError(
                    f"{cls.__name__}.{callback.__name__} must be an awaitable"
                    ", not a callable."
                )

    def __init__(
        self,
        app: ASGIHTTPApp,
        scope: t.Dict[str, t.Any],
        receive: t.Callable[[], t.Awaitable[t.Dict[str, t.Any]]],
        flexible_locs: t.Tuple[str, ...],
    ) -> None:
        """
        Args:
            app: Application object which routes the endpoint.
            scope: Scope variable received from ASGI server.
            receive: `receive` method given from ASGI server.
            flexible_locs: Flexible locations requested.
        """
        self._receive = receive
        self._is_disconnected = False

        ASGIEndpointBase.__init__(self, app, scope, flexible_locs)
        HTTPMixIn.__init__(self)

    async def get_req_body_iter(
        self,
        bufsize: int = 8192,
        cache: bool = False,
    ) -> t.AsyncGenerator[bytes, None]:
        """Make an access to the request body as an iterator.

        Note:
            If the flag `cache` is `True`, the request body data is to be
            cached into the property `body`, i.e. one always can access
            to the request body even after the iteration. On the other hand,
            if the `cache` is `False`, caching is not conducted and
            access to the `body` will be failed.

        Args:
            bufsize: Chunk size of each item.
            cache: If the request body is to be cached or not.

        Returns:
            Async iterator with binary of the request body.
        """
        buffer = io.BytesIO()
        more_body = True
        cacher = await self.__class__.body

        while more_body:
            chunk = await self._receive()
            type = chunk.get("type")
            if type == ASGIHTTPEvents.disconnect:
                self._is_disconnected = True
                return

            body = chunk.get("body", b"")
            buffer.write(body)
            buffer.flush()
            more_body = chunk.get("more_body", False)

            while buffer.tell() >= bufsize:
                buffer.seek(0)
                item = buffer.read(bufsize)
                yield item

                if cache:
                    # TODO
                    #   Seek more efficient ways
                    if cacher._has_cache(self):
                        item = cacher._get_cache(self) + item

                    cacher._set_cache(self, item)

                rest = buffer.read()
                buffer.close()
                buffer = io.BytesIO(rest)

        # TODO
        #   Seek more efficient ways
        buffer.seek(0)
        item = buffer.read()
        yield item
        if cache:
            if cacher._has_cache(self):
                item = cacher._get_cache(self) + item

            cacher._set_cache(self, item)

        buffer.close()

    @awaitable_cached_property
    async def body(self) -> bytes:
        """Request body received from client.
        """
        buffer = io.BytesIO()
        async for chunk in self.get_req_body_iter():
            buffer.write(chunk)

        buffer.flush()
        data = buffer.getvalue()
        buffer.close()
        return data

    @awaitable_property
    async def is_disconnected(self) -> bool:
        """Whether the connection is closed or not.
        """
        await self.body
        return self._is_disconnected

    @property
    def content_length(self) -> t.Optional[int]:
        length = self.get_header("Content-Length")
        if length:
            return int(length)
        return None

    @property
    def method(self) -> str:
        return self._scope.get("method")


class ASGIWebSocketEndpoint(ASGIEndpointBase):

    @cached_property
    def subprotocols(self) -> t.Tuple[str, ...]:
        return tuple(self._scope.get("subprotocols"))

    async def do_ACCEPT(
        self,
        accept: WebSocketAccept_t,
    ) -> None:
        raise NotImplementedError

    async def do_COMMUNICATE(
        self,
        recvmsg: WebSocketRecvMsg_t,
        sendmsg: WebSocketSendMsg_t,
        close: WebSocketClose_t,
    ) -> None:
        raise NotImplementedError


class StaticEndpoint(EndpointBase):

    def setup(self, doc_root: str) -> None:
        self._filepath = os.path.join(doc_root, *self.path[1:].split("/"))
        self._content_type = ContentType(file2mime(self._filepath))

        if not os.path.isfile(self.filepath) and not os.path.isdir(self.filepath):
            raise DEFAULT_NOT_FOUND_ERROR

    @property
    def filepath(self) -> str:
        return self._filepath

    @property
    def content_type(self) -> ContentType:
        return self._content_type


class StaticWSGIEndpoint(WSGIEndpoint, StaticEndpoint):

    def do_GET(self) -> None:
        self.send_file(self.filepath, content_type=self.content_type)


class StaticRedirectWSGIEndpoint(WSGIEndpoint, StaticEndpoint):

    def setup(self, doc_root: str) -> None:
        super().setup(doc_root)

    def do_GET(self) -> None:
        self.add_header("Location", f"{self.path}index.html")
        self.send_only_status(HTTPStatus.MOVED_PERMANENTLY)


class StaticDownloadWSGIEndpoint(WSGIEndpoint, StaticEndpoint):

    def do_GET(self) -> None:
        self.send_file(
            self.filepath,
            content_type=self.content_type,
            fname=os.path.basename(self.filepath),
        )


class StaticASGIEndpoint(ASGIHTTPEndpoint, StaticEndpoint):

    async def do_GET(self) -> None:
        self.send_file(self.filepath, content_type=self.content_type)


class StaticRedirectASGIEndpoint(ASGIHTTPEndpoint, StaticEndpoint):

    def setup(self, doc_root: str, suffix: str) -> None:
        super().setup(doc_root)

        self._suffix = suffix

    @property
    def suffix(self) -> str:
        return self._suffix

    async def do_GET(self) -> None:
        self.add_header("Location", f"{self.path}{self.suffix}")
        self.send_only_status(HTTPStatus.MOVED_PERMANENTLY)


class StaticDownloadASGIEndpoint(ASGIHTTPEndpoint, StaticEndpoint):

    async def do_GET(self) -> None:
        self.send_file(
            self.filepath,
            content_type=self.content_type,
            fname=os.path.basename(self.filepath),
        )
