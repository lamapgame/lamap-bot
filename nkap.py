def has_enough_nkap(nkap, bet):
    ''' Check if the player has enough nkap to bet '''
    if (nkap >= (bet*2)):
        return True
    return False
