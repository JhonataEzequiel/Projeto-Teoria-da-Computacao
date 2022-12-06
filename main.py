import random
from typing import List


def add_string_to_chain(generated_chain: str, picked_transition: str) -> str:
    new_str_to_the_chain = picked_transition.split('-> ')[1]
    for i in range(len(generated_chain)):
        if i != len(generated_chain) - 1:
            if picked_transition.split('-> ')[1].endswith('epsilon'):
                new_str_to_the_chain = picked_transition.split('-> ')[1][:-7]
        if picked_transition.split('-> ')[0] == generated_chain[i]:
            new_chain = generated_chain[:i] + new_str_to_the_chain \
                        + generated_chain[i + 1:]
            generated_chain = new_chain
            return generated_chain


def get_non_terminals_in_chain(generated_chain: str, _variables: str) -> List[str]:
    non_terminals_in_the_chain = [non_terminal for non_terminal in generated_chain if
                                  non_terminal in _variables]
    return non_terminals_in_the_chain


def fast_mode(_terminals: str, _variables: str, _initial: str, _productions: List[str]):
    started = False
    stop = False
    process_to_generate_the_chain = []
    generated_chain = []
    processes_used = []
    remove_transition = False
    removed_transitions_this_time = []
    generated_chains = []
    chain_in_iterations = []
    iteration = 0
    picked_start = ''
    possible_starts = [start for start in _productions if start[0] == _initial]
    while not stop:

        if not started:
            picked_start = random.choice(possible_starts)
            process_to_generate_the_chain = [picked_start]
            generated_chain = picked_start.split('-> ')[1]
            if generated_chain.endswith('epsilon'):
                generated_chain = generated_chain[:-7]
            chain_in_iterations = [generated_chain]
            non_terminals_in_the_chain = get_non_terminals_in_chain(generated_chain, _variables)
            if len(non_terminals_in_the_chain) == 0:
                possible_starts.remove(picked_start)
            started = True

        if remove_transition:
            if len(process_to_generate_the_chain) == 1:
                if len(possible_starts) == 0:
                    print('No more possible transitions to take to generate another chain!')
                    break
                possible_starts.remove(picked_start)
                if len(possible_starts) == 0:
                    print('No more possible transitions to take to generate another chain!')
                    break
                picked_start = random.choice(possible_starts)
                process_to_generate_the_chain = [picked_start]
                generated_chain = picked_start.split('-> ')[1]
                chain_in_iterations = [generated_chain]
            chain_in_iterations.pop()
            generated_chain = chain_in_iterations[-1] if len(chain_in_iterations) > 0 else \
                picked_start.split('-> ')[1] if len(possible_starts) > 0 else None
            if generated_chain is None:
                print('No more possible transitions to take to generate another chain!')
                break

        non_terminals_in_the_chain = get_non_terminals_in_chain(generated_chain, _variables)

        if len(non_terminals_in_the_chain) > 0:
            transitions_to_pick_from = [
                transition for transition in _productions
                if non_terminals_in_the_chain[0] in transition.split('-> ')[0]
            ]
            if remove_transition:
                for transition in removed_transitions_this_time:
                    if transition in transitions_to_pick_from:
                        transitions_to_pick_from.remove(transition)
                if len(transitions_to_pick_from) == 0:
                    chain_in_iterations.pop()
                    if len(chain_in_iterations) > 0:
                        generated_chain = chain_in_iterations[-1]
                        non_terminals_in_the_chain = get_non_terminals_in_chain(generated_chain, _variables)
                        transitions_to_pick_from = [
                            transition for transition in _productions
                            if non_terminals_in_the_chain[0] in transition.split('-> ')[0]
                        ]
                    else:
                        print('no more chains!')
                        break
                process_to_generate_the_chain.pop()
                remove_transition = False
                removed_transitions_this_time = []
            picked_transition = random.choice(transitions_to_pick_from)
            process_to_generate_the_chain.append(picked_transition)
            generated_chain = add_string_to_chain(generated_chain, picked_transition)
            chain_in_iterations.append(generated_chain)

        else:

            if process_to_generate_the_chain not in processes_used and generated_chain not in generated_chains:
                print('Generated Chain Final Result: ' + generated_chain)
                print('Process to generate the chain: ')
                print(process_to_generate_the_chain)
                print('Derivation on left side: ')
                print(chain_in_iterations)
                processes_used.append(process_to_generate_the_chain)
                generated_chains.append(generated_chain)
                opt = int(input('wanna generate another chain?\n1 - Yes\n2 - No'))

                while opt < 1 or opt > 2:
                    opt = int(input('Choose a valid number!\n1 - Yes\n2 - No'))

                if opt == 2:
                    stop = True

                elif opt == 1:
                    started = False
                    remove_transition = False
                    removed_transitions_this_time = []

            else:
                remove_transition = True
                removed_transitions_this_time.append(process_to_generate_the_chain[-1])

        iteration += 1


def detailed_mode(_terminals: str, _variables: str, _initial: str, _productions: List[str]):
    process_to_generate_the_chain = []
    chain_in_iterations = []
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
    chain_in_iterations.append(generated_chain)
    non_terminals_in_the_chain = [non_terminal for non_terminal in generated_chain if non_terminal in _variables]
    if len(non_terminals_in_the_chain) == 0:
        print('Process chosen to generate the chain: ')
        print(process_to_generate_the_chain)
        print('Generated Chain Final Result: ' + generated_chain[:-7] + '\n')
        return
    transitions_to_pick_from = [transition for transition in _productions
                                if non_terminals_in_the_chain[0] in
                                transition.split('-> ')[0]]
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
        generated_chain = add_string_to_chain(generated_chain, picked_transition)
        chain_in_iterations.append(generated_chain)

        non_terminals_in_the_chain = [non_terminal for non_terminal in generated_chain if non_terminal in _variables]

        if len(non_terminals_in_the_chain) == 0:
            print('Process chosen to generate the chain: ')
            print(process_to_generate_the_chain)
            print('Derivation on left side: ')
            print(chain_in_iterations)
            print('Generated Chain Final Result: ' + generated_chain + '\n')
            break

        transitions_to_pick_from = [transition for transition in _productions
                                    if non_terminals_in_the_chain[0] in
                                    transition.split('-> ')[0]]


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
