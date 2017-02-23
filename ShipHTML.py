






#*******************
# Ship HTML Chunks
#*******************

def get_anthem():

def get_ovation():

def get_quantum():

def get_allure():

def get_harmony():

def get_oasis():

def get_freedom():

def get_independence():

def get_liberty():

def get_adventure():

def get_explorer():

def get_mariner():

def get_navigator():

def get_voyager():

def get_brilliance():

def get_serenade():

def get_enchantment():

def get_grandeur():

def get_legend():

def get_rhapsody():

def get_vision():

def get_majesty():

def get_empress():

def switch_ship(ship):

    ship_name = ship.lower()

    if(ship_name == 'anthem of the seas'):
        chunk = get_anthem()
    elif(ship_name == 'ovation of the seas'):
        chunk = get_ovation()
    elif(ship_name == 'quantum of the seas'):
        chunk = get_quantum()
    elif(ship_name == 'allure of the seas'):
        chunk = get_allure()
    elif(ship_name == 'harmony of the seas'):
        chunk = get_harmony()
    elif(ship_name == 'oasis of the seas'):
        chunk = get_oasis()
    elif(ship_name == 'freedom of the seas'):
        chunk = get_freedom()
    elif(ship_name == 'independence of the seas'):
        chunk = get_independence()
    elif(ship_name == 'liberty of the seas'):
        chunk = get_liberty()
    elif(ship_name == 'adventure of the seas'):
        chunk = get_adventure()
    elif(ship_name == 'explorer of the seas'):
        chunk = get_explorer()
    elif(ship_name == 'mariner of the seas'):
        chunk = get_mariner()
    elif(ship_name == 'navigator of the seas'):
        chunk = get_navigator()
    elif(ship_name == 'voyager of the seas'):
        chunk = get_voyager()
    elif(ship_name == 'brilliance of the seas'):
        chunk = get_brilliance()
    elif(ship_name == 'jewel of the seas'):
        chunk = get_jewel()
    elif(ship_name == 'radiance of the seas'):
        chunk = get_radiance()
    elif(ship_name == 'serenade of the seas'):
        chunk = get_serenade()
    elif(ship_name == 'enchantment of the seas'):
        chunk = get_enchantment()
    elif(ship_name == 'grandeur of the seas'):
        chunk = get_grandeur()
    elif(ship_name == 'legend of the seas'):
        chunk = get_legend()
    elif(ship_name == 'rhapsody of the seas'):
        chunk = get_rhapsody()
    elif(ship_name == 'vision of the seas'):
        chunk = get_vision()
    elif(ship_name == 'majesty of the seas'):
        chunk = get_majesty()
    elif(ship_name == 'empress of the seas'):
        chunk = get_empress()
    else:
        chunk = "SHIP NOT FOUND"

    return chunk
