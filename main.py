from chain_getter import *


def free_of_context_grammar(_terminals: str, _variables: str, _initial: str, _productions: List[str]):
    """
    this function will call the chosen function by the user to generate the chain (fast mode or detailed mode)
    :param _terminals: all terminals symbols
    :param _variables: all non-terminals symbols
    :param _initial: the initial non-terminal symbol
    :param _productions: all possible productions
    :return:
    """

    # treating data
    if _terminals == '' or _variables == '' or _initial == '' or len(_productions) == 0 or \
            _initial not in _variables.split(','):
        raise 'Invalid data, please verify your input data'

    mode = input("choose witch mode do you wanna use:\n1 - fast mode\n2 - detailed mode\n")

    while mode not in ['1', '2']:
        mode = input('please, select a valid option!\n1 - fast mode\n2 - detailed mode\n')

    if mode == '1':
        fast_mode(_terminals, _variables, _initial, _productions)
    elif mode == '2':
        detailed_mode(_terminals, _variables, _initial, _productions)


if __name__ == '__main__':
    archive_name = 'w is odd and the middle symbol is 0.txt'
    with open(archive_name) as f:
        lines = f.readlines()
    terminals = lines[0].split('=')[1].strip()
    variables = lines[1].split('=')[1].strip()
    initial = lines[2].split('=')[1].strip()
    productions = [production.strip() for production in lines[4::]]
    free_of_context_grammar(terminals, variables, initial, productions)
    f.close()
