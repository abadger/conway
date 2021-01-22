Just Conway's Game of Life
==========================


| This is Conway's Game of Life.
| It's just a toy.
| But writing code is fun.
| And therefore I did.
|

`Conway's Game of Life <https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life>`_ seems to be a common
programming exercise.  I had to program it in Pascal when in High School and in C in an intro
college programming course.  I remember in college, since I had already programmed it before, that
I wanted to optimize the algorithm.  However, a combination of writing in C and having only a week
to work on it, I didn't have much time to implement anything fancy.

A couple years later, I hiked the Appalachian Trail.  Seven months away from computers, just hiking
day in and day out.  One of the things I found myself contemplating when walking up and down hills
all day was that pesky Game of Life algorithm and ways that I could improve it.

Fast forward through twenty intervening years of life and experience with a few other programming
languages to last weekend.  I needed a fun programming exercise to raise my spirits so I looked up
the rules to Conway's Game of Life, sat down with vim and python, and implemented a version with all
of the thoughts I'd had about it over the years.


Branches
--------

I've implemented Conway's Game of Life in several different ways and stored each one on a separate
branch for comparison.


Naive: Tracking the whole board
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| /usr/bin/time -p output: real 124.55
| cloc output:             116 code lines
|

The ``naive`` branch is an approximation of how I would have first coded Conway's Game of Life way
back in that intro to computer science course.  The grid of cells is what I would have called a two
dimensional array in my C days.  In Python, I've more often heard it called a list of lists.  Each
entry in the outer list is a row on the grid which are each represented by another list.  Each entry
in the inner lists are cells in that row of the grid.  If a cell is populated, then the list entry
contains ``True``.  If not, then the list entry contains ``False``.

Checking for changes is done by looping through every cell on the Board, and checking whether the
neighbor's of the cell meant that the cell would be populated or unpopulated on the next iteration.


Intermediate: Better checking
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| /usr/bin/time -p output: real 20.46
| cloc output:             121 code lines
|

The ``intermediate`` branch rectifies an inefficiency with checking of the next generation in the
naive branch.  Instead of checking every single cell, it only checks cells around currently
populated cells.  This is because empty cells which are not touching any populated cells will always
be empty in the next iteration.  Since most boards will have significantly more empty cells than
populated cells, this should mean that we can skip checking of most cells this way.


Gridless: Only tracking populated cells
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| /usr/bin/time -p output: real 6.06
| cloc output:             114 code lines
|

This is an idea that I thought of when Conway's was an assignment in an intro college course but
didn't have the time to implement in C over the course of one lab.  Working in Python, with it's
built in data types, it was actually very quick to implement.

The idea of ``gridless`` hinges on the same principle as the ``intermediate`` branch.  Most cells
are empty so it's a waste to operate on them.  Whereas ``intermediate`` just stops checking them,
though, ``gridless`` decides to back the board of cells with a different data structure, a set.
Within the set, we only store the cells which are populated.  Any cell not listed in the set is
known to be empty.  This reduces the memory usage in addition to reducing the number of cells we
have to check.


Main: Only checking cell changes once per iteration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| /usr/bin/time -p output: real real 4.28
| cloc output:             120 code lines
|

The ``main`` branch is a small optimization of ``gridless``. In ``gridless``, we performed checks
by running through the populated cells and checking both them and the cells which neighbored them.
In ``main``, we add the tweak of not checking a neighboring cell more than once.  That way if an
empty cell is bordered by multiple other cells, we do not process it multiple times.
