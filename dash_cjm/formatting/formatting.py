import codecs
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
}

# unicode_superscript = {str(num): '\u208' + str(num) for num in range(0, 9)}


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
    assert isinstance(string, str), 'The input string must be of type str, not {0}'.format(type(string))
    new = ''.join([unicode_subscript[s] if s.isdigit() else s for s in list(string)])
    return new
