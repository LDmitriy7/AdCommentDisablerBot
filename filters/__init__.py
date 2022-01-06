import aiogram_utils.filters

from loader import dp
from .misc import *


def setup():
    aiogram_utils.filters.setup(dp)
