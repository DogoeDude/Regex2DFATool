# coding=utf-8
"""**Random DFA generation (alternative version in python)**

ICDFA Random generation binding

.. *Authors:* Rogério Reis & Nelma Moreira

.. *This is part of FAdo project*  http://fado.dcc.fc.up.pt

.. *Version:* 1.0

.. *Copyright:* 1999-2014 Rogério Reis & Nelma Moreira {rvr,nam}@dcc.fc.up.pt

.. versionadded:: 1.0

..  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; if not, write to the Free Software
  Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA."""

import random
import time
from . import common
from . import fa


class ICDFArgen(object):
    """Generic ICDFA random generator class

    :var int n: number of states
    :var int k: size of the alphabet
    :var int pn: how more problable shall a non defined transition be?
    :var int seed: seed for the random generator. Default is to generate a time & system dependent.

    .. seealso:: Marco Almeida, Nelma Moreira, and Rogério Reis. Enumeration and generation with a string automata
       representation. Theoretical Computer Science, 387(2):93-102, 2007

    .. versionchanged:: 1.3.4 seed added to the random generator"""

    def __init__(self, n, k, nd=False, pn=1, seed=0):
        self.N = dict()
        self.n = n
        self.k = k
        if seed != 0:
            self.seed = seed
        else:
            if not common.PyPy:
                self.seed = hash(time.clock_gettime_ns(time.CLOCK_MONOTONIC_RAW))
            else:
                self.seed = hash( time.perf_counter())
        foo = n ** k
        random.seed(self.seed)
        if not nd:
            self.pn = 0
        else:
            self.pn = pn
        for j in range((n - 1) * k - 1, n - 3, -1):
            self.N[(n - 1, j)] = foo
            foo *= n
        for m in range(n - 2, 0, -1):
            foo = 0
            bar = 1
            m1 = m + 1
            for i in range(0, k):
                foo += bar * self.N[(m + 1, m * k + i)]
                bar *= m1
            self.N[(m, m * k - 1)] = foo
            for i in range(m * k - 2, m - 2, -1):
                self.N[(m, i)] = m1 * self.N[(m, i + 1)] + self.N[(m + 1, i + 1)]

    def __iter__(self):
        return self

    def genFinalities(self):
        """ Generate bit map of final states

        :rtype: list
        """
        return [random.randint(0, 1) for _ in range(self.n)]

    def _getFlag(self, m, l):
        k = self.k
        bar = 1
        foo = 0
        for i in range(l, m * k):
            foo += bar * self.N[(m, i)]
            bar *= m
        r = random.randint(0, foo)
        bar = 1
        for i in range(l, m * k):
            foo = bar * self.N[(m, i)]
            if r < foo:
                return i
            else:
                r -= foo
                bar *= m
        return m * k - 1

    def _rndT(self, i):
        r = random.randint(0, i + self.pn - 1)
        if r < self.pn:
            return -1
        else:
            return r - self.pn

    def __next__(self):
        """ Generate an ICDFA
        """
        g = -1
        s = []
        for i in range(1, self.n):
            flag = self._getFlag(i, g + 1)
            for j in range(g + 1, flag):
                s.append(self._rndT(i))
            s.append(i)
            g = flag
        for i in range(g + 1, self.n * self.k):
            s.append(self._rndT(self.n))
        return fa.stringToDFA(s, self.genFinalities(), self.n, self.k)

    def next(self):
        return self.__next__()

class ICDFArnd(ICDFArgen):
    """ Complete ICDFA random generator class

    This is the class for the uniform random generator for Initially Connected DFAs

    :var int n: number of states
    :var int k: size of alphabet
    :var int seed: seed for the random generator (if 0 uses time as seed)

    .. note::
        This is an abstract class, not to be used directly

    .. versionchanged:: 1.3.4 seed added to the random generator"""

    def __init__(self, n, k, seed=0):
        super(ICDFArnd, self).__init__(n, k, False, 1, seed)

    def __str__(self):
        return "ICDFArnd %d %d %d" % (self.n, self.k, self.seed)


class ICDFArndIncomplete(ICDFArgen):
    """ Incomplete ICDFA random generator class

    :var int n: number of states
    :var int k: size of alphabet
    :var float bias: how often must the gost sink state appear (default None)
    :var int seed: seed for the random generator (if 0 uses time as seed)


    :raises IllegalBias: if a bias >=1 or <=0 is provided

    .. versionchanged:: 1.3.4 seed added to the random generator"""

    def __init__(self, n, k, bias=None, seed=0):
        if bias is None:
            super(ICDFArndIncomplete, self).__init__(n, k, True, 1, seed)
        elif bias <= 0 or bias >= 1:
            raise common.IllegalBias()
        else:
            m = int((bias * n) / (1 - bias))
            super(ICDFArndIncomplete, self).__init__(n, k, True, m, seed)
        self.n, self.k, self.bias = n, k, bias


    def __str__(self):
        return "ICDFArndIncomplete %d %d %d %d" % (self.n, self.k, self.bias, self.seed)