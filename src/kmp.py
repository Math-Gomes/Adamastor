from collections import namedtuple
import sympy as sym
import numpy as np # A matriz ajudará nas equações
import string # Possui o alfabeto para ser usado como entrada
import math

KMP = namedtuple('KMP', 'fsm pat_size alph_size pat')

def kmp(pat, alphabet=None):
    alphabet = list(alphabet or set(pat))
    m = len(pat)

    fsm = {c:[0]*m for c in alphabet}
    fsm[pat[0]][0] = 1 #Adiciona a primeira transição

    x = 0
    for j in range(1, m): #Para cada estado (exceto o primeiro)
        for c in alphabet:
            fsm[c][j] = fsm[c][x]
        fsm[pat[j]][j] = j+1
        x = fsm[pat[j]][x]

    return KMP(fsm, m, len(alphabet), pat)


def search(txt, pat):
    alphabet = list(set(txt))
    fsm, end_state, _ = kmp(pat, alphabet=alphabet)

    state = 0
    for i,c in enumerate(txt):
        state = fsm[c][state]
        if state == end_state:
            return i - len(pat) + 1

    return -1

def equations_(kmp_t, prob_dict):
    fsm, m, n,_ = kmp_t
    z = sym.symbols('z')
    mat = np.array(list(fsm.values()))
    fsm_keys = list(fsm.keys())

    #Cria as variáveis simbólicas para cada estado do autômato
    symbs = [sym.symbols('S_'+str(i)) for i in range(m+1)]

    eqr = [0]*m
    eqr[0] = 1
    for i,_ in enumerate(symbs[:-1]):
        pos = np.where(mat == i)
        for row,col in zip(*pos):
            eqr[i] += prob_dict[fsm_keys[row]]*z*symbs[col]

    eqs = []
    for i,s in enumerate(symbs[:-1]):
        eq = sym.Eq(s, eqr[i])
        eqs.append(eq)
    ll = kmp_t.pat[-1]
    eq = sym.Eq(symbs[-1],  prob_dict[ll]*z*symbs[-2])
    eqs.append(eq)

    return eqs, z

def mean_(eqs, z):
    aux,_ = eqs[-1].args
    g = sym.solve(eqs, exclude=[z])
    g_solve = g
    g = g[aux]

    g_ = sym.diff(g, z)

    return g_.simplify().subs(z, 1), g_solve