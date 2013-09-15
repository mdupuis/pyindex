# -*- coding: utf-8 -*-

from collections import defaultdict

morton16 = defaultdict(lambda: list())
morton32 = defaultdict(lambda: list())


for i in range(256):
    def mangle(x, y):
        return (((i >> x) & 1) << y)

    # 2x8
    morton16[1].append(mangle(7, 15) + mangle(6, 7) + mangle(5, 14) + \
                       mangle(4, 6) + mangle(3, 13) + mangle(2, 5) + \
                       mangle(1, 12) + mangle(0, 4))
    morton16[0].append(mangle(7, 11) + mangle(6, 3) + mangle(5, 10) + \
                       mangle(4, 2) + mangle(3, 9) + mangle(2, 1) + \
                       mangle(1, 8) + mangle(0, 0))


    # 4x8
    morton32[3].append(mangle(7, 31) + mangle(6, 23) + mangle(5, 15) + \
                       mangle(4, 7) + mangle(3, 30) + mangle(2, 22) + \
                       mangle(1, 14) + mangle(0, 6))
    morton32[2].append(mangle(7, 29) + mangle(6, 21) + mangle(5, 13) + \
                       mangle(4, 5) + mangle(3, 28) + mangle(2, 20) + \
                       mangle(1, 12) + mangle(0, 4))
    morton32[1].append(mangle(7, 27) + mangle(6, 19) + mangle(5, 11) + \
                       mangle(4, 3) + mangle(3, 26) + mangle(2, 18) + \
                       mangle(1, 10) + mangle(0, 2))
    morton32[0].append(mangle(7, 25) + mangle(6, 17) + mangle(5, 9) + \
                       mangle(4, 1) + mangle(3, 24) + mangle(2, 16) + \
                       mangle(1, 8) + mangle(0, 0))


for i in range(2):
    print ', '.join(map(str, map(hex, morton16[i])))


for i in range(4):
    print ', '.join(map(str, morton16[i]))
