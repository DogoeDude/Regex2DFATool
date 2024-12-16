#  Copyright (c) 2023-2024. Rogério Reis <rogerio.reis@fc.up.pt> and Nelma Moreira <nelma.moreira@fc.up.pt>.
#
#  This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.
#
# ordered DFA
#
#  This program is free software: you can redistribute it and/or modify it under the terms of the
#  GNU General Public License as published by the Free Software Foundation, either version 3 of the License,
#  or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
#  without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along with this program.
#  If not, see <https://www.gnu.org/licenses/>.

from z3 import *
from types import SimpleNamespace
from . common import *
from . fa import DFA


def _vard(t: int)-> str:
    v = 'x' + str(t)
    return v


def ordered_DFA(fa: DFA, Debug=False) -> tuple:
    if not fa.completeP(): # definition implies that the DFA needs to be complete
        raise DFAnotComplete
    LNS = SimpleNamespace()
    GNS = SimpleNamespace()
    exec("from z3 import *", globals(), locals())
    exec("S = Solver()", globals(), locals())
    vmax = len(fa)
    s = ""
    for c in range(vmax):
        s += _vard(c) + ", "
    s = s[:-1]
    s = s[:-1]
    # Variables' declatation
    s += " = Ints(\'"
    for c in range(vmax):
        s += _vard(c) + " "
    s = s[:-1]
    s += "\')"
    if Debug: print(s)
    else: exec(s, globals(), locals())
    s = "S.add(Distinct("
    for c in range(vmax):
        s += _vard(c) + ", "
    s = s[:-2] + "))"
    if Debug: print(s)
    else: exec(s, globals(), locals())
    if Debug: print(fa.States)
    s = "S.add(And("
    for q in range(len(fa.States)-1):
        for k in fa.Sigma:
            qs = fa.delta[q][k]
            for q1 in range(q+1,len(fa.States)):
                qs1 = fa.delta[q1][k]
                s += "Implies(" + _vard(q) + ">=" + _vard(q1) + ", " + _vard(qs) + ">=" + _vard(qs1) + "), "
                s += "Implies(" + _vard(q1) + ">=" + _vard(q) + ", " + _vard(qs1) + ">=" + _vard(qs) + "), "
    s = s[:-2] + "))"
    if Debug: print(s)
    else: exec(s, globals(), locals())
    if not Debug:
        result = eval("S.check()", globals(), locals())
        if result == sat:
            model = eval("S.model()", globals(), locals())
            dd = model.decls()
            lmodel = [ (fa.States[int(x.name()[1:])], model[x]) for x in dd]
            #
            # print(model)
            # print(model.decls())
            # lmodel = [model[i] for i in model]
            return lmodel
        else:
            return ()

