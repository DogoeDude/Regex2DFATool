# -*- coding: utf-8 -*-
"""Finite languages and related automata manipulation

Finite languages manipulation

.. *Authors:* Rogério Reis, Nelma Moreira & Guilherme Duarte

.. *This is part of FAdo project*   https://fado.dcc.fc.up.pt

.. *Copyright*: 1999-2022 Rogério Reis & Nelma Moreira {rvr,nam}@dcc.fc.up.pt

.. This program is free software; you can redistribute it and/or modify
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

#  Copyright (c) 2023-2024. Rogério Reis <rogerio.reis@fc.up.pt> and Nelma Moreira <nelma.moreira@fc.up.pt>.
#
#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
#
#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

from . import fa
import copy
from . common import *
import random
from bitarray import bitarray, frozenbitarray
from bitarray.util import ba2int
from itertools import product
from z3 import *


class FL(object):
    """Finite Language Class

    :var Words: the elements of the language
    :var Sigma: the alphabet"""
    def __init__(self, wordsList=None, Sigma=None):
        self.Words = set([])
        if Sigma is None:
            self.Sigma = set([])
        else:
            self.Sigma = Sigma
        if wordsList is not None:
            for w in wordsList:
                if type(w) is Word:
                    self.addWord(w)
                else:
                    self.addWord(Word(w))

    def __str__(self):
        l = "({"
        for i in self.Words:
            l += str(i) + ","
        l = l[:-1] + "}, {"
        for i in self.Sigma:
            l += str(i)+","
        l = l[:-1] + "})"
        return l

    def __repr__(self):
        return "FL%blksz" % self.__str__()

    def __len__(self):
        return len(self.Words)

    def __contains__(self, item):
        return item in self.Words

    def union(self, other):
        """union of FL:   a | b

        Args:
            other (FL): right hand operand
        Returns:
            FL: result of the union
        Raises:
            FAdoGeneralError: if both arguments are not FL"""
        return self.__or__(other)

    def __or__(self, other):
        if type(other) != type(self):
            raise FAdoGeneralError("Incompatible objects")
        new = FL()
        new.Sigma = self.Sigma | other.Sigma
        new.Words = self.Words | other.Words
        return new

    def intersection(self, other):
        """Intersection of FL: a & b

        Args:
            other (FL): left hand operand
        Returns:
            FL: result of the operation
        Raises:
            FAdoGeneralError: if both arguments are not FL"""
        return self.__and__(other)

    def __iter__(self):
        return iter(self.Words)

    def __and__(self, other):
        if type(other) != type(self):
            raise FAdoGeneralError("Incompatible objects")
        new = FL()
        new.Sigma = self.Sigma | other.Sigma
        new.Words = self.Words & other.Words
        return new

    def diff(self, other):
        """Difference of FL: a - b

        Args:
            other (FL): left hand operand
        Returns:
            FL: result of the operation
        Raises:
            FAdoGeneralError: if both arguments are not FL"""
        return self.__sub__(other)

    def __sub__(self, other):
        if type(other) != type(self):
            raise FAdoGeneralError("Incompatible objects")
        new = FL()
        new.Sigma = self.Sigma | other.Sigma
        new.Words = self.Words - other.Words
        return new

    def setSigma(self, Sigma, Strict=False):
        """Sets the alphabet of a FL

        Args:
            Sigma (string): alphabet
            Strict (bool): behaviour

        .. attention::
           Unless Strict flag is set to True, alphabet can only be enlarged.  The resulting alphabet is  in fact the
           union of the former alphabet with the new one. If flag is set to True, the alphabet is simply replaced."""
        if Strict:
            self.Sigma = Sigma
        else:
            self.Sigma = self.Sigma.union(Sigma)

    def addWords(self, wList):
        """Adds a list of words to a FL

        Args:
            wList (list): words to be added"""
        self.Words |= set(wList)
        for w in wList:
            if w.epsilonP():
                continue
            for c in w:
                self.Sigma.add(c)

    def addWord(self, word):
        """Adds a word to a FL

        Args:
            word (string): word to be added
        Returns:
            FL: """
        if word in self:
            return
        self.Words.add(word)
        if not word.epsilonP():
            for c in word:
                self.Sigma.add(c)

    def suffixClosedP(self):
        """Tests if a language is suffix closed

        Returns:
            bool: True if language is suffix closed"""
        wrds = list(copy.copy(self.Words))
        if Epsilon not in wrds:
            return False
        else:
            wrds.remove(Epsilon)
        wrds.sort(lambda x, y: len(x) - len(y))
        while wrds:
            w = wrds.pop()
            for w1 in suffixes(w):
                if w1 not in self.Words:
                    return False
                else:
                    if w1 in wrds:
                        wrds.remove(w1)
        return True

    def filter(self, automata):
        """Separates a language in two other using a DFA of NFA as a filter

        Args:
            automata (dict): the automata to be used as a filter
        Returns:
            tuple of FL: the accepted/unaccepted pair of languages"""
        a, b = (FL(), FL())
        a.setSigma(self.Sigma)
        b.setSigma(self.Sigma)
        for w in self.Words:
            if automata.evalWord(w):
                a.addWords([w])
            else:
                b.addWords([w])
        return a, b

    def MADFA(self):
        """Generates the minimal acyclical DFA using specialized algorithm

        .. versionadded:: 1.3.3

        .. seealso:: Incremental Construction of Minimal Acyclic Finite-State Automata, J.Daciuk, blksz.Mihov, B.Watson and r.E.Watson

        :rtype: ADFA"""
        if self.Words == FL([Epsilon]).Words:
            aut = ADFA()
            i = aut.addState()
            aut.setInitial(i)
            aut.addFinal(i)
            aut.setSigma(self.Sigma)
            return aut
        aut = ADFA()
        i = aut.addState()
        aut.setInitial(i)
        aut.setSigma(self.Sigma)
        register = set()
        foo = sorted(list(self.Words))
        for w in foo:  # sorted(list(self.Words)):
            (cPrefix, lState) = aut._common_prefix(w)
            cSuffix = w[len(cPrefix):]
            if aut.delta.get(lState, {}):
                aut._replace_or_register(lState, register)
            aut.addSuffix(lState, cSuffix)
        aut._replace_or_register(i, register)
        aut.Minimal = True
        return aut

    def trieFA(self):
        """Generates the trie automaton that recognises this language

        Returns:
            ADFA: the trie automaton"""
        new = ADFA()
        new.setSigma(copy.copy(self.Sigma))
        i = new.addState()
        new.setInitial(i)
        for w in self.Words:
            if w.epsilonP():
                new.addFinal(i)
            else:
                s = i
                for c in w:
                    if c not in new.delta.get(s, []):
                        sn = new.addState()
                        new.addTransition(s, c, sn)
                        s = sn
                    else:
                        s = new.delta[s][c]
                new.addFinal(s)
        return new

    def toDFA(self):
        """ Generates a DFA recognizing the language

        Returns:
            ADFA: the DFA

        .. versionadded:: 1.2"""
        return self.trieFA()

    def toNFA(self):
        """Generates a NFA recognizing the language

        Returns:
            ANFA:

        .. versionadded:: 1.2"""
        return self.toDFA().toANFA()

    # noinspection PyUnboundLocalVariable
    def multiLineAutomaton(self):
        """Generates the trivial linear ANFA equivalent to this language

        Returns:
            ANFA: the trivial linear ANFA"""
        new = ANFA()
        s1 = None
        new.setSigma(copy.copy(self.Sigma))
        for w in self.Words:
            s = new.addState()
            new.addInitial(s)
            for c in w:
                s1 = new.addState()
                new.addTransition(s, c, s1)
                s = s1
            new.addFinal(s1)
        return new


class DFCA(fa.DFA):
    """Deterministic Cover Automata class

    .. inheritance-diagram:: DFCA"""

    def __init__(self):
        super(DFCA, self).__init__()
        self.length = None

    @property
    def length(self):
        """ The length of the longest word
        Returns:
            int: the length of the longest word"""
        return self.length

    @length.setter
    def length(self, value):
        """Setter
        :param int value: size"""
        self.length = value

    @length.deleter
    def length(self):
        """Length deleter"""
        self.length = None


class AFA(object):
    """Base class for Acyclic Finite Automata

    .. inheritance-diagram:: AFA

    **note:** This is just a container for some common methods. **Not to be used directly!!**"""
    def __init__(self):
        self.Dead = None
        self.delta = dict()
        self.Initial = None
        self.States = []
        self.Final = set()

    @abstractmethod
    def addState(self, _):
        """
        Returns:
            int: """
        pass

    @abstractmethod
    def finalP(self, _):
        pass

    def setDeadState(self, sti):
        """Identifies the dead state

        Args:
            sti (string): index of the dead state

        .. attention::
           nothing is done to ensure that the state given is legitimate

        .. note::
           without dead state identified, most of the methods for acyclic automata can not be applied"""
        self.Dead = sti

    def ensureDead(self):
        """Ensures that a state is defined as dead"""
        try:
            _ = self.Dead
        except AttributeError:
            x = self.addState(DeadName)
            self.setDeadState(x)

    def ordered(self):
        """Orders states names in its topological order

        Returns:
            list of int: ordered list of state indexes

        .. note::
           one could use the FA.toposort() method, but special care must be taken with the dead state for the
           algorithms related with cover automata."""

        def _dealS(st1):
            if st1 not in torder:
                torder.append(st1)
                if st1 in list(self.delta.keys()):
                    for k in self.delta[st1]:
                        for dest in forceIterable(self.delta[st1][k]):
                            if dest not in torder and dest != self.Dead:
                                queue.append(dest)

        try:
            dead = self.Dead
        except AttributeError:
            raise FAdoGeneralError("ADFA has not dead state identified")
        torder, queue = [], []
        _dealS(self.Initial)
        while queue:
            st = queue.pop()
            _dealS(st)
        torder.append(dead)
        return torder

    def _getRdelta(self):
        """
        Returns:
            dict: pair, map of number of sons map, of reverse conectivity"""
        done = set()
        deltaC, rdelta = {}, {}
        notDone = set(forceIterable(self.Initial))
        while notDone:
            sts = uSet(notDone)
            done.add(sts)
            l = set()
            for k in self.delta.get(sts, []):
                for std in forceIterable(self.delta[sts][k]):
                    l.add(std)
                    rdelta.setdefault(std, set([])).add(sts)
                    if std not in done:
                        notDone.add(std)
            deltaC[sts] = len(l)
            notDone.remove(sts)
        for s in forceIterable(self.Initial):
            if s not in rdelta:
                rdelta[s] = set()
        return deltaC, rdelta

    def directRank(self):
        """Compute rank function

        Returns:
            dict: rank map"""
        r, _ = self.evalRank()
        n = {}
        for x in r:
            for i in r[x]:
                n[i] = x
        return n

    def evalRank(self):
        """Evaluates the rank map of a automaton

        Returns:
            tuple: pair of sets of states by rank map, reverse delta accessability map"""
        (deltaC, rdelta) = self._getRdelta()
        rank, deltai = {}, {}
        for s in range(len(self.States)):
            deltai.setdefault(deltaC[s], set([])).add(s)
        i = -1
        notDone = list(range(len(self.States)))
        deltaC[self.Dead] = 0
        deltai[1].remove(self.Dead)
        deltai[0] = {self.Dead}
        rdelta[self.Dead].remove(self.Dead)
        while notDone:
            rank[i] = deepcopy(deltai[0])
            deltai[0] = set()
            for s in rank[i]:
                for s1 in rdelta[s]:
                    l = deltaC[s1]
                    deltaC[s1] = l - 1
                    deltai[l].remove(s1)
                    deltai.setdefault(l - 1, set()).add(s1)
                notDone.remove(s)
            i += 1
        return rank, rdelta

    def getLeaves(self):
        """The set of leaves, i.e. final states for last symbols of language words

        Returns:
            set: A set of leaves"""
        # noinspection PyUnresolvedReferences
        def _last(s1):
            queue, done = {s1}, set()
            while queue:
                q = queue.pop()
                done.add(q)
                for k in self.delta.get(q, {}):
                    for s1 in forceIterable(self.delta[q][k]):
                        if self.finalP(s1):
                            return False
                        elif s1 not in done:
                            queue.add(s1)
            return True

        leaves = set()
        for s in self.Final:
            if _last(s):
                leaves.add(self.States[s])
        return leaves


class ADFA(fa.DFA, AFA):
    """Acyclic Deterministic Finite Automata class

    .. inheritance-diagram:: ADFA

    .. versionchanged:: 1.3.3
    """
    def __init__(self):
        fa.DFA.__init__(self)
        AFA.__init__(self)
        self.Minimal = False

    def __repr__(self):
        return 'ADFA({0:blksz})'.format(self.__str__())

    def complete(self, dead=None):
        """Make the ADFA complete

        Args:
            dead (int, optional): a state to be identified as dead state if one was not identified yet

        .. attention::
           The object is modified in place

        .. versionchanged:: 1.3.3"""
        if dead is not None:
            self.Dead = dead
        else:
            try:
                if self.Dead is None:
                    raise AttributeError
                else:
                    _ = self.Dead
            except AttributeError:
                foo = self.addState(DeadName)
                self.Dead = foo
        for st in range(len(self.States)):
            for k in self.Sigma:
                if k not in list(self.delta.get(st, {}).keys()):
                    self.addTransition(st, k, self.Dead)
        self.Minimal = False
        return self

    def dup(self):
        """Duplicate the basic structure into a new ADFA. Basically a copy.deep.

        Returns:
            ADFA: """
        return copy.deepcopy(self)

    def __invert__(self):
        """ Complement of a ADFA is a DFA

        Returns:
            DFA: """
        aut = self.forceToDFA()
        return ~aut

    def minimalP(self, method=None):
        """Tests if the DFA is minimal

        Args:
            method (str): minimization algorithm (here void)
        Returns:
            bool:

        .. versionchanged:: 1.3.3"""
        if self.Minimal:
            return True
        foo = self.minimal()
        if self.completeP():
            foo.complete()
        answ = len(foo) == len(self)
        if answ:
            self.Minimal = True
        return answ

    def forceToDFA(self):
        """ Conversion to DFA

        Returns:
            DFA: """
        new = fa.DFA()
        new.States = copy.deepcopy(self.States)
        new.Sigma = copy.deepcopy(self.Sigma)
        new.Initial = self.Initial
        new.Final = copy.copy(self.Final)
        for s in self.delta:
            for c in self.delta[s]:
                new.addTransition(s, c, self.delta[s][c])
        return new

    def forceToDFCA(self):
        """ Conversion to DFCA

        Returns:
            DFA: """
        return self.forceToDFA()

    def wordGenerator(self):
        """Creates a random word generator

        Returns:
            RndWGen: the random word generator

        .. versionadded:: 1.2"""
        return RndWGen(self)

    def possibleToReverse(self):
        """Tests if language is reversible

        .. versionadded:: 1.3.3"""
        return True

    def minimal(self):
        """Finds the minimal equivalent ADFA

        Returns:
            DFA: the minimal equivalent ADFA

        .. seealso:: [TCS 92 pp 181-189] Minimisation of acyclic deterministic automata in linear time, Dominique Revuz

        .. versionchanged:: 1.3.3 """

        def _getListDelta(ss):
            """returns [([sons,final?],blksz) for blksz in ss].sort"""
            l = []
            for s in ss:
                dl = [new.delta[s][k] for k in new.Sigma]
                dl.append(s in new.Final)
                l.append((dl, s))
            l.sort()
            return l

        def _collapse(r1, r2):
            """redirects all transitions going to r2 to r1 and adds r2 to toBeDeleted"""
            for s in rdelta[r2]:
                for k in new.delta[s]:
                    if new.delta[s][k] == r2:
                        new.delta[s][k] = r1
            toBeDeleted.append(r2)

        if len(self.States) == 1:
            return self
        new = copy.deepcopy(self)
        new.trim()
        new.complete()
        if new.Dead is None:
            deadName = None
        else:
            deadName = new.States[new.Dead]
        rank, rdelta = new.evalRank()
        toBeDeleted = []
        maxr = len(rank) - 2
        for r in range(maxr + 1):
            ls = _getListDelta(rank[r])
            (d0, s0) = ls[0]
            j = 1
            while j < len(ls):
                (d1, s1) = ls[j]
                if d0 == d1:
                    _collapse(s0, s1)
                else:
                    (d0, s0) = (d1, s1)
                j += 1
        new.deleteStates(toBeDeleted)
        if deadName is not None:
            new.Dead = new.stateIndex(deadName)
        new.Minimal = True
        return new

    def minReversible(self):
        """Returns the minimal reversible equivalent automaton

        Returns:
            ADFA: """
        new = self.dup()
        new.evalRank()

    def statePairEquiv(self, s1, s2):
        """Tests if two states of a ADFA are equivalent

        Args:
            s1 (int): state1
            s2 (int): state2
        Returns:
            bool:

        .. versionadded:: 1.3.3"""
        if not self.same_nullability(s1, s2):
            return False
        else:
            return self.delta.get(s1, {}) == self.delta.get(s2, {})

    def addSuffix(self, st, w):
        """Adds a suffix starting in st

        :param int st: state
        :param Word w: suffix

        .. versionadded:: 1.3.3

        .. attention:: in place transformation"""
        s1 = st
        for c in w:
            s2 = self.addState()
            self.addTransition(s1, c, s2)
            s1 = s2
        self.addFinal(s1)

    def _last_child(self, s):
        """to be used by xxx of FL.MADFA

        Args:
            s (int): state index
        Returns:
            tuple: pair state index / symbol

        .. versionadded:: 1.3.3"""
        for c in sorted(list(self.Sigma)).__reversed__():
            if c in self.delta.get(s, {}):
                return self.delta[s][c], c
        raise FAdoGeneralError("Something unexpected in _last_child({:d})".format(s))

    def _replace_or_register(self, s, r):
        """to be used by xxx of FL.MADFA

        Args:
            s (int): state index
            r (set): register (inherited from context)

        .. versionadded:: 1.3.3"""
        (child, c) = self._last_child(s)
        if self.delta.get(child, {}):
            self._replace_or_register(child, r)
        for q in r:
            if self.statePairEquiv(q, child):
                self.delta[s][c] = q
                self.deleteState(child)
                return
        r.add(child)

    def _common_prefix(self, wrd):
        """The longest prefix of w that can be read in the ADFA and the correspondent state

        Args:
            wrd (Word): the word """
        pref = Word()
        q = self.Initial
        for s in wrd:
            if s in self.delta.get(q, {}):
                pref.append(s)
                q = self.delta[q][s]
            else:
                break
        return pref, q

    def _addWordToMinimal(self, w):
        """Incremental minimization algorithm

        Args:
            w (Word): the word

        .. attention:: in place transformation

        .. versionadded:: 1.3.3

        .. seealso:: Incremental Construction of Minimal Acyclic Finite-State Automata, J.Daciuk, blksz.Mihov,
                     B.Watson and r.E.Watson"""

        def _transverseNonConfluence(wrd):
            inCount = dict()
            for s in range(len(self.States)):
                for c in self.delta.get(s, {}):
                    for s1 in self.delta[s][c]:
                        inCount[s1] = inCount.get(s1, 0) + 1
            q1 = self.Initial
            visited1 = [q1]
            for ii, sym in enumerate(wrd):
                if sym not in self.delta.get(q1, {}) or inCount[self.delta[q1][sym]] > 1:
                    # here there was a reference to blksz self.delta.get(blksz, {}) that must be wrong!
                    return q1, ii
                q1 = self.delta[q1][sym]
                visited1.append(q1)

        def _cloneConfluence(st, wrd, ind):
            q1 = st
            for ii, sym in enumerate(wrd[ind:]):
                if sym not in self.delta.get(q1, {}):
                    return q1, ii + ind
                qn = self.delta[q1][sym]
                sn = self.addState()
                for c1 in self.delta.get(qn, {}):
                    self.delta.setdefault(sn, {})[c1] = self.delta[qn][c1]
                    if self.finalP(qn):
                        self.addFinal(sn)
                self.addTransition(q1, sym, sn)
                q1 = sn
                visited.append(q1)

        def _replOrReg(st, wrd):
            if len(w) != 0:
                self.addTransition(q, wrd[0], _replOrReg(self.delta[st][wrd[0]], wrd[1:]))
            else:
                for c in register:
                    if self.statePairEquiv(c, q):
                        self.deleteState(q)
                        return c
                register.add(q)

        def _addSuffix(st, wrd):
            s = st
            for c in wrd:
                sn = self.addState()
                self.addTransition(s, c, sn)
                s = sn
            self.addFinal(s)

        register = set()
        visited = []
        q, i = _transverseNonConfluence(w)
        f = q
        register.remove(q)
        j = i
        q, i = _cloneConfluence(q, w, i)
        _addSuffix(q, w[i:])
        if j < len(w):
            self.delta[f][w[j]] = _replOrReg(self.delta[f][w[j]], w[j+1:])

    def dissMin(self, witnesses=None):
        """Evaluates the minimal dissimilarity language

        Args:
            witnesses (dict): optional witness dictionay
        Returns:
            FL:

        .. versionadded:: 1.2.1"""
        new = self.minimal()
        sz = len(new.States)
        todo = [(i, j) for i in range(sz) for j in range(i)]
        mD = FL(Sigma=new.Sigma)
        lvl = new.level()
        rnk = new.directRank()
        l = max([rnk[x] for x in rnk])
        Li = []
        for (i, j) in todo:
            if self.finalP(i) ^ self.finalP(j):
                if witnesses is not None:
                    witnesses[(i, j)] = Word(Epsilon)
                Li.append((i, j))
                mD.addWord(Word(Epsilon))
        delFromList(todo, Li)
        words = self.words()
        for w in words:
            if len(w) >= l or not todo:
                break
            Li = []
            for (i, j) in todo:
                if (lvl[i] + len(w) > l) or (lvl[j] + len(w) > l):
                    Li.append((i, j))
                elif self.evalWordP(w, i) ^ self.evalWordP(w, j):
                    mD.addWord(w)
                    if witnesses is not None:
                        witnesses[(i, j)] = w
                    Li.append((i, j))
            delFromList(todo, Li)
        return mD

    def diss(self):
        """ Evaluates the dissimilarity language

        Returns:
            FL:

        .. versionadded:: 1.2.1"""
        new = self.minimal()
        n = len(new.States)
        mD = FL(Sigma=new.Sigma)
        lvl = new.level()
        rnk = new.directRank()
        l = max([rnk[x] for x in rnk])
        if len(new.Final) != n:
            mD.addWord(Word(Epsilon))
        words = self.words()
        for w in words:
            lw = len(w)
            if lw >= l:
                break
            skip = False
            for i in range(n):
                if skip:
                    break
                for j in range(i):
                    if (lvl[i] + lw <= l) and (lvl[j] + lw <= l) and (self.evalWordP(w, i) ^ self.evalWordP(w, j)):
                        mD.addWord(w)
                        skip = True
                        break
        return mD

    def level(self):
        """Computes the level  for each state

        Returns:
            dict: levels of states

        .. versionadded:: 0.9.8"""
        lvl = {}
        done, alvl = set(), [self.Initial]
        l = 0
        while alvl:
            nlvl = set()
            for i in alvl:
                lvl[i] = l
                done.add(i)
                for c in self.delta[i]:
                    j = self.delta[i][c]
                    if j not in done and j not in alvl:
                        nlvl.add(j)
            l += 1
            alvl = copy.copy(nlvl)
        return lvl

    def _gap(self, l, lvl):
        """Computes the gap value for each pair of states.

        The automata is supposed to have its states named numerically in such way that the initial is zero

        Args:
            l (int): length of the longest word
            lvl (dict): level of each state
        Returns:
            dict: gap function """
        def _range(r, s):
            return l - max(lvl[r], lvl[s])
        gp = {}
        n = len(self.States) - 1
        for i in range(n):
            gp[(self.stateIndex(i), self.stateIndex(n))] = l
        if lvl[self.stateIndex(n)] <= l:
            for i in self.Final:
                gp[(i, self.stateIndex(n))] = 0
        for i in range(n):
            for j in range(i + 1, n):
                if not self.same_nullability(self.stateIndex(i), self.stateIndex(j)):
                    gp[(self.stateIndex(i), self.stateIndex(j))] = 0
                else:
                    gp[(self.stateIndex(i), self.stateIndex(j))] = l
        for i in range(n - 2, -1, -1):
            for j in range(n, i, -1):
                for c in self.Sigma:
                    i1, j1 = self.delta[self.stateIndex(i)][c], self.delta[self.stateIndex(j)][c]
                    if i1 != j1:
                        if int(self.States[i1]) < int(self.States[j1]):
                            g = gp[(i1, j1)]
                        else:
                            g = gp[(j1, i1)]
                        if g + 1 <= _range(self.stateIndex(i), self.stateIndex(j)):
                            gp[(self.stateIndex(i), self.stateIndex(j))] = min(gp[(self.stateIndex(i),
                                                                                   self.stateIndex(j))], g + 1)
        return gp

    def minDFCA(self):
        """Generates a minimal deterministic cover automata from a DFA

        Returns:
            DCFA:

        .. versionadded:: 0.9.8

        .. seealso::
            Cezar Campeanu, Andrei Päun, and Sheng Yu, An efficient algorithm for constructing minimal cover
            automata for finite languages, IJFCS"""
        new = self.dup().minimal()
        if not self.completeP():
            new.complete()
        rank = new.directRank()
        irank = dict((v, [k for (k, xx) in [key_value for key_value in list(rank.items()) if key_value[1] == v]])
                     for v in set(rank.values()))
        l = rank[new.Initial]
        lvl = new.level()
        foo = [x for x in irank]
        foo.sort(reverse=True)
        lnames = [None for _ in new.States]
        newname = 0
        for i in foo:
            for j in irank[i]:
                lnames[j] = newname
                newname += 1
        new.States = lnames
        g = new._gap(l, lvl)
        P = [False for _ in new.States]
        toMerge = []
        for i in range(len(new.States) - 1):
            if not P[i]:
                for j in range(i + 1, len(new.States)):
                    if not P[j] and g[(new.stateIndex(i), new.stateIndex(j))] == l:
                        toMerge.append((i, j))
                        P[j] = True
        for (a, b) in toMerge:
            new.mergeStates(new.stateIndex(b), new.stateIndex(a))
        new.trim()
        new = new.forceToDFCA()
        new.length = l
        return new

    def trim(self):
        """Remove states that do not lead to a final state, or, inclusively, that can't be reached from the initial
        state. Only useful states remain.

        .. attention:: in place transformation"""
        fa.OFA.trim(self)
        try:
            del self.Dead
        except AttributeError:
            pass
        return self

    def toANFA(self):
        """Converts the ADFA in a equivalent ANFA

        Returns:
            ANFA:"""
        new = ANFA()
        new.setSigma(copy.copy(self.Sigma))
        new.States = copy.copy(self.States)
        for s in range(len(self.States)):
            for k in self.delta.get(s, {}):
                new.addTransition(s, k, self.delta[s][k])
        new.addInitial(self.Initial)
        for s in self.Final:
            new.addFinal(s)
        return new

    def toNFA(self):
        """Converts the ADFA in a equivalent NFA

        Returns:
            ANFA:

        .. versionadded:: 1.2"""
        return self.toANFA()


class RndWGen(object):
    """Word random generator class

    .. versionadded:: 1.2"""
    def __init__(self, aut):
        """
        :param aut: automata recognizing the language
        :type aut: ADFA """
        self.Sigma = list(aut.Sigma)
        self.table = dict()
        self.aut = aut.minimal()
        rank, _ = self.aut.evalRank()
        self.aut._compute_delta_inv()
        deltai = self.aut.delta_inv
        mrank = max(rank)
        for i in range(0, mrank + 1):
            for s in rank[i]:
                self.table.setdefault(s, {})
                if self.aut.finalP(s):
                    final = 1
                else:
                    final = 0
                self.table[s][None] = sum([self.table[s].get(c, 0) for c in self.Sigma])
                for c in self.Sigma:
                    rs = deltai[s].get(c, [])
                    for r in rs:
                        self.table.setdefault(r, {})
                        self.table[r][c] = self.table[s][None] + final

    @staticmethod
    def _rndChoose(l):
        sm = sum(l)
        r = random.randint(1, sm)
        for i, j in enumerate(l):
            if r <= j:
                return i
            else:
                r -= j

    def __next__(self):
        """Next word

        :return: a new random word"""
        word = Word()
        s = self.aut.Initial
        while True:
            if self.aut.finalP(s) and random.randint(1, self.table[s][None] + 1) == 1:
                return word
            i = self._rndChoose([self.table[s].get(c, 0) for c in self.Sigma])
            word.append(self.Sigma[i])
            s = self.aut.delta[s][self.Sigma[i]]


# noinspection PyUnresolvedReferences
class ANFA(fa.NFA, AFA):
    """Acyclic Nondeterministic Finite Automata class

    .. inheritance-diagram:: ANFA"""

    def moveFinal(self, st, stf):
        """Unsets a set as final transfering transition to another final
        :param int st: the state to be 'moved'
        :param int stf: the destination final state

        .. note::
           stf must be a 'last' final state, i.e., must have no out transitions to anywhere but to a possible dead
           state

        .. attention:: the object is modified in place"""
        (rdelta, _) = self._getRdelta()
        for s in rdelta[st]:
            l = []
            for k in self.delta[s]:
                if st in self.delta[s][k]:
                    l.append(k)
            for k in l:
                self.addTransition(s, k, stf)
            self.delFinal(s)

    def mergeStates(self, s1, s2):
        """Merge state s2 into state s1

        Args:
            s1 (int): state index
            s2 (int): state index

        .. note::
           no attempt is made to check if the merging preserves the language of teh automaton

        .. attention:: the object is modified in place"""
        (_, rdelta) = self._getRdelta()
        for s in rdelta[s2]:
            l = []
            for k in self.delta[s]:
                if s2 in self.delta[s][k]:
                    l.append(k)
            for k in l:
                self.delta[s][k].remove(s2)
                self.addTransition(s, k, s1)
        for k in self.delta.get(s2, {}):
            for ss in self.delta[s2][k]:
                self.delta.setdefault(s1, {}).setdefault(k, set()).add(ss)
        self.deleteState(s2)

    def mergeLeaves(self):
        """Merge leaves

        .. attention:: object is modified in place"""
        l = self.getLeaves()
        if len(l):
            s0n = l.pop()
            while l:
                s0 = self.stateIndex(s0n)
                s = self.stateIndex(l.pop())
                self.mergeStates(s0, s)

    def mergeInitial(self):
        """Merge initial states

        .. attention:: object is modified in place"""
        l = copy.copy(self.Initial)
        s0 = self.stateIndex(l.pop())
        while l:
            s = self.stateIndex(l.pop())
            self.mergeStates(s0, s)


def sigmaInitialSegment(Sigma: list, l: int, exact=False) -> ADFA:
    """Generates the ADFA recognizing Sigma^i for i<=l

    Args:
        Sigma (list): the alphabet
        l (int): length
        exact (bool): only the words with exactly that length?
    Returns:
        ADFA: the automaton
    """
    new = ADFA()
    new.setSigma(Sigma)
    s = new.addState()
    if not exact:
        new.addFinal(s)
    new.setInitial(s)
    for i in range(l):
        s1 = new.addState()
        if not exact or i == l - 1:
            new.addFinal(s1)
        for k in Sigma:
            new.addTransition(s, k, s1)
        s = s1
    return new


# noinspection PyUnboundLocalVariable
def genRndTrieBalanced(maxL, Sigma, safe=True):
    """Generates a random trie automaton for a binary language of balanced words of a given leght for max word

    Args:
        maxL (int): the length of the max word
        Sigma (set): the alphabet to be used
        safe (bool): should a word of size maxl be present in every language?
    Returns:
        ADFA: the generated trie automaton """

    def _genEnsurance(m, alphabet):
        l = len(alphabet)
        fair = m / l
        if m % l == 0:
            odd = 0
        else:
            odd = 1
        pool = copy.copy(alphabet)
        c = {}
        sl = []
        while len(sl) < m:
            s1 = random.choice(pool)
            c[s1] = c.get(s1, 0) + 1
            if c[s1] == fair + odd:
                pool.remove(s1)
            sl.append(s1)
        return sl

    def _legal(cont):
        l = [cont[k1] for k1 in cont]
        return max(l) - min(l) <= 1

    def _descend(s1, ens, safe1, m, cont):
        sons = 0
        if not safe1:
            if _legal(cont):
                final = random.randint(0, 1)
            else:
                final = 0
        # noinspection PyUnboundLocalVariable
        if safe1:
            trie.addFinal(s1)
            final = 1
        elif final == 1:
            trie.addFinal(s1)
        if m != 0:
            if safe1:
                ks = ens.pop()
            else:
                ks = None
            for k1 in trie.Sigma:
                ss = trie.addState()
                trie.addTransition(s1, k1, ss)
                cont[k1] = cont.get(k1, 0) + 1
                if _descend(ss, ens, k1 == ks, m - 1, cont):
                    sons += 1
                cont[k1] -= 1
        if sons == 0 and final == 0:
            trie.deleteState(s1)
            return False
        else:
            return True

    if safe:
        ensurance = _genEnsurance(maxL, Sigma)
    else:
        ensurance = None
    trie = ADFA()
    trie.setSigma(Sigma)
    s = trie.addState()
    trie.setInitial(s)
    contab = {}
    for k in Sigma:
        contab[k] = 0
    _descend(s, ensurance, safe, maxL, contab)
    if random.randint(0, 1) == 1:
        trie.delFinal(s)
    return trie


# noinspection PyUnboundLocalVariable
def genRndTrieUnbalanced(maxL, Sigma, ratio, safe=True):
    """Generates a random trie automaton for a binary language of balanced words of a given length for max word

    Args:
        maxL (int): length of the max word
        Sigma (set): alphabet to be used
        ratio (int): the ratio of the unbalance
        safe (bool): should a word of size maxl be present in every language?
    Returns:
        ADFA: the generated trie automaton """

    def _genEnsurance(m, alphabet):
        chief = uSet(alphabet)
        fair = m / (ratio + 1)
        pool = list(copy.copy(alphabet))
        c = {}
        sl = []
        while len(sl) < m:
            s1 = random.choice(pool)
            c[s1] = c.get(s1, 0) + 1
            if len(sl) - c.get(chief, 0) == fair:
                pool = [chief]
            sl.append(s1)
        return sl

    def _legal(cont):
        l = [cont[k1] for k1 in cont]
        return (ratio + 1) * cont[uSet(Sigma)] >= sum(l)

    # noinspection PyUnboundLocalVariable
    def _descend(s1, ens, safe1, m, cont):
        sons = 0
        if not safe1:
            if _legal(cont):
                final = random.randint(0, 1)
            else:
                final = 0
        if safe1:
            trie.addFinal(s1)
            final = 1
        elif final == 1:
            trie.addFinal(s1)
        if m:
            if safe1:
                ks = ens.pop()
            else:
                ks = None
            for k1 in trie.Sigma:
                ss = trie.addState()
                trie.addTransition(s1, k1, ss)
                cont[k1] = cont.get(k1, 0) + 1
                if _descend(ss, ens, k1 == ks, m - 1, cont):
                    sons += 1
                cont[k1] -= 1
        if sons == 0 and final == 0:
            trie.deleteState(s1)
            return False
        else:
            return True
    if safe:
        ensurance = _genEnsurance(maxL, Sigma)
    else:
        ensurance = None
    trie = ADFA()
    trie.setSigma(Sigma)
    s = trie.addState()
    trie.setInitial(s)
    contab = {}
    for k in Sigma:
        contab[k] = 0
    _descend(s, ensurance, safe, maxL, contab)
    if random.randint(0, 1) == 1:
        trie.delFinal(s)
    return trie


# noinspection PyUnboundLocalVariable
def genRandomTrie(maxL, Sigma, safe=True):
    """Generates a random trie automaton for a finite language with a given length for max word

    Args:
        maxL (int): length of the max word
        Sigma (set): alphabet to be used
        safe (bool): should a word of size maxl be present in every language?
    Returns:
        ADFA: the generated trie automaton """

    def _genEnsurance(m, alphabet):
        l = len(alphabet)
        sl = list(alphabet)
        return [sl[random.randint(0, l - 1)] for _ in range(m)]

    # noinspection PyUnboundLocalVariable
    def _descend(s1, ens, safe1, m):
        sons = 0
        final = None
        if not safe1:
            final = random.randint(0, 1)
        if safe1:
            trie.addFinal(s1)
            final = 1
        elif final == 1:
            trie.addFinal(s1)
        if m:
            if safe1:
                ks = ens.pop()
            else:
                ks = None
            for k in trie.Sigma:
                ss = trie.addState()
                trie.addTransition(s1, k, ss)
                if _descend(ss, ens, k == ks, m - 1):
                    sons += 1
        if sons == 0 and final == 0:
            trie.deleteState(s1)
            return False
        else:
            return True

    if safe:
        ensurance = _genEnsurance(maxL, Sigma)
    else:
        ensurance = None
    trie = ADFA()
    trie.setSigma(Sigma)
    s = trie.addState()
    trie.setInitial(s)
    _descend(s, ensurance, safe, maxL)
    if random.randint(0, 1) == 1:
        trie.delFinal(s)
    return trie


# noinspection PyUnboundLocalVariable
def genRndTriePrefix(maxL, Sigma, ClosedP=False, safe=True):
    """Generates a random trie automaton for a finite (either prefix free or prefix closed) language with a given
    length for max word

    Args:
        maxL (int): length of the max word
        Sigma (set): alphabet to be used
        ClosedP (bool): should it be a prefix closed language?
        safe (bool): should a word of size maxl be present in every language?
    Returns:
        ADFA: the generated trie automaton """

    def _genEnsurance(m, alphabet):
        l = len(alphabet)
        sl = list(alphabet)
        return [sl[random.randint(0, l - 1)] for _ in range(m)]

    def _descend(s1, ens, saf, m):
        sons = ClosedP
        if m == 0:
            final = random.randint(0, 1)
            if saf or final == 1:
                trie.addFinal(s1)
                return True
            else:
                return False
        else:
            if saf is True:
                ks = ens.pop()
            else:
                ks = None
            for k in trie.Sigma:
                ss = trie.addState()
                trie.addTransition(s1, k, ss)
                r = _descend(ss, ens, k == ks, m - 1)
                if not ClosedP:
                    sons |= r
                else:
                    sons &= 1
            if not ClosedP:
                if not sons:
                    final = random.randint(0, 1)
                    if final == 1:
                        trie.addFinal(s1)
                        return True
                    else:
                        return False
                else:
                    return True
            else:
                if not sons:
                    final = random.randint(0, 1)
                    if final == 1:
                        trie.addFinal(s1)
                        return True
                    else:
                        return False
                else:
                    trie.addFinal(s1)
                    return True

    ensurance = None
    if safe:
        ensurance = _genEnsurance(maxL, Sigma)
    trie = ADFA()
    trie.setSigma(Sigma)
    s = trie.addState()
    trie.setInitial(s)
    _descend(s, ensurance, safe, maxL)
    return trie


def DFAtoADFA(aut):
    """Transforms an acyclic DFA into a ADFA

    Args:
        aut (DFA): the automaton to be transformed
    Returns:
        ADFA: the converted automaton
    Raises:
        notAcyclic: if the DFA is not acyclic """
    new = copy.deepcopy(aut)
    new.trim()
    if not new.acyclicP(True):
        raise notAcyclic()
    afa = ADFA()
    afa.States = copy.copy(new.States)
    afa.Sigma = copy.copy(new.Sigma)
    afa.Initial = new.Initial
    afa.delta = copy.copy(new.delta)
    afa.Final = copy.copy(new.Final)
    afa.complete()
    return afa


def stringToADFA(s):
    """Convert a canonical string representation of a ADFA to a ADFA

    Args:
        s (str): the string in its canonical order
    Returns:
        ADFA: the ADFA

    .. seealso::
        Marco Almeida, Nelma Moreira, and Rogério Reis. Exact generation of minimal acyclic deterministic finite
        automata. International Journal of Foundations of Computer Science, 19(4):751-765, August 2008. """
    k = len(s[0]) - 1
    new = ADFA()
    new.setSigma([str(c) for c in range(k)])
    for st, sts in enumerate(s):
        new.addState(str(st))
        for c, s1 in enumerate(sts[:-1]):
            new.addTransition(st, str(c), s1)
        if sts[-1]:
            new.addFinal(st)
    new.setInitial(len(s) - 1)
    return new


# Block

def dfa_block(m, sigma=["a", "b"]):
    return sigmaInitialSegment(sigma, m, True)


def dfa_maxlen(m, sigma=["a", "b"]):
    return sigmaInitialSegment(sigma, m)

def coBlockDFA(a: fa.DFA, n: int) -> fa.DFA:
    """
    Args:
        a (DFA): automaton accepting fixed length words
        n (int): length of words accepted, n > 0
    Returns:
        DFA: accepts the words of length n not accepted by a

    .. versionadded:: 2.1.2 """

    def _addStates(a, n, k):
        # Invoked using k blksz.t. k-1 = 1st level of a state with a missing transition
        # then new states added at levels k,...,n and new transitions from each
        # new state to the new one of the next level using all symbols as labels
        if k > n:
            return
        newst = {}
        for i in range(k, n+1):
            newst[i] = a.addState()
        a.Final = set([newst[n]])
        for i in range(k, n):
            for sym in a.Sigma:
                a.addTransition(newst[i], sym, newst[i+1])
        return newst

    al = a.Sigma
    coa = a.dup()
    coa.trim()
    coa.Final = set([])
    lev = 0
    sss = set([a.Initial])
    missing_states_added = False
    while lev < n and sss:
        ssq = set()
        for s in sss:
            for sym in al:
                q = coa.Delta(s, sym)
                if q is None:
                    if not missing_states_added:
                        newst = _addStates(coa, n, lev+1)
                        missing_states_added = True
                    coa.addTransition(s, sym, newst[lev+1])
                else:
                    ssq.add(q)
        lev += 1
        sss = ssq
    return coa.trim()


def blockUniversalP(a, n):
    """
    Args:
         a (NFA): blksz NFA (= NFA accepting only words of same length)
         n (int): length of accepted words
    Returns:
        bool: whether a is blksz universal (accepts all words of length n)

    .. versionadded: 2.1.2"""
    return coBlockDFA(a.toDFA(), n).emptyP()


class BitString(object):
    """ Class to represent the bitstring of a block language

    :var blocksize: the size of the block
    :var alphsize: the size of the alphabet
    :var bst: the bitstring representation of the language

    .. versionadded: 2.1.3
    """
    def __init__(self,blksz, alphsize, bst=None):
        self.blocksize = blksz
        self.alphsize = alphsize
        if bst is not None:
            self.bst = bitarray(bst)
        else:
            self.bst = bitarray(alphsize**blksz)


    def strb(self):
        return "".join([str(self.bst[i]) for i in range(len(self.bst))])

    def minDFA(self):
        def _nonnullname(n):
            for i in n:
                if i != "0":
                    return True
            return False

        def _partName(n, k, c):
            p = len(n) // k
            return n[p*c:p*(c+1)]

        lastDone = False
        whole = self.strb()
        aut = fa.DFA()
        todo, done = set(), set()
        idx = idx = aut.addState(whole)
        aut.setInitial(idx)
        todo.add(idx)
        while todo:
            idx = todo.pop()
            done.add(idx)
            for c in range(self.alphsize):
                n = _partName(aut.States[idx], self.alphsize, c)
                if _nonnullname(n):
                    id1 = aut.stateIndex(n, True)
                    if len(n) == 1:
                        if not lastDone:
                            aut.setFinal([id1])
                            lastDone = True
                    elif id1 not in done:
                        todo.add(id1)
                    aut.addTransition(idx, str(c), id1)
        return aut

        si = aut.addState(self.strb())
        aut.setInitial(si)

    def minNFA(self):
        aut = ANFA()
        sti1 = aut.addState('final')
        aut.addFinal(sti1)
        m = {frozenbitarray('1'): sti1}
        d= {frozenbitarray('1'): {frozenbitarray('1')}}
        PreviousStatesID = {frozenbitarray('0'), frozenbitarray('1')}
        for ri in range(1, self.blocksize + 1):
            idsize = self.alphsize ** ri
            states_id = [self.bst[k * idsize: (k + 1) * idsize] for k in range(self.alphsize ** self.blocksize // idsize)]
            states_id = {y for y in [frozenbitarray(x) for x in states_id] if y.any()}
            left = 0
            right = len(states_id)
            coverSize = -1
            coverModel = None
            while left <= right:
                mid = (left + right) // 2
                r = _coverOfSizeN(states_id, PreviousStatesID, mid, self.alphsize, idsize)
                if r:
                    coverSize = mid
                    coverModel = r
                    right = mid - 1
                else:
                    left = mid + 1
            if coverSize == -1:
                raise NFAerror(
                    f'no cover found for StatesID: {states_id}, PreviousStatesID: {PreviousStatesID}')
            cover = coverModel[0]
            statesCover = coverModel[1]
            for StateID in cover:
                if ri < self.blocksize:
                    sti1 = aut.addState()
                else:
                    sti1 = aut.addState('start')
                    aut.setInitial({sti1})
                m[StateID] = sti1
                ImageIDsize = idsize // self.alphsize
                ImagesStateID = [StateID[k * ImageIDsize: (k + 1) * ImageIDsize] for k in range(self.alphsize)]
                for sigma, ImageStateID in zip(range(self.alphsize), ImagesStateID):
                    if all(not b for b in ImageStateID):
                        continue
                    for CoverImageStateID in d[ImageStateID]:
                        foo_ = m[CoverImageStateID]
                        aut.addTransition(sti1, sigma, foo_)
            for StateID, CoverStateID in zip(states_id, statesCover):
                d[StateID] = CoverStateID
            PreviousStatesID = states_id
        return aut

    def _notNull(self, v):
        for i in v:
            if v != 0:
                return True
        return Fa
    def reverse(self):
        """ Compute the BitString representation of the reverse of the current language.

        .. versionadded: 2.1.3"""
        s = self.bst
        r = _allShuffle(self.alphsize, self.blocksize, s)
        return BitString(self.blocksize, self.alphsize, r)

    def _reverseGD(self):
        """ Compute the BitString representation of the reverse of the current language.

        .. versionadded: 2.1.3

        .. note::
           This version computes the reverse directly but is approximately 10 times slower than the other version"""
        l = self.alphsize**self.blocksize
        n = [0 for _i in range(l)]
        for i in range(l):
            ib = pad(self.blocksize, inBase(i, self.alphsize))
            ib.reverse()
            n[fromBase(ib, self.alphsize)] = self.bst[i]
        return BitString(self.blocksize, self.alphsize, n)


def _coverOfSizeN(vs, pv, n, k, l):
    bvv = [BitVecVal(ba2int(v), l) for v in vs]
    pv_ = [ba.to01() for ba in (pv.union({frozenbitarray(l // k)}))]
    s = [''.join(id) for id in product(pv_, repeat=k)]
    bvs = [BitVecVal(int(x, 2), l) for x in s]
    f = BitVecVal(0, l)
    Ssize = len(s)
    subset = [Bool(f'x{i}') for i in range(Ssize)]
    subsetv = []
    for v in vs:
        subsetv.append([Bool(f'x{v},{i}') for i in range(Ssize)])
    solver = Solver()
    solver.add(Sum(subset) == n)  # subset of size n
    for i, v in enumerate(bvv):
        ored = f
        for j in range(Ssize):
            solver.add(Implies(subsetv[i][j], subset[j]))  # if subseti[i][j] then subset[j]
            ored = ored | If(subsetv[i][j], bvs[j], f)  # there must be a sub-subset that Or'ed together equals v
        solver.add(ored == v)
    if solver.check() == sat:
        model = solver.model()
        result_subset = [frozenbitarray(s[i]) for i in range(Ssize) if is_true(model[subset[i]])]
        result_subsetv = []
        for i, _ in enumerate(vs):
            result_subsetv.append([frozenbitarray(s[j]) for j in range(Ssize) if is_true(model[subsetv[i][j]])])
        return result_subset, result_subsetv
    else:
        return None

def genRndBitString(b: int, k: int) -> BitString:
    """Generates a random bitstring with alphabet size k and block size b

    Args:
        b (int): The size of the block
        k (int): The size of the alphabet
    Returns:
        bitarray: the random bitstring

    .. versionadded: 2.1.4"""
    new = BitString(b, k)
    for i in range(k**b):
        new.bst[i]=random.randint(0,1)
    return new


def _pShuffle(k: int, s: int, l: bitarray) -> bitarray:
    """ Performs a perfect shuffle on a list assumming k to be the size of the alphabet and blksz the lenght of the slices
        being shuffled

    Args:
        k (int): the size of the alphabet
        blksz (int): the size of the slices
        l (bitarray): the list to be shuffled
    Returns:
        bitarray: the shuffled list

    .. versionadded: 2.1.3"""
    l1, l3 = len(l)//k, 0
    l2 = [i*l1 for i in range(k)]
    new = bitarray()
    while l3 < l1:
        for i in l2:
            _x,_y = i+l3, i+l3+s
            new.extend(l[i+l3:i+l3+s])
        l3 += s
    return new


def _allShuffle(k: int, blksz: int, l: bitarray) -> bitarray:
    """ Perform the complete reversal of a bitstring l of a language where k is the size of the alphabet, blksz is
        the size of the block

    Args:
        k (int): the size of the alphabet
        blksz (int): the size of the block
        l (bitarray): the bitstring of the language
    Returns:
        bitarray: the bitstring of the reversed language

    .. versionadded: 2.1.3"""
    blksz = blksz-1
    assert len(l) % (k**(blksz-1)) == 0
    n = l.copy()
    for i in range(0, blksz):
        n = _pShuffle(k, k ** i, n)
    return n

def firstBlockWords(alpzs: int, nwords: int, blksz: int) -> ADFA:
    """ Generates the minimal ADFA that accepts exactly the first nwords (lexicographic order) of a blksz language

    Args:
        alpzs (int): alphabet size
        nwords (int): number of words
        blksz (int): blksz size
    Returns:
        ADFA: the ADFA that recognises exacly those words

    .. versionadded: 2.1.3"""
    assert 0 < nwords < alpzs**blksz+1
    rl = padList(inBase(nwords-1, alpzs),blksz)
    for i in range(blksz):
        if rl[blksz-1-i] != alpzs-1:
            break
    triv, opt = i, i
    if triv == 0:
        triv = 1
    aut = ADFA()
    aut.setSigma(list(range(alpzs)))
    ini = aut.addState()
    aut.setInitial(ini)
    main, border = ini, ini
    div, order = False, 0
    for i in rl[:-triv]:
        ns = aut.addState()
        if main == border:
            if i == 0:
                aut.addTransition(main,0,ns)
                main, border = ns, ns
            else:
                if opt != 0 and order + triv + 1 == blksz:
                    for j in range(i + 1):
                        aut.addTransition(main, j, ns)
                    main, border = ns, ns
                else:
                    for j in range(i):
                        aut.addTransition(main, j, ns)
                    div = True
                    nb =  aut.addState()
                    aut.addTransition(border, i, nb)
                    main, border = ns, nb
        else: # already diverged
            for j in range(alpzs):
                aut.addTransition(main, j, ns)
            for j in range(i):
                aut.addTransition(border, j, ns)
            if opt != 0 and order + triv + 1 == blksz:
                aut.addTransition(border, i, ns)
                main, border = ns, ns
            else:
                nb = aut.addState()
                aut.addTransition(border, i, nb)
                main, border = ns, nb
        order += 1
    # now deal with the last symbols and its obtimisation
    while triv != 0:
        ns = aut.addState()
        if div:
            for j in range(alpzs):
                aut.addTransition(main, j, ns)
            if border != main:
                for j in range(rl[-triv]+1):
                    aut.addTransition(border, j, ns)
        else:
            for j in range(rl[-triv]+1):
                aut.addTransition(main, j, ns)
        main, border = ns, ns
        triv -= 1
    aut.setFinal([ns])
    return aut


def generateBlockTrie(sz: int, alpsz: int) -> ADFA:
    """Generates a trie for a blksz language

    Args:
        sz (int): size of the blksz
        alpsz (int): size of the alphabet
    Returns:
        ADFA: the automaton

    .. versionadded:: 2.1.3 """
    aut = ADFA()
    aut.setSigma(list(range(alpsz)))
    sti = aut.addState()
    aut.setInitial(sti)
    l = [sti]
    for i in range(sz):
        ln = []
        for st in l:
            for c in range(alpsz):
                sti = aut.addState()
                ln.append(sti)
                aut.addTransition(st, c, sti)
        l = ln
    aut.setFinal(l)
    return aut

class BlockWords(object):
    """Block language iterator"""
    def __init__(self, k:int, b:int):
        self.k = k
        self.b = b
        self.first = True

    def __iter__(self):
        return self

    def __next__(self):
        if self.first:
            self.s = [0] * self.b
            self.first = False
            return self.s
        y = self._sequent(self.s)
        if y is None:
            raise StopIteration
        self.s = y
        return self.s

    def _sequent(self, s):
        for i in range(self.b):
            if s[self.b-1-i] != self.k-1:
                return s[:self.b-i-1]+[s[self.b-i-1]+1]+[0]*i
        return None
