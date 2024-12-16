=============
What is FAdo?
=============

The **FAdo** system aims to provide an open source extensible high-performance software library for the symbolic
manipulation of automata and other models of computation.

To allow high-level programming with complex data structures, easy prototyping of algorithms, and portability
(to use in computer grid systems for example), are its main features. Our main motivation is the theoretical
and experimental research, but we have also in mind the construction of a pedagogical tool for teaching automata
theory and formal languages.

-----------------
Regular Languages
-----------------

It currently includes most standard operations for the manipulation of regular languages. Regular languages can
be represented by regular expressions (RegExp) or finite automata, among other formalisms. Finite automata may
be deterministic (DFA), non-deterministic (NFA) or generalized (GFA). In **FAdo** these representations are implemented
as Python classes.



Elementary regular languages operations as union, intersection, concatenation, complementation and reverse are
implemented for each class. Also several other regular operations (e.g shuffle) and combined operations are available for specific models.



* Several conversions between these representations are implemented:

  * NFA -> DFA: subset construction

  * NFA -> RE: recursive method

  * GFA -> RE: state elimination, with possible choice of state orderings (several heuristics)

  * RE -> NFA: Thompson, Glushkov/Position, epsilon-Follow, Follow, Partial Derivatives (naive and compressed RE), Prefix; and their duals.

  * SRE -> DFA: Brzozowski (SRE are RegExp ACIA, using sets)

  * RE -> DFA: AuPoint (Marked before)  and YMG (Marked after)

* For DFAs several minimization algorithms are available: Moore, Hopcroft, and some incremental algorithms. Brzozowski minimization is available for NFAs.

* An algorithm for hyper-minimization of DFAs

* For DFAs tests for reversability   

* Language equivalence of two DFAs can be determined by reducing their correspondent minimal DFA to a canonical form, or by the Hopcroft and Karp algorithm.

* For NFAs reductions by left and right  bisimilarity

* Enumeration of the first words of a language or all words of a given length (Cross Section)

* Some support for the transition semigroups of DFAs

----------------
Finite Languages
----------------

Special methods for finite languages are available:

* Construction of a ADFA (acyclic finite automata) from a set of words

* Minimization of ADFAs

* Several methods for ADFAs random generation

* Methods for deterministic cover finite automata (DCFA)
  
* Special methods for Block languages where all words have the same length

-----------
Transducers
-----------

Several methods for transducers in standard form (SFT) are available:

* Rational operations: union, inverse, reversal, composition, concatenation, Star

* Test if a transducer is functional

* Input intersection and Output intersection operations

-----
Codes
-----

A *language property* is a set of languages. Given a property specified by a transducer, several language tests are possible.

* Satisfaction i.e. if a language satisfies the property

* Maximality i.e. the language satisfies the property and is maximal

* Properties implemented by transducers include: input preserving, input altering, trajectories, and fixed properties

* Computation of the edit distance of a regular language, using input altering transducers


----
PRAX
----

Polynomial Random Approximation Algorithms allow to decide hard automata problems considering cetrain natural distributions on set of words.

In particular, using the notion of approximate universality

* Test NFA universality for finite languagens

* Test NFA universality for infinite languages using tractable word distributions (Lambert and Dirichlet)  

  
  
