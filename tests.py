def div2(n):
    """test si divisible par 2"""
    if n % 2 == 0:
        return True
    else:
        return False
assert div2(2) == True
assert(div2(3) == False, "3 est divisible par 2")
assert div2(4) == True


def div3(n):
    """test si divisible par 3"""
    if n % 3 == 0:
        return True
    else:
        return False
assert div3(2) == False
assert div3(3) == True
assert div3(4) == False

def div5(n):
    """test si divisible par 5"""
    if n % 5 == 0:
        return True
    else:
        return False
assert div5(2) == False
assert div5(3) == False
assert div5(5) == True

def divN(N,nb):
    """test si divisible par n en (nb divisible par N) """
    if nb % N == 0:
        return True
    else:
        return False
assert divN(2,2) == True
assert divN(3,3) == True
assert divN(6,5) == False