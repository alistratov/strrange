import unittest
import time

from strrange import range as sr
from .decorators import loading_tests_enabled

"""
1. Alphabets not cached, 100_000 passes

Load testing... 800000 samples
Range ('A', 'Z')                                  :      0.686s   145858.4 ops/s
Range ('-50', '+50')                              :      0.175s   571484.5 ops/s
Range ('file001.txt', 'file100.txt')              :      0.555s   180315.4 ops/s
Range ('qaa', 'qtz')                              :      0.803s   124572.9 ops/s
Range ('A', 'ZZ')                                 :      0.718s   139222.5 ops/s
Range ('A0z', 'Z9z')                              :      1.015s    98477.5 ops/s
Range ('v1.0.0', 'v1.0.99')                       :      0.473s   211513.1 ops/s
Range ('x--', 'x------------------------')        :      0.788s   126840.8 ops/s
Ran 1 test in 5.213s

2. Cached alphabets, 100_000 passes

Load testing... 800000 samples
Range ('A', 'Z')                                  :      0.522s   191493.0 ops/s
Range ('-50', '+50')                              :      0.176s   569262.5 ops/s
Range ('file001.txt', 'file100.txt')              :      0.567s   176506.1 ops/s
Range ('qaa', 'qtz')                              :      0.649s   154046.8 ops/s
Range ('A', 'ZZ')                                 :      0.562s   178060.3 ops/s
Range ('A0z', 'Z9z')                              :      0.826s   121016.7 ops/s
Range ('v1.0.0', 'v1.0.99')                       :      0.478s   209038.3 ops/s
Range ('x--', 'x------------------------')        :      0.780s   128287.3 ops/s
Ran 1 test in 4.560s
"""


class LoadingStrRange(unittest.TestCase):
    @loading_tests_enabled
    def test_samples(self):
        PASSES = 100_000
        SAMPLES = [
            ('A', 'Z'),
            ('-50', '+50'),
            ('file001.txt', 'file100.txt'),
            ('qaa', 'qtz'),
            ('A', 'ZZ'),
            ('A0z', 'Z9z'),
            ('v1.0.0', 'v1.0.99'),
            ('x--', 'x------------------------'),
        ]

        print(f'Load testing... {PASSES * len(SAMPLES)} samples')
        for a, b in SAMPLES:
            t1 = time.perf_counter()

            for _p in range(PASSES):
                # list(sr(a, b))
                t = sr(a, b)
                # Get only the first and last elements to force evaluation
                _ = next(iter(t))

            t2 = time.perf_counter()
            title = f'Range ({a!r}, {b!r})'
            print(f'{title:50}: {t2 - t1:10.3f}s {PASSES / (t2 - t1):10.1f} ops/s')
