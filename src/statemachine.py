# https: // github.com/pytransitions/transitions
# graphviz pygraphviz transitions 
from transitions.extensions import GraphMachine
from kmp import kmp

class Model(object):
    pass

def get_machine_info(ksm,pat_size):
    states = []
    for i in range(pat_size+1):
        states.append('S_{}'.format(i))
    # print(states)

    transitions = []
    for letter,letter_data in ksm.items():
        for source,dest in enumerate(letter_data):
            transitions.append({'trigger': letter, 'source': 'S_{}'.format(source), 'dest': 'S_{}'.format(dest)})
    # print(transitions)

    return states,transitions

def plot_state_machine(states, transitions,filename):
    m = Model()
    machine = GraphMachine(model=m,
                        states=states,
                        transitions=transitions,
                        initial='S_0',
                        auto_transitions=False,
                        show_conditions=True)

    G = m.get_graph()
    G.graph_attr['label'] = 'Autômato'
    # ['neato', 'dot', 'twopi', 'circo', 'fdp', 'nop']
    G.draw(filename, prog='dot')

pat = 'aab'
alph = 'ab'
ksm, pat_size, _ = kmp(pat, alph)
states,transitions = get_machine_info(ksm,pat_size)
plot_state_machine(states, transitions, 'sm.png')
