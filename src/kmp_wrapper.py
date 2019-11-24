'''
 Módulo para fazer a comunicação com sage
'''

import pickle
import subprocess

def solve(fsm, pat, alph, prob_dict):
    '''
        Executa o script sage baseado em python 2

        fsm é o dicionário da maquina de estados
        pat é o padrão
        alph é o alfabeto
        prob_dict é o dicionário de probabilidades

        # RETORNO
        media: autoexplicativo
        eqs: lista de strigs das equações
    '''
    kmp = (fsm, len(pat), len(alph), pat, prob_dict)

    #TODO escrever em um arquivo temporário
    kmp_fname = 'kmp_dump.pyc'
    with open(kmp_fname, 'wb') as arq:
        pickle.dump(kmp, arq, protocol=2) # mantém compatibilidade com python2

    out = subprocess.run(['sage', '--python', 'kmp_sage.py', kmp_fname],
        stdout=subprocess.PIPE)
    uout = str(out.stdout, encoding='utf8')
    uout = uout.split('\n')
    m = float(uout[0])
    eqs = [i for i in uout[1:] if i != '']
    return m, eqs
