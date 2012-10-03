import texttable as tt

class bcolors:
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    WHITE = ''


def print_yellow(string):
    print_color(bcolors.YELLOW, string)

def print_red(string):
    print_color(bcolors.RED, string)

def print_blue(string):
    print_color(bcolors.BLUE, string)

def print_green(string):
    print_color(bcolors.GREEN, string)

def print_purple(string):
    print_color(bcolors.PURPLE, string)

def print_white(string):
    print string

def print_color(type, string):
    print get_color_string(type, string)

def get_color_string(type, string):
    end = bcolors.ENDC
    if type == bcolors.WHITE:
        end = ''
    return '%s%s%s' % (type, string, end)

def print_dict(color_dict, one_line=False):
    print_list = []
    for k,v in color_dict.iteritems():
        print_list.append(get_color_string(k,v))
    if one_line:
        print '\t'.join(print_list)
    else:
        for p in print_list:
            print p

def print_ordered_cards(card_list):
    print_list = []
    for color, value in card_list:
        print_list.append('%*s' % (20, get_color_string(color,value)))
    print ' '.join(print_list)

def prepare_card_row(card_list):
    print_list = []
    for color, value in card_list:
        print_list.append(get_color_string(color,value))
    return print_list

def print_color_table(card_rows):

    tab = tt.Texttable()

    x = [] # The empty row will have the header
    tab.add_rows(card_rows)
    tab.set_cols_align(['r','r','r','r','r','r'])
    tab.header(['How to Acquire', 'Card Type', 'Card Name', 'Buy', 'Kill', 'Worth'])
    print tab.draw()

