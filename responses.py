import textwrap


def handle_set_response(message) -> str:
    p_message = message.lower()
    return "Your keystone has been set to " + message + " for the week." 


def handle_keys_response(keys) -> str:
    key_list = ""
    pair_separator = 2
    for keystone in keys:
        for key in keystone:
            pair_separator += 1
            data_string = (f"{key}: {keystone[key]}")
            user_info = data_string.split('\'')
            if pair_separator % 2 != 0:
                key_list += user_info[3] + " "
            else:
                key_list += user_info[3] + "\n"
    return key_list
    

def handle_help_response():
    help_list ='''
    Usage: !kc <command> [arguments] \n
    Commands: \n
    set         Sets the user\'s keystone and level. Accepts a keystone abbreviation followed by the key level as an arugment (I.E. NELTH20). See dungeon abbreviations for valid abberviations.
    keys        Lists the keys of all users for the week.
    help        Returns a list of all commands and basic interfacing help.

    --Dungeon Abbreviations (Dragonflight Season 2)--\n
    NL      -      Neltharion\'s Lair
    UNDR    -      The Underrot
    FH      -      Freehold
    VP      -      The Vortex Pinnacle
    BH      -      Brackenhide Hollow
    HOI     -      Halls of Infusion
    ULD     -      Uldaman: Legacy of Tyr
    NELT    -      Neltharus
    '''
    return textwrap.dedent(help_list)


def handle_unknown_response():
    return "Invalid command, please try again or type \"!kc help\" to see a list of valid commands."
