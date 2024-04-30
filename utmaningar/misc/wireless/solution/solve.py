#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import sys

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print("usage: {} <in-path> <out-path>".format(sys.argv[0]))
    sys.exit(1)
  inpath   = sys.argv[1]
  outpath  = sys.argv[2]
  data     = np.fromfile(inpath, dtype=np.complex64)
  vmin     = 20*np.log10(np.max(data).real) - 13
  plt.specgram(data, mode="magnitude", Fs=4000, NFFT=512, noverlap=256, vmin=vmin)
  plt.ylabel("Frequency [Hz]")
  plt.xlabel("Time [s]")
  plt.savefig(outpath, dpi=160)

