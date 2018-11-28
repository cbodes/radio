

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


class cpfsk(gr.basic_block):
    """
    docstring for block cpfsk
    """
    data = np.array([])

    def __init__(self, sample_rate, w_bandwidth, w_carrier):
        gr.basic_block.__init__(self,
                                name="cpfsk",
                                in_sig=[np.float32],
                                out_sig=[np.complex64])
        self.w_b = w_bandwidth * np.pi
        self.w_c = w_carrier * np.pi * 2.
        self.amplitude = 1.
        self.cur_phase = 0.
        self.cur_t = 0.
        self.smpl_rate = sample_rate
        self.prev_freq = 0.
        self.tstep = 1. / self.smpl_rate

    def forecast(self, noutput_items, ninput_items_required):
        # setup size of input_items[i] for work call
        for i in range(len(ninput_items_required)):
            ninput_items_required[i] = noutput_items

    def general_work(self, input_items, output_items):
        in0 = input_items[0][0]
        myFreq = (in0 * self.w_b + self.w_c)
        self.cur_phase = self.cur_phase + (self.cur_t * (self.prev_freq - myFreq))
        mySample = self.amplitude * np.exp(1j * (myFreq * self.cur_t + self.cur_phase))
        output_items[0][:1] = mySample
        self.data = np.append(self.data, mySample)
        self.cur_t += self.tstep
        self.prev_freq = myFreq
        self.consume(0, 1)
        return 1
        # output_items[0][:] = np.exp(input_items[0][:len(output_items[0])] * 1j)
        # self.consume(0, len(output_items[0]))
        # return len(output_items[0])


# !/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018 <+YOU OR YOUR COMPANY+>.

# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.


# import numpy as np
# from gnuradio import gr


# class cpfsk(gr.basic_block):
#     """
#     docstring for block cpfsk
#     """
#     data = np.array([])

#     def __init__(self, sample_rate, w_bandwidth, w_carrier):
#         gr.basic_block.__init__(self,
#                                 name="cpfsk",
#                                 in_sig=[np.float32],
#                                 out_sig=[gr.gr_vector_complexf])
#         self.w_b = w_bandwidth * np.pi * 2.
#         self.w_c = w_carrier * np.pi * 2.
#         self.amplitude = 1
#         self.cur_phase = 0
#         self.cur_t = np.float32(0)
#         self.smpl_rate = sample_rate
#         self.prev_freq = 0
#         self.tstep = 1. / self.smpl_rate
#         self.times = np.arange(0, 4096 * self.tstep, self.tstep)

#     def forecast(self, noutput_items, ninput_items_required):
#         # setup size of input_items[i] for work call
#         for i in range(len(ninput_items_required)):
#             ninput_items_required[i] = noutput_items

#     def general_work(self, input_items, output_items):
#         output_items[0][:] = input_items[0][:len(output_items[0])] * 1j
#         self.data = np.append(self.data, input_items[0][:len(output_items[0])])
#         self.consume(0, len(output_items[0]))
#         return len(output_items[0])
