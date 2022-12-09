import random
from typing import List


def add_string_to_chain(generated_chain: str, picked_transition: str) -> str:
    """
    This function returns a new string generated with the combination of the generated chain so far and the next
    transition
    :param generated_chain: generated chain so far
    :param picked_transition: next transition to overwrite the non-terminal symbol
    :return: new created chain
    """
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
    """
    returns a list of all non-terminals in the generated chain so far
    """
    non_terminals_in_the_chain = [non_terminal for non_terminal in generated_chain if
                                  non_terminal in _variables]
    return non_terminals_in_the_chain


def fast_mode(_terminals: str, _variables: str, _initial: str, _productions: List[str]):
    """
    This function generates a new chain overwriting the most left non-terminal symbol with a production chose randomly.
    All parameters are the same as the free_of_context_grammar function in main.py
    """
    started = False
    stop = False

    # shows all the chosen transitions to get to the final result of the chain
    process_to_generate_the_chain = []

    generated_chain = []
    processes_used = []
    remove_transition = False
    removed_transitions_this_time = []
    generated_chains = []

    # shows the most left derivation so far
    chain_in_iterations = []

    iteration = 0
    picked_start = ''
    possible_starts = [start for start in _productions if start[0] == _initial]
    while not stop:

        if not started:
            # select one of the possible ways to start the chain, and removes the chosen option if it only has terminals
            picked_start = random.choice(possible_starts)
            process_to_generate_the_chain = [picked_start]
            generated_chain = picked_start.split('-> ')[1]
            if generated_chain.endswith('epsilon'):
                # this function accepts transitions that ends with epsilon, but also have other symbols before it
                # example: in 'BAepsilon', it will only consider BA
                generated_chain = generated_chain[:-7]
            chain_in_iterations = [generated_chain]
            non_terminals_in_the_chain = get_non_terminals_in_chain(generated_chain, _variables)
            if len(non_terminals_in_the_chain) == 0:
                possible_starts.remove(picked_start)
            started = True

        non_terminals_in_the_chain = get_non_terminals_in_chain(generated_chain, _variables)

        if len(non_terminals_in_the_chain) > 0:
            transitions_to_pick_from = [
                transition for transition in _productions
                if non_terminals_in_the_chain[0] in transition.split('-> ')[0]
            ]
            if remove_transition:
                # if all possible chains at that moment were generated already with the given transitions, it will remove
                # them and step back once in the chain, making it possible to create other chains, as long as there are
                # transitions to pick from.
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
                        print('no more possible chains!')
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
                # if the chain was not generated before, it is shown to the user, who can choose to generate another
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
    """
    This function lets the user choose what productions will be used to generate a chain
    """
    process_to_generate_the_chain = []
    chain_in_iterations = []
    possible_starts = [start for start in _productions if start[0] == _initial]

    options = ''
    for i in range(len(possible_starts)):
        options += f'{i} - {possible_starts[i]}\n'
    options += f'{len(possible_starts)} - exit\n'

    # choosing first production
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

    # if the chosen start has no more non-terminals symbols, it stops
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

        # lets the user decide what transition will be used next
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
