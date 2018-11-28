from gnuradio import gr
from cdma import cdmagen, cdmarx, rrc_filter, cpfsk
from gnuradio import blocks

import matplotlib.pyplot as plt
import numpy as np
from time import sleep

class MyRadio (gr.top_block):
    def __init__ (self):
        gr.top_block .__init__(self, "TEST")
        bitstream = [1, 0, 0, 1, 0, 1]
        cdma_code=[1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, -1, -1 ]

        self.cdma_rx = cdmarx(len(bitstream))
        self.cdmagenerator = cdmagen (cdma_code)
        self.rrc_stream = blocks.vector_to_stream(np.dtype(np.float32).itemsize, len(cdma_code) * len(bitstream))
        self.rrc_filt = rrc_filter(500000, .0001, 1, len(bitstream))
        self.vector_source = blocks.vector_source_b(data=bitstream,repeat=False, vlen=1)
        self.vector_to_stream = blocks.vector_to_stream(1, 1)
        self.vector_to_stream2 = blocks.vector_to_stream(np.dtype(np.float32).itemsize, len(bitstream) * 32)
        self.vector_to_stream3 = blocks.vector_to_stream(32*32, 32)
        self.stream_to_vector = blocks.stream_to_vector(np.dtype(np.int8).itemsize, 32)
        self.cpfsk_gen = cpfsk()


        self.connect (self.vector_source, self.vector_to_stream)
        self.connect (self.vector_to_stream, self.cdmagenerator)
        self.connect (self.cdmagenerator, self.rrc_filt)
        self.connect (self.rrc_filt, self.cdma_rx)
    
    def getResultData(self):
        return self.rrc_filt.data

if __name__ == '__main__':
    test = MyRadio()
    edges= test.edge_list()
    test.start()
    sleep(1)
    test.stop()
    test.wait()
    print (test.getResultData())
    plt.plot(test.getResultData())
    plt.show()