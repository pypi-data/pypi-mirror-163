#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: LiangChao
@email：liang20201101@163.com
@desc: 
"""


class MakitError(Exception):
    """"""

    def __init__(self, *args, **kwargs):
        self.data = kwargs
        super().__init__(*args)


class NotSupportError(MakitError):
    """
    """
