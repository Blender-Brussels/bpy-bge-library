# Copyright (C) Labomedia February 2012
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
#############################################################################

import GameLogic as gl
import socket
from OSC.OSC import decodeOSC

# Get dict with all instance key =number value= tuple of ip, port, buffer size
config = gl.listen

# gl.connected[n], gl.socket[n] are attribut of gamelogic and set in init.py

# ------------------- main -------------------- #
# launch every socket define in gl.listen in config.py
def main():
    # Get osc data
	for key in config.keys():
        plug_and_listen(key)

    # Print and save every 60 frames
    if gl.tempo == 5:
        gl.tempo = 0
        print_in_terminal()
        save_in_file()
    gl.tempo += 1

# ------------------ listen ------------------- #
def plug_and_listen(n):
    '''Get osc data'''
    ip = config[n][0]
    port = config[n][1]
    buffer_size = config[n][2]

    # Connect Blender
    if not gl.connected[n] :
        gl.socket[n] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            gl.socket[n].bind((ip, port))
            gl.socket[n].setblocking(0)
            gl.socket[n].settimeout(0.002)
            gl.socket[n].setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)
            print('Plug : IP = {} Port = {} Buffer Size = {} Socket = {}'.format(ip, port, buffer_size, n))
            gl.connected[n] = True
        except:
            print('No connected to IP = {} Port = {}'.format(ip, port))
            pass


    # If Blender connected
    if gl.connected[n] :
        try:
            raw_data = gl.socket[n].recv(buffer_size)
            data = decodeOSC(raw_data)
            #print(data)
            convert_data(data, n)
        except socket.error:
            pass

# ------------------- set data in variable_stats -------------------- #
def add_in_stat_dict(var_name, xxx):
    # xxx is not a list but int or float
    if isinstance(xxx, int) and isinstance(xxx, float):
        # xxx is the current value
        # gl.variable_stat[variable] = [current, average, mini, maxi]
        if str(var_name) in gl.variable_stat :
            if xxx < gl.variable_stat[var_name][2]:
                var_mini = xxx
            else:
                var_mini = gl.variable_stat[var_name][2]
            if xxx > gl.variable_stat[var_name][3]:
                var_maxi = xxx
            else:
                var_maxi = gl.variable_stat[var_name][3]
        else:
            var_mini = xxx
            var_maxi = xxx
        # I am lazy, it is median
        var_average =(abs(var_maxi) - abs(var_mini))/2.0

        gl.variable_stat[str(var_name)] = [xxx, var_average, var_mini, var_maxi]
    #elif isinstance(xxx, list):
        # TODO if xxx is list

# ------------------- set data in attribut of GameLogic -------------------- #
def convert_data(data, n):
    '''Convert OSC message in variable'''
    # if list
    if isinstance(data, list):
        if len(data) > 1 :
            # if bundle cut bundle and time
            if data[0]=='#bundle':
                # Cut the two first item
                data = data[2:]
            test_if_list_of_list(data, n)
    else:
        pass


def test_if_list_of_list(data, n):
    '''test if first in list is a list'''
    if isinstance(data[0], list):
        for i in range(len(data)):
            list_to_var(data[i])
    else:
        list_to_var(data, n)


def list_to_var(data, n):
    '''Set value in variable'''
    # First item is the tag, otherwise message in not osc
    var_name = name(data[0], n)
    # if the second is type of all values, example 'iif
    if isinstance(data[1], str) or data[1][0] == ",":
        # cut the 2 first
        data = data[2:]
    # cut the first: msg don't respect OSC format
    else:
        data = data[1:]
    # data is always list, convert list to int or float or str if len=1
    if len(data)==1:
        data = data[0]
    # Set attr to gamelogic
    setattr(gl, var_name, data)
    # Set data as value in attribution dict
    print( var_name )
    gl.attribution[var_name] = data
    add_in_stat_dict(var_name, data)


def name(s, n):
    '''Convert s in variable name'''
    # Cut the first / if
    if s[0] == '/':
        s = s[1:]
    # add socket number in front to identify the socket and separate identical name
    # so the first item is never a number
    s = 'n' + str(n) + '_' + s
    # Replace / or - or , with _ (add str in list if necessary)
    for i in ['/', '-', ',']:
        s = s.replace(i, '_')
    return s

# ------------------- print -------------------- #
def print_in_terminal():
    '''Print in terminal all variables and values to debug'''
    print ("Variable type and value:",)
    for key, value in gl.attribution.items():
        print ('{} = {}'.format(key, getattr(gl, key)))
    print()

# ------------------- help.txt -------------------- #
def save_in_file():
    '''Save in file help.txt'''
    help_file = open('help.txt', 'w')
    help_file.writelines('All datas received with OSC')

    help_file.write(3*'\n')

    help_file.write('Put this dictionary "gl.attribution" in init.py of OSC_work ')
    help_file.write('\n')
    help_file.write('gl.attribution = { \n')
    for key in sorted(gl.attribution):
        help_file.write('"{}": {},\n'.format(str(key), ''.join(repr(0))))
    help_file.write('}')
    help_file.write(2*'\n')

    help_file.write('Type    ==>      Variable               Value ')
    help_file.write('\n')
    for key, value in gl.attribution.items():
        help_file.write('{} ==> {} = {} \n'.format(type(value), key, value))

    help_file.write(2*'\n')

    help_file.write('All variable attribut of gl')
    help_file.write('\n')
    for key in gl.attribution.keys():
        help_file.write('{} = gl.{} \n'.format(key, key))

    help_file.write('\n')

    help_file.write('Variable    Median    Mini     Maxi')
    help_file.write('\n')
    for key, value in gl.variable_stat.items():
        help_file.write('{} Median = {} Mini = {} Maxi = {} \n'.format( str(key), value[1], value[2], value[3]))

    help_file.close()


# ------------------- main -------------------- #
main()
