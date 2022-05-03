"""
This program creates all day-2 dead-ending games,
reduces them modulo E using known reductions,
and determines which are invertible and which are P-free.
Algebraic functions (neg, add, o, etc) 
and tests (is_greater, is_invertible, is_Pfree)
are imported from deadend_functions.py
"""

import itertools
import random
from deadend_functions import *

"""
First we define the four games born by day 1
and the day 2 ends.
Games are represented as lists of lists, G = [GL,GR]
"""

zero = [[],[]]
one = [[zero],[]]
star = [[zero],[zero]]
negone = [[],[zero]]

day1 = [zero, one, negone, star]

two = [ [one], [] ]          #the canonical game "two"
d1x4 = [ [one,zero], [] ]    #the 1x4 domineering board

day2ends = [two, neg(two), d1x4, neg(d1x4)]

"""
Next we create the non-end dead-ending day2 games
by using all possible non-empty subsets of day 1 games as option sets.
We use the powerset function from itertools.
"""

subsets=[]
def powerset(S,n):
    """Given a list S and length n,
    returns a list of all non-empty subsets of S up to size n""" 
    if n > 0:
        for x in itertools.combinations( S, n ):
            subsets.append(list(x))
        powerset( S, n-1 )
    return(subsets)

option_sets= list(powerset(day1,4))

day2nonends= []
for GL in option_sets:
    for GR in option_sets:
        G = [ GL, GR]
        day2nonends.append(G)

day2 = day2ends + day2nonends

def reduce(G):
    """Given a day2 dead-end game G, this function
    applies the reversibility reductions for E
    and returns the reduced form of G"""
    GL = list(G[0])
    GR = list(G[1])
    if star in G[0] and all(Gr in [one,star] for Gr in G[1]):
        if negone in G[0]:
            GL.remove(star)
        elif zero in G[0]:
            GL.remove(star)
            GL.append(negone)
    if star in G[1] and all(Gl in [negone,star] for Gl in G[0]):
        if one in G[1]:
            GR.remove(star)
        elif zero in G[1]:
            GR.remove(star)
            if negone in G[1]:
                GR.remove(negone)
                GR=GR+[one,negone]
            else:
                GR.append(one)
    return [GL,GR]


"""Create a list of the unique reduced day2 positions"""

day2reduced = []
for G in day2:
    H = reduce(G)
    if H not in day2reduced:
        day2reduced.append(H)

day2reduced.remove(star)    #star is not a day-2 game
day2reduced.remove([[negone],[one]])    #this game is zero, not a day-2 game

"""Create a list of the invertible reduced day2 positions"""

invertible=[]
for G in day2reduced:
    if is_invertible(G):
        #print_game(G)
        invertible.append(reduce(G))

print(f"There are {len(day2reduced)} unique reduced day-2 games in E")
print(f"There are {len(invertible)} invertible reduced day-2 positions in E")


"""Confirm that all reduced invertible day-2 games are P-free:"""

pfree_invert = True
for G in day2reduced:
    if not (is_invertible(G) == is_Pfree(G)):
        p_free_invert = False

print(f"Day 2 games are invertible iff P-free? {pfree_invert}")


"""Test the conjecture that larger games are invertible if & only if P-free:"""

day3options = day1 + day2reduced

def make_day3():
    """Makes a dead-ending game born by day 3
    with 1 or 2 random Left options and 1 or 2 random Right options"""
    num_left_options = random.choice([1,2])  #number of left options
    GL = random.sample(day3options,num_left_options)
    num_right_options = random.choice([1,2])  #number of left options
    GR = random.sample(day3options,num_right_options)
    G = [GL,GR]
    return G

def test_conjecture(k):
    """Creates k ~random day3 dead-ending games
    and for each checks the conjecture that p-free iff invertible.
    Returns True if no counterexample is found"""
    conjecture = True
    for i in range(k):
        G = make_day3()
        if not (is_Pfree(G)==is_invertible(G)):
            print("Counterexample!")
            print_game(G)
            conjecture = False
    return conjecture

print(f"Tested day 3 dead-ending games are invertible iff pfree? {test_conjecture(10)}")
