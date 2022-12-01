import random
from typing import List


def get_chain(_terminals: str, _variables: str, _initial: str, _productions: List[str], current_chain: str = '',
              started: bool = False):
    non_terminals_in_the_chain = [non_terminal for non_terminal in current_chain if non_terminal in _variables]
    if len(non_terminals_in_the_chain) == 0:
        return current_chain
    if started and current_chain == '':
        return current_chain
    started = True
    if not started:
        possible_starts = [start for start in _productions if start[0] == _initial]


def fast_mode(_terminals: str, _variables: str, _initial: str, _productions: List[str]):
    pass


def detailed_mode(_terminals: str, _variables: str, _initial: str, _productions: List[str]):
    process_to_generate_the_chain = []
    possible_starts = [start for start in _productions if start[0] == _initial]

    options = ''
    for i in range(len(possible_starts)):
        options += f'{i} - {possible_starts[i]}\n'
    options += f'{len(possible_starts)} - exit\n'

    picked_start = int(input(options))
    while picked_start < 0 or picked_start > len(possible_starts):
        picked_start = int(input('choose a valid number!\n' + options))
    if picked_start == len(possible_starts):
        return
    picked_start = possible_starts[picked_start]
    process_to_generate_the_chain.append(picked_start)
    generated_chain = picked_start.split('-> ')[1]
    non_terminals_in_the_chain = [non_terminal for non_terminal in generated_chain if non_terminal in _variables]
    transitions_to_pick_from = [transition for transition in _productions
                                if non_terminals_in_the_chain[0] in
                                transition.split('-> ')[0] and _initial not in transition]
    while True:
        print('Generated Chain Until Now: ' + generated_chain + '\n')
        options = ''
        for i in range(len(transitions_to_pick_from)):
            options += f'{i} - {transitions_to_pick_from[i]}\n'
        options += f'{len(transitions_to_pick_from)} - exit\n'
        picked_transition = input(options)
        picked_transition = int(picked_transition)
        while picked_transition < 0 or picked_transition > len(transitions_to_pick_from):
            picked_transition = input('choose a valid number!\n' + options)
        if picked_transition == len(transitions_to_pick_from):
            break
        picked_transition = transitions_to_pick_from[picked_transition]
        process_to_generate_the_chain.append(picked_transition)
        new_str_to_the_chain = picked_transition.split('-> ')[1]
        for i in range(len(generated_chain)):
            if i != len(generated_chain) - 1:
                if picked_transition.split('-> ')[1].endswith('epsilon'):
                    new_str_to_the_chain = picked_transition.split('-> ')[1][:-7]
            if picked_transition.split('-> ')[0] == generated_chain[i]:
                new_chain = generated_chain[:i] + new_str_to_the_chain \
                            + generated_chain[i + 1:]
                generated_chain = new_chain
                break

        non_terminals_in_the_chain = [non_terminal for non_terminal in generated_chain if non_terminal in _variables]
        if len(non_terminals_in_the_chain) == 0:
            print('Process chosen to generate the chain: ')
            print(process_to_generate_the_chain)
            print('Generated Chain Final Result: ' + generated_chain + '\n')
            break
        transitions_to_pick_from = [transition for transition in _productions
                                    if non_terminals_in_the_chain[0] in
                                    transition.split('-> ')[0] and _initial not in transition]


def free_of_context_grammar(_terminals: str, _variables: str, _initial: str, _productions: List[str]):
    if _terminals == '' or _variables == '' or _initial == '' or len(_productions) == 0 or \
            _initial not in _variables.split(','):
        raise 'Invalid data, please verify your input data'

    mode = input("choose witch mode do you wanna use:\n1 - fast mode\n2 - detailed mode\n")
    if mode == '1':
        fast_mode(_terminals, _variables, _initial, _productions)
    elif mode == '2':
        detailed_mode(_terminals, _variables, _initial, _productions)
    else:
        while mode not in ['1', '2']:
            mode = input('please, select a valid option!\n1 - fast mode\n2 - detailed mode\n')


if __name__ == '__main__':
    with open('test.txt') as f:
        lines = f.readlines()
    terminals = lines[0].split('=')[1].strip()
    variables = lines[1].split('=')[1].strip()
    initial = lines[2].split('=')[1].strip()
    productions = [production.strip() for production in lines[4::]]
    free_of_context_grammar(terminals, variables, initial, productions)
    f.close()
