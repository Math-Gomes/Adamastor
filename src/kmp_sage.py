# -*- coding: utf-8 -*-
'''
Esse módulo não deve ser usado diretamente.
'''


from __future__ import print_function
from collections import namedtuple
import sys # Argumentos da entrada
import pickle # Faz a leitura do objetos (USAR PROTOCOLO 2)
import numpy as np # A matriz ajudará nas equações
import string # Possui o alfabeto para ser usado como entrada
import sage.all


def equations_sage(kmp_t):
    fsm, m, n, pat, prob_dict = kmp_t
    z = sage.all.var('z')
    mat = np.array(fsm.values())
    fsm_keys = fsm.keys()

    #Cria as variáveis simbólicas para cada estado do autômato
    symbs = [sage.all.var('S_'+str(i)) for i in range(m+1)]

    eqr = [0]*m
    eqr[0] = 1
    for i,_ in enumerate(symbs[:-1]):
        pos = np.where(mat == i)
        for row,col in zip(*pos):
            eqr[i] += prob_dict[fsm_keys[row]]*z*symbs[col]

    eqs = []
    for i,s in enumerate(symbs[:-1]):
        eq = s == eqr[i]
        eqs.append(eq)
    eq = symbs[-1] == prob_dict[pat[-1]]*z*symbs[-2]
    eqs.append(eq)

    return eqs, symbs, z

def mean_sage(eqs, symbs, z):
    sol = sage.all.solve(eqs, symbs)
    eqf = sol[0][-1] # Equação do estado final
    eqf_rhs = eqf.rhs() # Descarta o lado esquerdo da equação
    g_ = eqf_rhs.diff()

    return g_.subs(z=1)

# pat = 'tobeornottobe'
# alph = string.ascii_lowercase

# print(pat, alph)

# kmp_t = kmp(pat, alph)

# eqs, symbs, z = equations_sage(kmp_t)

# print('Média:',mean_sage(eqs, symbs, z, kmp_t.alph_size))

if __name__=='__main__':
    kmp_file = sys.argv[1]
    with open(kmp_file, 'rb') as arq:
        kmp = pickle.load(arq)

    eqs, symbs, z = equations_sage(kmp)
    m = mean_sage(eqs, symbs, z)
    print(m)
    for i in eqs:
        print(i)

