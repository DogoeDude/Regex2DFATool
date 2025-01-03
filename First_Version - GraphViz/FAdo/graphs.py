# -*- coding: utf-8 -*-
"""**Graph support**

Basic Graph object support and manipulation

.. versionadded: 1.0

.. *Authors:* Rogério Reis & Nelma Moreira

.. *This is part of FAdo project*   http://fado.dcc.fc.up.pt.

.. *Copyright:* 2014 Rogério Reis & Nelma Moreira {rvr,nam}@dcc.fc.up.pt

.. This program is free software; you can redistribute it and/or
   modify it under the terms of the GNU General Public License as published
   by the Free Software Foundation; either version 2 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
   or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
   for more details.

   You should have received a copy of the GNU General Public License along
   with this program; if not, write to the Free Software Foundation, Inc.,
   675 Mass Ave, Cambridge, MA 02139, USA."""

import copy

from . common import *


class Graph(Drawable):
    """Graph base class

    :var list Vertices: Vertices' names
    :var set Edges: set of pairs (always sorted)

    .. inheritance-diagram:: Graph"""

    @abstractmethod
    def dotFormat(self, size):
        pass

    def __init__(self):
        self.Vertices = []
        self.Edges = set()

    def addVertex(self, vname):
        """Adds a vertex (by name)

        :param vname: vertex name
        :return: vertex index
        :rtype: int

        :raises DuplicateName: if vname already exists"""
        if vname in self.Vertices:
            raise DuplicateName
        self.Vertices.append(vname)
        return len(self.Vertices) - 1

    def vertexIndex(self, vname, autoCreate=False):
        """Return vertex index

        :param bool autoCreate: auto creation of non existing states
        :param vname: vertex name
        :rtype: int

        :raises GraphError: if vname not found"""
        if vname not in self.Vertices:
            if not autoCreate:
                raise GraphError
            else:
                return self.addVertex(vname)
        else:
            return self.Vertices.index(vname)

    def addEdge(self, v1, v2):
        """Adds an edge
        :param int v1: vertex 1 index
        :param int v2: vertex 2 index
        :raises GraphError: if edge is loop"""
        if v1 == v2:
            raise GraphError
        if v1 < v2:
            self.Edges.add((v1, v2))
        else:
            self.Edges.add((v2, v1))


class DiGraph(Graph):
    """Directed graph base class

    .. inheritance-diagram:: DiGraph"""
    def addEdge(self, v1, v2):
        """Adds an edge

        :param int v1: vertex 1 index
        :param int v2: vertex 2 index"""
        self.Edges.add((v1, v2))

    def inverse(self):
        """Inverse of a digraph"""
        new = DiGraph()
        new.Vertices = copy.deepcopy(self.Vertices)
        for (i, j) in self.Edges:
            new.addVertex(j)
        return new

    # noinspection PyUnresolvedReferences
    def dotFormat(self, size="20,20", direction="LR", sep="\n", strict=False, maxLblSz=MAXLBL):
        """ A dot representation

        :arg str direction: direction of drawing
        :arg str size: size of image
        :arg str sep: line separator
        :arg maxLblSz: max size of labels before getting removed
        :arg strict: use limitations of label sizes
        :return: the dot representation
        :rtype: str

        .. versionadded:: 0.9.6

        .. versionchanged:: 0.9.8"""
        s = "digraph finite_state_machine {{{0:s}".format(sep)
        s += "rankdir={0:s};{1:s}".format(direction, sep)
        s += "size=\"{0:s}\";{1:s}".format(size, sep)
        s += "node [shape = point]; dummy{0:s}".format(sep)
        niStates = [i for i in range(len(self.States)) if i != self.Initial]
        for sti in niStates:
            s += self.dotDrawVertex(sti)
        for s1, s2 in self.Edges:
            s += self.dotDrawEdge(s1, s2)
        s += "}}{0:s}".format(sep)
        return s

    @staticmethod
    def dotDrawEdge(st1, st2, sep="\n"):
        """ Draw a transition in Dot Format

        :arg str st1: starting state
        :arg str st2: ending state
        :arg str sep: separator
        :rtype: str"""
        return "\"{0:s}\" -> \"{1:s}\" {3:s} ".format(st1, st2, sep)

    def dotDrawVertex(self, sti, sep="\n"):
        """ Draw a Vertex in Dot Format

        :arg int sti: index of the state
        :arg str sep: separator
        :rtype: str """
        lbl = self.Vertices[sti].__str__()
        return "node [shape = circle]; \"{0:s}\";{1:s}".format(lbl, sep)


class DiGraphVm(DiGraph):
    """Directed graph with marked vertices

    :var set MarkedV: set of marked vertices

    .. inheritance-diagram:: DiGraphVm"""
    def __init__(self):
        super(DiGraphVm, self).__init__()
        self.MarkedV = set()

    def markVertex(self, v):
        """Mark vertex v

        :param int v: vertex"""
        self.MarkedV.add(v)
