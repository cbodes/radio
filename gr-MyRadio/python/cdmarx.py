#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2018 <+YOU OR YOUR COMPANY+>.
#
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
#

import numpy as np
from gnuradio import gr


class cdmarx(gr.basic_block):
    """
    docstring for block cdmarx
    """
    data = []

    def __init__(self, cdmaCode):
        gr.basic_block.__init__(self,
                                name="cdmarx",
                                in_sig=[np.int8],
                                out_sig=None)
        self.cdma_code = np.tile(cdmaCode, 4096)
        self.total_errors = 0
        self.total_samples = 0

    def general_work(self, input_items, output_items):
        in0 = input_items[0]
        curMax = np.sum(np.logical_and(in0, self.cdma_code[:len(in0)]))
        for i in range(1, 5, 1):
            curSum = np.sum(np.logical_and(in0, self.cdma_code[i:i+len(in0)]))
            if (curSum < curMax):
                curMax = curSum
        self.total_errors += len(in0) - curMax
        self.total_samples += len(in0)
        #print self.total_errors / self.total_samples
        print in0
        self.consume_each(len(in0))
        return 0
