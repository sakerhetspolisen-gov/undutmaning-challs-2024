#!/usr/bin/env python3
import numpy as np
import sys

SPACE   = 700
MARK    = 800
DIT     = (MARK,)
DAH     = (MARK, MARK, MARK)
CHARSEP = (SPACE, SPACE, SPACE) 
WORDSEP = (SPACE, SPACE, SPACE, SPACE, SPACE, SPACE, SPACE)

def ch(*args):
  return sum([[*i, SPACE] for i in args], [])[:-1]

syms = {
  "a": ch(DIT, DAH),
  "b": ch(DAH, DIT, DIT, DIT),
  "c": ch(DAH, DIT, DAH, DIT),
  "d": ch(DAH, DIT, DIT),
  "e": ch(DIT),
  "f": ch(DIT, DIT, DAH, DIT),
  "g": ch(DAH, DAH, DIT),
  "h": ch(DIT, DIT, DIT, DIT),
  "i": ch(DIT, DIT),
  "j": ch(DIT, DAH, DAH, DAH),
  "k": ch(DAH, DIT, DAH),
  "l": ch(DIT, DAH, DIT, DIT),
  "m": ch(DAH, DAH),
  "n": ch(DAH, DIT),
  "o": ch(DAH, DAH, DAH),
  "p": ch(DIT, DAH, DAH, DIT),
  "q": ch(DAH, DAH, DIT, DAH),
  "r": ch(DIT, DAH, DIT),
  "s": ch(DIT, DIT, DIT),
  "t": ch(DAH),
  "u": ch(DIT, DIT, DAH),
  "v": ch(DIT, DIT, DIT, DAH),
  "w": ch(DIT, DAH, DAH),
  "x": ch(DAH, DIT, DIT, DAH),
  "y": ch(DAH, DIT, DAH, DAH),
  "z": ch(DAH, DAH, DIT, DIT),
  "0": ch(DAH, DAH, DAH, DAH, DAH),
  "1": ch(DIT, DAH, DAH, DAH, DAH),
  "2": ch(DIT, DIT, DAH, DAH, DAH),
  "3": ch(DIT, DIT, DIT, DAH, DAH),
  "4": ch(DIT, DIT, DIT, DIT, DAH),
  "5": ch(DIT, DIT, DIT, DIT, DIT),
  "6": ch(DAH, DIT, DIT, DIT, DIT),
  "7": ch(DAH, DAH, DIT, DIT, DIT),
  "8": ch(DAH, DAH, DAH, DIT, DIT),
  "9": ch(DAH, DAH, DAH, DAH, DIT),
  "?": ch(DIT, DIT, DAH, DAH, DIT, DIT),
}

def tok2freq(t):
  return syms[t] if t in syms else syms['?']

def word2freq(s):
  result = []
  for f in sum([[*tok2freq(tok), "CHARSEP"] for tok in s], [])[:-1]:
    if f == "CHARSEP":
      result += CHARSEP
    else:
      result.append(f)
  return result

def words2freq(s):
  result = []
  for f in sum([[*word2freq(word), "WORDSEP"] for word in s.lower().split(" ")], [])[:-1]:
    if f == "WORDSEP":
      result += WORDSEP
    else:
      result.append(f)
  return result

# fsksignal, noise produces normalized iq data (range [-1,1])

def fsksignal(states, time_unit_s, sample_rate_hz):
  samples_per_time_unit = sample_rate_hz * time_unit_s
  nsamples              = len(states) * samples_per_time_unit
  ts                    = np.arange(nsamples) * 1/sample_rate_hz
  fs                    = np.repeat(states, samples_per_time_unit)
  samples               = np.empty((int(nsamples), 2))
  samples[:,0]          = np.cos(2*np.pi*fs*ts)
  samples[:,1]          = np.sin(2*np.pi*fs*ts)
  return samples

def noise(nsamples):
  samples        = np.empty((int(nsamples), 2))
  samples[:,0]   = np.random.normal(size=int(nsamples))
  samples[:,1]   = np.random.normal(size=int(nsamples))
  return samples

if __name__ == "__main__":
  if len(sys.argv) != 3:
    print("usage: {} <flag> <to-path>".format(sys.argv[0]), file=sys.stderr)
    sys.exit(1)
  flag = ''.join(ch if ch in syms or ch == " " else "?" for ch in sys.argv[1].lower())
  path = sys.argv[2]
  
  sample_rate_hz = 4000
  scale_signal   = 0.0005
  scale_noise    = 0.0001
  signal = fsksignal(words2freq(" " + flag + " "), 0.1, sample_rate_hz)
  data = (signal*scale_signal + noise(signal.shape[0])*scale_noise) / 2
  data.astype('float32').tofile(path)
  if flag != sys.argv[1].lower():
    print("WARN: Unmapped symbols in flag replaced with '?'",
        file=sys.stderr)
  print("flag '{}' written to {}".format(flag, path), file=sys.stderr)

