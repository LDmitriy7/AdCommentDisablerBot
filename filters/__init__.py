import aiogram_utils.filters
import aiogram_utils.filters

from .is_forwarded_from_linked_channel import *


def setup():
    aiogram_utils.filters.setup(dp)
