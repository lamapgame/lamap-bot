def has_enough_nkap(nkap, bet):
    ''' Check if the player has enough nkap to bet '''
    if (nkap >= 0 and nkap > bet):
        return True
    return False
