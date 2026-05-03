from .context_processors import register_context_processors
from .errors import register_error_handlers
from .filters import register_template_filters

__all__ = [
    "register_context_processors",
    "register_error_handlers",
    "register_template_filters",
]
