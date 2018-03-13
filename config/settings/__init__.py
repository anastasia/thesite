try:
    from .settings import *
except ImportError as e:
    raise Exception("Settings not found")
