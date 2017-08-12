from __future__ import absolute_import, unicode_literals


def digit2str(digit, prefix_len=0, total_len=0):
    digit_str = str(digit)
    if prefix_len != 0:
        return '0' * prefix_len + digit_str
    elif total_len != 0:
        return '0' * (total_len - len(digit_str)) + digit_str
    else:
        return digit_str
