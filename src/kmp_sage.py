# -*- coding: utf-8 -*-

from __future__ import print_function
from collections import namedtuple
import numpy as np # A matriz ajudará nas equações
import string # Possui o alfabeto para ser usado como entrada
import sage.all

KMP = namedtuple('KMP', 'fsm pat_size alph_size')

def kmp(pat, alphabet=None):
    if not alphabet:
        alphabet = list(set(pat))
    else:
        alphabet = list(alphabet)
    m = len(pat)

    """
    fsm é um dicionario que descreve a máquina de estados. Se o estado atual
    é j e o próximo caracter é i, o próximo estado será fsm[i][j].
    """
    fsm = {c:[0]*m for c in alphabet}
    fsm[pat[0]][0] = 1 #Adiciona a primeira transição

    x = 0
    for j in range(1, m): #Para cada estado (exceto o primeiro)
        for c in alphabet:
            fsm[c][j] = fsm[c][x]
        fsm[pat[j]][j] = j+1
        x = fsm[pat[j]][x]

    return KMP(fsm, m, len(alphabet))


def search(txt, pat):
    alphabet = list(set(txt))
    fsm, end_state, _ = kmp(pat, alphabet=alphabet)

    state = 0
    for i,c in enumerate(txt):
        state = fsm[c][state]
        if state == end_state:
            return i - len(pat) + 1

    return -1

def equations_sage(kmp_t):
    fsm, m, n = kmp_t
    z = sage.all.var('z')
    mat = np.array(list(fsm.values()))

    #Cria as variáveis simbólicas para cada estado do autômato
    symbs = [sage.all.var('S_'+str(i)) for i in range(m+1)]

    eqr = [0]*m
    eqr[0] = 1
    for j,k in enumerate(mat.T):
        counts = np.bincount(k, minlength=m+1)
        for i in range(m):
            eqr[i] += counts[i]*z*symbs[j]

    eqs = []
    for i,s in enumerate(symbs[:-1]):
        eq = s == eqr[i]
        eqs.append(eq)
    eq = symbs[-1] == z*symbs[-2]
    eqs.append(eq)

    return eqs, symbs, z

def mean_sage(eqs, symbs, z, alph_size=2):
    sol = sage.all.solve(eqs, symbs)
    eqf = sol[0][-1] # Equação do estado final
    eqf_rhs = eqf.rhs() # Descarta o lado esquerdo da equação

    g = eqf_rhs.subs(z=z/alph_size)
    g_ = g.diff()

    return g_.subs(z=1)

# pat = 'tobeornottobe'
# alph = string.ascii_lowercase

# print(pat, alph)

# kmp_t = kmp(pat, alph)

# eqs, symbs, z = equations_sage(kmp_t)

# print('Média:',mean_sage(eqs, symbs, z, kmp_t.alph_size))
