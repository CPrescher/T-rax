# -*- coding: utf8 -*-
__author__ = 'Clemens Prescher'

from .BaseModel import SingleSpectrumModel


class DiamondModel(SingleSpectrumModel):
    def __init__(self):
        super(DiamondModel, self).__init__()
