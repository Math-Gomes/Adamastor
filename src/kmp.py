from collections import namedtuple
import sympy as sym
import numpy as np # A matriz ajudará nas equações
import string # Possui o alfabeto para ser usado como entrada

KMP = namedtuple('KMP', 'fsm pat_size alph_size pat')

def kmp(pat, alphabet=None):
    alphabet = list(alphabet or set(pat))
    # if not alphabet:
    #     alphabet = list(set(pat))
    # else:
    #     alphabet = list(alphabet)
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


def equations(kmp_t):
    fsm, m, n, _ = kmp_t
    z = sym.symbols('z')
    mat = np.array(list(fsm.values()))

    #Cria as variáveis simbólicas para cada estado do autômato
    symbs = [sym.symbols('S_'+str(i)) for i in range(m+1)]
##    for i in range(m+1):
##        sym_name = sym.symbols('S_'+str(i))
##        symbs.append(sym_name)

    eqr = [0]*m
    eqr[0] = 1
    for j,k in enumerate(mat.T):
        counts = np.bincount(k, minlength=m+1)
        for i in range(m):
            eqr[i] += counts[i]*z*symbs[j]

    eqs = []
    for i,s in enumerate(symbs[:-1]):
        eq = sym.Eq(s, eqr[i])
        eqs.append(eq)

    eq = sym.Eq(symbs[-1], z*symbs[-2])
    eqs.append(eq)

    return eqs, z

def equations_(kmp_t, prob_dict):
    fsm, m, n,_ = kmp_t
    z = sym.symbols('z')
    mat = np.array(list(fsm.values()))
    fsm_keys = list(fsm.keys())

    #Cria as variáveis simbólicas para cada estado do autômato
    symbs = [sym.symbols('S_'+str(i)) for i in range(m+1)]
##    for i in range(m+1):
##        sym_name = sym.symbols('S_'+str(i))
##        symbs.append(sym_name)

    eqr = [0]*m
    eqr[0] = 1
    # for j,k in enumerate(mat.T):
    #     counts = np.bincount(k, minlength=m+1)
    #     for i in range(m):
    #         eqr[i] += counts[i]*z*symbs[j]
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

def mean(eqs, z, alph_size=2):
    aux,_ = eqs[-1].args
    g = sym.solve(eqs, exclude=[z])
    g = g[aux]

    g = g.subs(z, z/alph_size)
    g_ = sym.diff(g, z)

    return g_.subs(z, 1)

def mean_(eqs, z):
    aux,_ = eqs[-1].args
    g = sym.solve(eqs, exclude=[z])
    g = g[aux]

    g_ = sym.diff(g, z)

    return g_.subs(z, 1)


# sym.init_printing()

# pat = 'tobeornottobe'
# ##alph = "".join([chr(i) for i in range(ord('a'), ord('z')+1)])
# alph = string.ascii_lowercase

# print(pat, alph)

# kmp_t = kmp(pat, alph)
# #print(fms)
# eqs, z = equations(kmp_t)
# for i in eqs:
#     s = sym.pretty(i)
#     print(s)


# # for i in eqs:
# #     j,k = i.args
# #     print(j, '=', k, ', ', end='')

# print('Média:',mean(eqs,z, kmp_t.alph_size))

if __name__ == "__main__":
    pat = 'kkkk'
    alph = 'ck'
    prob = {
        'c':.01,
        'k':.99,
    }
    kmp_t = kmp(pat, alph)
    eqs, z = equations_(kmp_t, prob)
    for i in eqs:
        s = sym.pretty(i)
        print(s)
    print('Média:', mean_(eqs,z))