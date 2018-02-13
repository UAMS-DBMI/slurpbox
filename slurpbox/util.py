def format_sizeof(num, suffix='', divisor=1000):
    """
    Formats a number (greater than unity) with SI Order of Magnitude
    prefixes.
    Parameters
    ----------
    num  : float
        Number ( >= 1) to format.
    suffix  : str, optional
        Post-postfix [default: ''].
    divisor  : float, optionl
        Divisor between prefixes [default: 1000].
    Returns
    -------
    out  : str
        Number with Order of Magnitude SI unit postfix.
    """
    for unit in ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 999.95:
            if abs(num) < 99.95:
                if abs(num) < 9.995:
                    return '{0:1.2f}'.format(num) + unit + suffix
                return '{0:2.1f}'.format(num) + unit + suffix
            return '{0:3.0f}'.format(num) + unit + suffix
        num /= divisor
    return '{0:3.1f}Y'.format(num) + suffix



if __name__ == '__main__':
    print(format_sizeof(547294757398, 'B'))
