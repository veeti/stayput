__import__('pkg_resources').declare_namespace(__package__)

from .items import Site, Node
from .templaters import Templater, SimpleTemplater
from .scanners import empty_scanner, filesystem_scanner
from .routers import simple_router