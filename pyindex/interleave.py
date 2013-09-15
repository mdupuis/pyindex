# -*- coding: utf-8 -*-

"""
This is the equivalent of what you find in morton.py except that these
functions do not use lookup tables to do the work and that you can
(de)interleave 3 integers together.

In theory, these functions could work regardless of the size of the
integers you pass in. This should come later, altough you should expect
them to be slower.
"""


def part1by1(n):
    """
    Inserts one 0 bit between each bit in `n`.

    n: 32-bit integer
    """
    n &= 0x0000FFFF

    n = (n | (n << 8)) & 0x00FF00FF
    n = (n | (n << 4)) & 0x0F0F0F0F
    n = (n | (n << 2)) & 0x33333333
    n = (n | (n << 1)) & 0x55555555

    return n


def part1by2(n):
    """
    Inserts two 0 bits between each bit in `n`.

    n: 32-bit integer
    """
    n &= 0x000003FFF

    n = (n ^ (n << 16)) & 0xFF0000FF
    n = (n ^ (n << 8)) & 0x0300F00F
    n = (n ^ (n << 4)) & 0x030C30C3
    n = (n ^ (n << 2)) & 0x09249249

    return n


def unpart1by1(n):
    """
    Gets every other bits from `n`.

    n: 32-bit integer
    """
    n &= 0x55555555

    n = (n ^ (n >> 1)) & 0x33333333
    n = (n ^ (n >> 2)) & 0x0F0F0F0F
    n = (n ^ (n >> 4)) & 0x00FF00FF
    n = (n ^ (n >> 8)) & 0x0000FFFF

    return n


def unpart1by2(n):
    """
    Gets every third bits from `n`.

    n: 32-bit integer
    """
    n &= 0x09249249

    n = (n ^ (n >> 2)) & 0x030C30C3
    n = (n ^ (n >> 4)) & 0x0300F00F
    n = (n ^ (n >> 8)) & 0xFF0000FF
    n = (n ^ (n >> 16)) & 0x000003FF

    return n


def interleave2(x, y):
    """
    Interleaves two integers.
    """
    return part1by1(x) | (part1by1(y) << 1)


def deinterleave2(n):
    """
    Deinterleaves an integer into two integers.
    """
    return unpart1by1(n), unpart1by1(n >> 1)


def interleave3(x, y, z):
    """
    Interleaves three integers.
    """
    return part1by2(x) | (part1by2(y) << 1) | (part1by2(z) << 2)


def deinterleave3(n):
    """
    Deinterleaves an integer into three integers.
    """
    return unpart1by2(n), unpart1by2(n >> 1), unpart1by2(n >> 2)
