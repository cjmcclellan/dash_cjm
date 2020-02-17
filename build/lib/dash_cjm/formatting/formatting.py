import codecs
from math import log10, floor
"""
These functions will help deal with formatting in Dash, such as subscripting and greek letter.

"""

# unicode_subscript = {str(num): codecs.decode('\u208' + str(num), 'unicode_escape') for num in range(0, 9)}
unicode_subscript = {
    '1': '\u2081',
    '2': '\u2082',
    '3': '\u2083',
    '4': '\u2084',
    '5': '\u2085',
    '6': '\u2086',
    '7': '\u2087',
    '8': '\u2088',
    '9': '\u2089',
    'o': '\u2092',
    'x': '\u2093',
    'm': '\u2098',
    'i': '\u1d62',
    'n': '\u2099',
}

unicode_superscript = {

    '1': '\u00b9',
    '2': '\u00b2',
    '3': '\u00b3',
    '-': '\u207B',
    'bullet': '\u2022',
}

# unicode_superscript = {str(num): '\u208' + str(num) for num in range(0, 9)}

unicode_symbols = {
    'mu': '\u03BC',
    'omega': '\u03A9',
}


def get_symbol_unicode(symbol):
    """
    Get the unicode for the requested symbol.  If not it list, return the symbol name
    Args:
        symbol (str): Name of the desired symbol

    Returns:
        str or unicode of the symbol
    """
    return unicode_symbols.get(symbol, symbol)


def get_superscript_unicode(value):
    """
    Get the superscript unicode for the requested value.  If not it list, return the value name
    Args:
        value (str): Name of the desired superscript value

    Returns:
        str or unicode of the superscript value
    """
    return unicode_superscript.get(value, value)


def get_subscript_unicode(value):
    """
    Get the subscript unicode for the requested value.  If not it list, return the value name
    Args:
        value (str): Name of the desired subscript value

    Returns:
        str or unicode of the subscript value
    """
    return unicode_subscript.get(value, value)


def convert_num_subscript(string):
    """
    Unicode subscript all digits in a string.
    Args:
        string (str): A string with digits

    Returns:
        str: The string with digits all subscript

    Examples:
        >>>convert_num_subscript('MoS2')
        >>>'MoS\u2082'
    """
    if isinstance(string, float):
        return string
    assert isinstance(string, str), 'The input string must be of type str, not {0}'.format(type(string))
    new = ''.join([unicode_subscript[s] if s.isdigit() else s for s in list(string)])
    return new


def create_dropdown_options(data):
    """
    Converts a list of strings to a dict for dash dropdown options
    Args:
        data (list): List of strings of the options

    Returns: list of dictionary options

    """
    assert isinstance(data, list), 'You must give a list of strings.'
    result = []
    for d in data:
        result.append({'value': create_dash_option(d), 'label': d})

    return result


def round_to_n(x, n):
    if x == 0:
        return 0
    return round(x, -int(floor(log10(abs(x)))) + (n - 1))


def create_dash_option(string):
    """
    Converts a generic string to be compatible with dash options for dropdown values
    Args:
        string (str):

    Returns:

    """
    assert isinstance(string, str), 'You must pass a string object'
    string.replace(' ', '_')
    return string
