import tkinter as tk
import ctypes
from ctypes import windll
import ctypes.wintypes
import time
import os
import win32ui


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_ulong), ("y", ctypes.c_ulong)]

user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
hdc = windll.user32.GetDC(0)
point = POINT()


class Pixel:
    def __init__(self, red = 0, green = 0, blue = 0):
        self.r = red
        self.g = green
        self.b = blue

        
class Line:
    def __init__(self, start_coords, end_coords, colour):#(start_coords = (0,0), end_coords = (0,1), colour = Pixel(0,0,0)):
        self.startxy = start_coords
        self.endxy = end_coords
        self.colour = colour
        self.startx = start_coords[0]
        self.starty = start_coords[1]
        self.endx = end_coords[0]
        self.endy = end_coords[1]
        self.length = self.endx - self.startx + 1


class Word:
    def __init__(self, name, lcoords, rcoords):
        self.name = name
        self.lcoords = lcoords
        self.rcoords = rcoords
        


def colour_check(pixel):
    
    r = pixel.r//25
    g = pixel.g//25
    b = pixel.b//25
    if r == g and g == b:
        r == pixel.r//32
        
        if r == 0:
            return "black"
        elif r <= 2:
            return "dark grey"
        elif r <= 7:
            return "grey"
        else:
            return "white"
       
       
    elif r > g and g == b:
        return "red"
    elif r > g and g>b:
        return "orange"
    elif r == g and g>b:
        return "yellow"
    elif g>r and r>b:
        return "light green"
    elif g>b and b == r:
        return "green"
    elif g>b and b>r:
        return "blue green"
    elif b>g and g>r :
        return "light blue"
    elif b>g and g == r:
        return "dark blue"
    elif b>r and r>g:
        return "dark purple"
    elif b == r and r>g:
        return "purple pink"
    else:
        return "red pink"

    
def row_check (pixel):
    row = 0
    r = pixel.r//25
    g = pixel.g//25
    b = pixel.b//25
    colour = colour_check(pixel)
    if colour == ("red" or "orange" or "yellow"):
        row = r/2 + 4/2
    elif colour == ("green" or "light green"):
        row = g/2 + 4/2
    elif colour ==("blue green" or "light blue" or "blue" or "dark blue"):
        row = b/2 + r/2
    elif colour == ("dark purple" or "purple pink" or "red pink"):
        row = r/2 + g/2
    else:
        r == pixel.r//32
        row = r
                  
    return row


def colour_friends(pixel, pixel2):
    r = pixel.r//25
    g = pixel.g//25
    b = pixel.b//25

    r = pixel2.r//25
    g = pixel2.g//25
    b = pixel2.b//25
    
    colour = colour_check(pixel)
    colour2 = colour_check(pixel2)
    
    if colour == ("red"):
        return colour == colour2 or (colour2 == ("orange" or "red pink") and row_check(pixel) == row_check(pixel2))
    elif colour == ("orange"):
        return colour == colour2 or (colour2 == "red" and row_check(pixel) == row_check(pixel2))
    elif colour == ("yellow"):
        return colour == colour2 # yellow has no friends
    elif colour == ("green"):
        return colour == colour2 or (colour2 == "light green" and row_check(pixel) == row_check(pixel2))
    elif colour == ("light green"):
        return colour == colour2 or (colour2 == ("green" or "blue green") and row_check(pixel) == row_check(pixel2))
    elif colour ==("blue green"):
        return colour == colour2 or (colour2 == ("light green" or "light blue") and row_check(pixel) == row_check(pixel2))
    elif colour ==("light blue"):
        return colour == colour2 or (colour2 == ("blue green" or "dark blue") and row_check(pixel) == row_check(pixel2))
    elif colour ==("dark blue"):
        return colour == colour2 or (colour2 == ("light blue" or "dark purple") and row_check(pixel) == row_check(pixel2)) 
    elif colour == ("dark purple"):
        row = row_check(pixel)
        nice_row = (row < 4) or (row > 6)
        return colour == colour2 or (((colour2 == "dark blue" and nice_row) or (colour2 == "purple pink")) and row_check(pixel) == row_check(pixel2))
    elif colour == ("purple pink"):
        row = row_check(pixel)
        nice_row = (row < 4) or (row > 6)
        return colour == colour2 or (((colour2 == "dark purple" and nice_row) or (colour2 == "red pink")) and row_check(pixel) == row_check(pixel2))
    elif colour == ("red pink"):
        return colour == colour2 or (colour2 == ("orange" or "red pink") and row_check(pixel) == row_check(pixel2))
    else:
        return colour == colour2
    return "error?e"


def close_rgb(pixel1, pixel2):
    
    colour1 = colour_check(pixel1)
    colour2 = colour_check(pixel2)
    row1 = row_check(pixel1)
    row2 = row_check(pixel2)
    same_colour_move = ((colour1 == colour2) and (abs(row1 - row2) <= 1))
    diff_colour_move = colour_friends(pixel1, pixel2)
    return (same_colour_move or diff_colour_move)

def sorted_lines (line_list):
    
    sorted_list = []
    temp_list = line_list
    while(temp_list != []):
        min_y = temp_list[0].starty
        min_x = temp_list[0].startx
        min_index = 0
        index = 0
        for line in temp_list:
            if line.starty < min_y:
                min_y = line.starty
                min_x = line.startx
                min_index = index
            elif line.starty == min_y:
                if line.startx < min_x:
                    min_x = line.startx
                    min_index = index
            index += 1
        sorted_list.append(temp_list[min_index])
        del temp_list[min_index]
    
    return sorted_list
                
           
def lineCatcher (x1,y1,x2,y2):
    window_name = "Diablo II"#"New Text Document - Notepad" #
    wd = win32ui.FindWindow(None, window_name)
    tempList = []
    print("Searching for lines... please wait...")
    for rows in range(y1, y2):
        #print("current row: ",rows)    
        #TODO: TEST LINE: #print("running, please be patient...")
        #TODO: TEST LINE: #print("Current row: " + str(rows))
        
        for columns in range(x1, x2):            
            dc = wd.GetWindowDC()
            j = dc.GetPixel(columns, rows)
            if j >= 0:
                r = j % 256
                g = (j // 256) % 256
                b = j // (256*256)
            dc.DeleteDC()
        
            if (tempList != []):
                last_line = tempList[-1]
                # check if same y values or not:
                if last_line.starty == rows:
                
                    last_pixel = Pixel(last_line.colour.r,
                                   last_line.colour.g,
                                   last_line.colour.b)
                    # CLOSE_RGB was original way, led to longer lines and
                    # faster load time, but maybe less accuracy
                    # pixel by pixel doesn't work with letter_sorting;
                    # need to attach pixels on same line if connected to
                    # make arm_counter, leg etc work
                    # if Pixel(r,g,b) == last_pixel:   
                    if close_rgb(Pixel(r,g,b), last_pixel):
                    
                        last_line.endxy = (columns, rows)
                        last_line.endx = columns
                        last_line.endy = rows
                        last_line.length = last_line.endxy[0] - last_line.startxy[0] + 1
                        
                        tempList[-1] = last_line
                    
                    else:
                        some_pixel = Pixel(r,g,b)
                        new_line = Line((columns,rows), (columns, rows), some_pixel)                        
                        tempList.append(new_line)
                else:
                    some_pixel = Pixel(r,g,b)
                    new_line = Line((columns,rows), (columns, rows), some_pixel)
                    tempList.append(new_line)
            else:
                # no lines so far
                new_line = Line((columns,rows), (columns, rows), Pixel(r,g,b))
                tempList.append(new_line)
                ## TODO: do I need templist?
    print("linelist size: ", len(tempList))
    return tempList

   

def max_height(line_list):
    start_y = line_list[0].starty
    end_y = start_y
    for line in line_list:
        end_y = max(start_y, line.starty)
    height = end_y - start_y + 1
    return height
        

def trunk_counter(line_list):
    # refactor code so it can accept smaller trunks)
    possible_x = []
    trunk_count = 0
    height = max_height(line_list)
    minx = line_list[0].startx
    maxx = line_list[0].endx
    possible_trunks = []
    for line in line_list:
        minx = min(minx, line.startx)
        maxx = max(maxx, line.endx)
    for x in range(minx, maxx+1):
        y_vals = []
        for line in line_list:
            if line.startx <= x <= line.endx:
                y_vals.append(line.starty)
        y_vals.sort()
        
        
        #print("x: " + str(x) + " y_vals: " + str(y_vals))
        
        if y_vals != []:
            longest_streak = 1
            current_streak = 1
            previous = y_vals[0]
            for num in y_vals:
                if num == (previous + 1):
                    
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                elif num != previous:
                    
                    longest_streak = max(longest_streak, current_streak)
                    current_streak = 1
                previous = num
            if longest_streak >= (height * 0.4):
                possible_trunks.append(x)
                
    # check for adjacent x?
    if possible_trunks != []:
        trunk_count = 1
        last_x = possible_trunks[0]
        for pots in possible_trunks:
            #print("POTS: " + str(pots))
            if (pots != last_x and abs(pots - last_x) > 1):
                trunk_count += 1
            last_x = pots
            
    return trunk_count

def arm_counter(line_list):
    arm_count = 0
    
    #find width of letter first
    start_x = line_list[0].startx
    end_x = start_x

    for line in line_list:
        start_x = min(start_x, line.startx)
        end_x = max(end_x, line.endx)

    length = end_x - start_x + 1
    #print("LENGTH: " + str(length))

    pot_arms = []
    for line in line_list:
        cur_length = line.endx - line.startx + 1
        if cur_length > 0.5 * length:
            arm_count += 1
            pot_arms.append(line)


    # now delete redundant "arms" i.e. adjacent lines
    cur_y = 0
    for arms in pot_arms:
        if cur_y == 0:
            cur_y = arms.starty
        elif abs(cur_y - arms.starty) == 1:
            arm_count -= 1
            cur_y = arms.starty
        else:
            cur_y = arms.starty
   
    
        
        
    #print("arm count: " + str(arm_count))
    return arm_count

def leg_counter(line_list):
    ''' criteria for legs:
- height at least 20% of letter
- end_x of leg > start_x (or vice versa '''
    #find height of line_list - similar to arm_counter
    leg_count = 0
    current_leg = line_list[0]
    start_y = current_leg.starty
    end_y = current_leg.starty

    for line in line_list:
        start_y = min(start_y, line.starty)
        end_y = max(end_y, line.endy)

    height = end_y - start_y + 1
    pot_leg_list = []
    for line in line_list:
        if pot_leg_list == []:
            pot_leg_list.append([line])
        else:
            connected = False
            for pot in pot_leg_list:
                for line2 in pot:
                    if abs(line.starty - line2.starty) == 1 and (line.endx > line2.startx and 
                     line.startx < line2.endx):
                        connected = True
                if connected == True:
                    pot.append(line)
    # a leg must be at least 20% the height of a letter
    for pots in pot_leg_list:
        if len(pots) > 2.9 * height:
            leg_count += 1
    return leg_count


def check_connection(some_line, some_other_line):
    delta_y = abs(some_line.starty - some_other_line.starty)
    colourpoo = rgb_to_hex(some_line.colour.r, some_line.colour.g, some_line.colour.b)
    ##print(str(some_line.startx)+","+str(some_line.starty)+","
    #      + str(some_line.endx)+","+str(some_line.endy) + "," + colourpoo)
    colourpoo = rgb_to_hex(some_other_line.colour.r, some_other_line.colour.g, some_other_line.colour.b)
    ##print(str(some_other_line.startx)+","+str(some_other_line.starty)+","
    #      + str(some_other_line.endx)+","+str(some_other_line.endy) + "," + colourpoo)
    s_x1 = some_line.startx
    ##print("s_x1: " + str(s_x1))
    e_x1 = some_line.endx
    ##print("e_x1: " + str(e_x1))
    s_x2 = some_other_line.startx
    ##print("s_x2: " + str(s_x2))
    e_x2 = some_other_line.endx
    ##print("e_x2: " + str(e_x2)) 
    if delta_y < 2:
        # start of line 2 is between, equal to
        # or exactly 1 away from start or end
        # of line 1
        if ((s_x1 - 1) <= s_x2 <= (e_x1 + 1) or
            (s_x2 - 1) <= s_x1 <= (e_x2 + 1)):
            #print("True")
            return True
        # similar, but for end of line 2
        elif ((s_x1 - 1) <= e_x2 <= (e_x1 + 1) or
              (s_x2 - 1) <= e_x1 <= (e_x2 + 1)):
            #print("True")
            return True
        else:
            #print("False")
            return False
    else:
        return False


def max_y(letter):
    maxy = 0
    for line in letter:
        
        if type(line) == list:
            print("bbrokenz")
        else:
            maxy = max(maxy, line.starty)
    return maxy


def letter_filter(letter_list):
    new_list = []
    for letter in letter_list:
        if((arm_counter(letter) < 4) and
           (leg_counter(letter) < 4) and
           (trunk_counter(letter) <4)):
            new_list.append(letter)
    return new_list
    

def potential_letter_sort(line_list):
    print("running potential letter sort....")
    letter_sorted = []
    temp_sorted = []
    for line in line_list:
        # If the list is empty, start a new letter:
        if temp_sorted == []:
            temp_sorted.append([line])
        else:
            index = 0 # used if a line connects two letters
            index_list = []
            for letter in temp_sorted:
                connected = False
                # Check if same colour, and
                # check if connected
                # lists are sorted by Y value
                max_y_val = max_y(letter)                
                # Check colour first:
                if close_rgb(line.colour, letter[0].colour):
                    # Same colour, check if connected:
                    for line2 in letter:
                        if check_connection(line, line2):
                            connected = True
                            if index not in index_list:
                                index_list.append(index)
                if connected == False and max_y_val < (line.starty - 1):
                    # no connection and max_y is too far to connect?
                    # add this letter to letter_sorted, no need
                    # to search through it anymore (remove from
                    # temp_sorted)
                    pass                    #TO DO: FIX OR REMOVE THIS
                    #if len(letter) > 1:
                        ##print("adding letta to sorted....")
                        #letter_sorted.append(letter)
                        #del temp_sorted[index]
                        #index -= 1
                index += 1
                for ind in index_list:
                    #TO DO: FIX OR REMOVE THIS
                    pass
            if index_list == []:
                # didn't connect to any letter, it's a new letter now
                temp_sorted.append([line])
            elif len(index_list) > 1:
                temp_letter = []
                index_list.reverse()
                for connection in index_list:             
                    if temp_letter == []:
                        for line3 in temp_sorted[connection]:
                            temp_letter.append(line3)
                    else:
                        temp_letter.extend(temp_sorted[connection])
                    del temp_sorted[connection]
                temp_letter.append(line)
                temp_sorted.append(temp_letter)
                
            else:
                
                # line is connected to exactly one letter
                if temp_sorted != []:
                    temp_sorted[index_list[0]].append(line)
    print("Okay, here we go...")
    print("It's letter morphin' time!")
    temp_sorted = letter_filter(temp_sorted)
    real_letterz = []
    for letter in temp_sorted:
        
        new_letter = Word("", (0,0),(0,0))
        xvals = 0
        yvals = 0
        xvals_2 = 0
        yvals_2 = 0
        index = 0
        for line in letter:
            xvals += line.startxy[0]
            yvals += line.startxy[1]
            xvals_2 += line.endxy[0]
            yvals_2 += line.endxy[1]
            index += 1
        xvals = xvals // index
        yvals = yvals // index
        xvals_2 = xvals_2 // index
        yvals_2 = yvals_2 // index
        lcoords = (xvals, yvals)
        rcoords = (xvals_2, yvals_2)
        if a_check(letter):
            new_letter = Word("a", lcoords, rcoords)
        elif e_check(letter):
            new_letter = Word("e", lcoords, rcoords)
        elif f_check(letter):
            new_letter = Word("f", lcoords, rcoords)
        elif h_check(letter):
            new_letter = Word("h", lcoords, rcoords)
        elif i_check(letter):
            new_letter = Word("i", lcoords, rcoords)
        elif k_check(letter):
            new_letter = Word("k", lcoords, rcoords)
        elif l_check(letter):
            new_letter = Word("l", lcoords, rcoords)
        elif m_check(letter):
            new_letter = Word("m", lcoords, rcoords)
        elif n_check(letter):
            new_letter = Word("n", lcoords, rcoords)
        elif t_check(letter):
            new_letter = Word("t", lcoords, rcoords)
        elif v_check(letter):
            new_letter = Word("v", lcoords, rcoords)
        elif x_check(letter):
            new_letter = Word("x", lcoords, rcoords)
        elif y_check(letter):
            new_letter = Word("y", lcoords, rcoords)
        elif z_check(letter):
            new_letter = Word("z", lcoords, rcoords)
        else:
            new_letter = Word("x", lcoords, rcoords)

        if new_letter.name != "":
            real_letterz.append(new_letter)
        for letter in real_letterz:
            print(letter.name, letter.lcoords, letter.rcoords)
    #return temp_sorted OLD SCOOL
    return real_letterz # NEW SCOOLa


def wordCatcher():
    completed_words = []
    current_words = []
    #TODO: allow for flexibility based on screen size
    #TODO: for now assuming 800x600
    for x in range(5):
        x1 = x*40 + 1
        line_list = lineCatcher(x1, 350, x1+40, 450)
        letters = potential_letter_sort(line_list)
        #**************************
        # NEED letters to return string e.g. "e", "h", "*" (wildcard), etc.

        # I.E. need letter CLASS? NO, LETTER = WORD
        if current_words != []:
                
            for word in current_words:
                not_connected = True
                for letter in letters:
                    # Checking if part of the word
                    if neighbours(word, letter):
                        # Add it to the word
                        word.name += letter.name
                        word.rcoords = letter.rcoords
                        # Doesn't need to be part of another word
                        letters.remove(letter)
                        not_connected = False
                if not_connected == True:
                    # This word never connected - it is finished
                    # As we move left ot right, it can never be larger
                    # than it already is.
                    completed_words.append(word)
                    current_words.remove(word)
                    
        else:
            current_words = letters
    # Need to add all current_words to completed words:
    completed_words.extend(current_words)
    for words in completed_words:
        print(word.name)


def neighbours(some_word, some_letter):
    if ((abs(some_word.lcoords[1] - some_letter.lcoords[1]) < 5) and
    (abs(some_word.rcoords[0] - some_letter.rcoords[0] < 7))):
        return True
    else:
        return False

                                           
def a_check(some_letter):
    arms = arm_counter(some_letter)
    legs = leg_counter(some_letter)
    trunks = trunk_counter(some_letter)

    if arms == 1 and (legs == 2 and trunks == 0):
        return True
    elif arms == 1 and (legs == 0 and trunks == 2):
        return True
    else:
        return False

def e_check(some_letter):
    arms = arm_counter(some_letter)
    legs = leg_counter(some_letter)
    trunks = trunk_counter(some_letter)
    letter_list = []
    #print("ARMS: " + str(arms) + " YEGS: " + str(legs) + " TRUNKS: " + str(trunks))
    if arms == 3 and trunks == 1 and leg_counter(some_letter) == 0:
        #print("E found: ")
        for line in some_letter:
            #print(str(line.startxy)+','+str(line.endxy))
            #canvass.create_line(line.startx, line.starty, line.endx, line.endy, fill="purple")
            pass
        return True
        
    #else:
        #print("not an E, sorry")


def f_check(some_letter):

    arms = arm_counter(some_letter)
    legs = leg_counter(some_letter)
    trunks = trunk_counter(some_letter)

    if arms == 2 and (trunks == 1 and legs == 0):
        return True
    else:
        return False


def h_check(some_letter):
    arms = arm_counter(some_letter)
    legs = leg_counter(some_letter)
    trunks = trunk_counter(some_letter)

    if arms == 1 and (trunks == 2 and legs == 0):
        return True
    else:
        return False


    
def i_check(some_letter):
    arms = arm_counter(some_letter)
    legs = leg_counter(some_letter)
    trunks = trunk_counter(some_letter)

    if arms == 2 and (trunks == 1 and legs == 0):
        return True
    elif arms == 0 and (trunks == 1 and legs == 0):
        return True
    else:
        return False


def k_check(some_letter):
    arms = arm_counter(some_letter)
    legs = leg_counter(some_letter)
    trunks = trunk_counter(some_letter)

    if arms == 0 and (trunks == 1 and legs == 2):
        return True
    else:
        return False

    
def l_check(some_letter):
    arms = arm_counter(some_letter)
    legs = leg_counter(some_letter)
    trunks = trunk_counter(some_letter)
    if arms == 1 and trunks == 1 and legs == 0:
        return True
        #for line in some_letter:
         #   canvass.create_line(line.startx, line.starty, line.endx, line.endy, fill="green")


def m_check(some_letter):
    arms = arm_counter(some_letter)
    legs = leg_counter(some_letter)
    trunks = trunk_counter(some_letter)
    if arms == 0 and trunks == 2 and legs == 2:
        return True
        #for line in some_letter:
         #   canvass.create_line(line.startx, line.starty, line.endx, line.endy, fill="red")
    if arms == 1 and trunks == 3 and legs == 0:
        return True
        #for line in some_letter:
         #   canvass.create_line(line.startx, line.starty, line.endx, line.endy, fill="red")


def n_check(some_letter):
    arms = arm_counter(some_letter)
    legs = leg_counter(some_letter)
    trunks = trunk_counter(some_letter)

    if arms == 1 and (trunks == 2 and legs == 1):
        return True
    else:
        return False    


def t_check(some_letter):
    arms = arm_counter(some_letter)
    legs = leg_counter(some_letter)
    trunks = trunk_counter(some_letter)

    if arms == 1 and (trunks == 1 and legs == 0):
        return True
    else:
        return False


def v_check(some_letter):
    arms = arm_counter(some_letter)
    legs = leg_counter(some_letter)
    trunks = trunk_counter(some_letter)

    if arms == 0 and (trunks == 0 and legs == 2):
        return True
    else:
        return False

    
def x_check(some_letter):
    arms = arm_counter(some_letter)
    legs = leg_counter(some_letter)
    trunks = trunk_counter(some_letter)

    if arms == 0 and (trunks == 0 and legs == 2):
        return True
    else:
        return False


def y_check(some_letter):
    arms = arm_counter(some_letter)
    legs = leg_counter(some_letter)
    trunks = trunk_counter(some_letter)

    if arms == 0 and (trunks == 1 and legs == 2):
        return True
    else:
        return False    


def z_check(some_letter):
    arms = arm_counter(some_letter)
    legs = leg_counter(some_letter)
    trunks = trunk_counter(some_letter)

    if arms == 2 and (trunks == 0 and legs == 1):
        return True
    else:
        return False





    
        
def rgb_to_hex(r, g, b):
    r2 = r % 16
    g2 = g % 16
    b2 = b % 16
    r1 = r // 16
    g1 = g // 16
    b1 = b // 16
    rgblist = [r1, r2, g1, g2, b1, b2]
    new_hex = ""
    for num in rgblist:
        if num > 9:
            num = chr(55 + num)
        new_hex += str(num)
    return '#' + new_hex

'''
black = Pixel(0,0,0)
white = Pixel(255,255,255)
liners = [Line((11,11),(15,11), black),
          Line((11,12),(11,12), black),
          Line((12,12),(13,12), white),
          Line((12,12),(14,12), white),
          Line((15,12),(15,12), black),
          Line((11,13),(11,13), black),
          Line((12,13),(15,13), white),
          Line((11,14),(11,14), black),
          Line((12,14),(12,14), white),
          Line((13,14),(13,14), black),
          Line((14,14),(15,14), white),
          Line((11,15),(13,15), black),
          Line((14,15),(15,15), white),
          Line((11,16),(11,16), black),
          Line((12,16),(12,16), white),
          Line((13,16),(13,16), black),
          Line((14,16),(15,16), white),
          Line((11,17),(11,17), black),
          Line((12,17),(15,17), white),
          Line((11,18),(15,18), black)]
'''
#sorted_letters = potential_letter_sort(liners)

#liney_list = lineCatcher(300,100,500,600) #second rectangle
#liney_list = lineCatcher(100,100,220,220)
#liney_list = lineCatcher(300,300,350,400) #NOTEPAD
#liney_list = lineCatcher(500,30,750,100) #map name
#liney_list = lineCatcher(412,435,426,450) #T
#liney_list = lineCatcher(385,325,395,340) #E
#liney_list = lineCatcher(375,435,390,450) #M
#liney_list = lineCatcher(375,435,450,450) #MULTIPL


'''
liney_list = [Line((1,1),(1,1),Pixel(255,255,0)),
              Line((2,1),(2,1),Pixel(255,127,0)),
              Line((3,1),(3,1),Pixel(255,255,0)),
              Line((4,1),(6,1),Pixel(0,255,255)),
              Line((1,2),(3,2),Pixel(0,255,0)),
              Line((4,2),(4,2),Pixel(0,255,255)),
              Line((5,2),(5,2),Pixel(255,127,0)),
              Line((6,2),(6,2),Pixel(0,255,255)),
              Line((1,3),(1,3),Pixel(0,0,255)),
              Line((2,3),(2,3),Pixel(0,255,0)),
              Line((3,3),(3,3),Pixel(0,0,255)),
              Line((4,3),(4,3),Pixel(255,255,0)),
              Line((5,3),(5,3),Pixel(0,255,255)),
              Line((6,3),(6,3),Pixel(255,255,0)),
              Line((1,4),(1,4),Pixel(0,0,255)),
              Line((2,4),(2,4),Pixel(0,255,0)),
              Line((3,4),(6,4),Pixel(0,0,255))]
'''
#print("liney list total: " + str(len(liney_list)))
#sorted_letters = potential_letter_sort(liney_list)
#print("sorted letter total: " + str(len(sorted_letters)))


wordCatcher()


def canvas_me(some_list, instruct):

    root = tk.Tk()
    canvass = tk.Canvas(root, width=800, height=800, bg="white")
    canvass.pack()

    if instruct == "linecatcher":
        for lines in liney_list:
            colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
   
            canvass.create_line(lines.startx, lines.starty,
                                lines.endx+1, lines.endy, fill=colourpoo)
    elif instruct == "sortedlist":
        for letters in some_list:
            for lines in letters:
                colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
                canvass.create_line(lines.startx, lines.starty, lines.endx+1, lines.endy, fill=colourpoo)
        
    elif instruct == "letterfindall":
        for letters in some_list:
            if m_check(letters):
                for lines in letters:
                    colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
                    canvass.create_line(lines.startx, lines.starty, lines.endx+1, lines.endy, fill="aquamarine")
            if e_check(letters):
                for lines in letters:
                    colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
                    canvass.create_line(lines.startx, lines.starty, lines.endx+1, lines.endy, fill="green")
            if f_check(letters):
                for lines in letters:
                    colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
                    canvass.create_line(lines.startx, lines.starty, lines.endx+1, lines.endy, fill="black")                    
            if h_check(letters):
                for lines in letters:
                    colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
                    canvass.create_line(lines.startx, lines.starty, lines.endx+1, lines.endy, fill="black")
            if i_check(letters):
                for lines in letters:
                    colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
                    canvass.create_line(lines.startx, lines.starty, lines.endx+1, lines.endy, fill="indigo")                    
            if l_check(letters):
                for lines in letters:
                    colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
                    canvass.create_line(lines.startx, lines.starty, lines.endx+1, lines.endy, fill="light blue")
            if t_check(letters):
                for lines in letters:
                    colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
                    canvass.create_line(lines.startx, lines.starty, lines.endx+1, lines.endy, fill="red")
    else:
        print("NO vAlId OPTION CHOSEN")
    root.mainloop()

'''
m = aquamarine
e = green
f = black
h = black
i = indigo
l = light blue
t = red





canvas_me(liney_list, "linecatcher")
canvas_me(sorted_letters, "sortedlist")
for letter in sorted_letters:
    if len(letter) == 0:
        print("WASH ME, WA-ASH ME-EY WA-ASH ME-EY.......")
canvas_me(sorted_letters, "letterfindall")

for lines in liney_list:
    colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
        
    #print(str(lines.startx)+","+str(lines.starty)+","+
          #str(lines.endx)+","+str(lines.endy) + "," + colourpoo)


for letters in sorted_letters:
    #print("LETTER")
    for lines in letters:
        colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
        
        #print(str(lines.startx)+","+str(lines.starty)+","+
             #str(lines.endx)+","+str(lines.endy) + "," + colourpoo)
    #print(e_check(letters))
    #print("END OF LETTER ******************")


for letters in sorted_letters:
    root = tk.Tk()
    canvass = tk.Canvas(root, width=800, height=600, bg="white")
    canvass.pack()
    
    for lines in letters:
        canvass.create_line(lines.startx, lines.starty, lines.endx+1, lines.endy, fill="black")
    root.mainloop()


#def draw_me(filename) maybe if I'm crazyyyyyyyyyyyy

   
#for lines in liners:
 #   colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
    #canvass.create_line(lines.startx, lines.starty, lines.endx, lines.endy, fill=colourpoo)
for letters in sorted_letters:
    
    #print("LETTER:")
    
    for lines in letters:
        colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
        
        #print(str(lines.startx)+","+str(lines.starty)+","+
              str(lines.endx)+","+str(lines.endy) + "," + colourpoo)
        
        #canvass.create_line(lines.startx, lines.starty, lines.endx, lines.endy, fill=colourpoo)
    e_check(letters)
    l_check(letters)
    m_check(letters)
    #print("END LETER******************************************************")


root.mainloop()

root = tk.Tk()
canvass = tk.Canvas(root, width=800, height=800, bg="white")
canvass.pack()


for lines in liney_list:
    
    colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
   
    #canvass.create_line(lines.startx, lines.starty,
                        #lines.endx, lines.endy, fill=colourpoo)

#for lines in liners:
 #   colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
    #canvass.create_line(lines.startx, lines.starty, lines.endx, lines.endy, fill=colourpoo)
for letters in sorted_letters:
    
    #print("LETTER:")
    
    for lines in letters:
        colourpoo = rgb_to_hex(lines.colour.r, lines.colour.g, lines.colour.b)
        
        #print(str(lines.startx)+","+str(lines.starty)+","+
              str(lines.endx)+","+str(lines.endy) + "," + colourpoo)
        
        #canvass.create_line(lines.startx, lines.starty, lines.endx, lines.endy, fill=colourpoo)
    e_check(letters)
    l_check(letters)
    m_check(letters)
    #print("END LETER******************************************************")


root.mainloop()
'''
