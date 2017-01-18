'''
ultimo_burrito.py
created: Jan 2017
created by: Rory F
Part of the AMMA-2050 code bank
All issues/queries, please send to Andy H :-)

Ultimo_burrito is the master general user interface
for calculating CMIP5 metrics as part of the AMMA-2050 project.
It provides an interface (GUI) that allows users to pick 
which metric calculation files they wish to run and for what time
period.

Results will then be saved into a specific area chosen by the user.
Note below give an overview of how the GUI has been constructed 
and provide insight if readers wish to create a similar interface.

The code is set up in five main sections - 
- Import python modules
- set global variables to be modified by the GUI
- create dictionaries that contain all possible GUI variables
- A set of modules that tie to the GUI interface
- What is seen on the GUI

More descriptive explanations are given within each section
in hashed out boxes

Also, see help files in the menu once ultimo_burrito is running.

To run,
from command line type - "python ultimo_burrito.py"
from canopy/kate, run as you would normally run a script (e.g. hit the play button in Canopy)

Update - work to do from 7th January
- Pretty picture in the background? Maybe the AMMA-2050 logo?
- custom titles, axes titles on the plot? These need to be put in the calc_files
- Finish the plot files
- Finish the help texts
'''

##############################################################################
# The main module used to create the GUI is Tkinter
# this is a standard python package that should be installed
# when you install python2.7
# As the GUI is currently a working file, there are some modules loaded that
# are redundant. These will be cleaned up once the final code is made
##############################################################################
from Tkinter import *
# import Tkinter.messagebox
from tkFileDialog import askdirectory  # this module asks users to select a given directory on their system
from tkFileDialog import askopenfile  # this module asks for a given file from the user NOT CURRENTLY USED
import tkSimpleDialog
import tkMessageBox
import glob  # Used to find all calculation metric files
import Tkinter as tk
import shutil

############################################################################
# Ultimo_burrito will pass a list of variables in to the file master.py
# once we hit run.
#
# Here we set up all the variables that will be passed through later.
#
# Note that some of these are strings and some are numbers.
# This code has been set up with that in mind
############################################################################
variable = '***'  # e.g. precipitation
period = []  # this is the scenario e.g. historical
bc = []  # this is the bias_correction and resolution choice
outpath = '***'  # where do I want to save data

# The inpath needs sending through to load_file_names
inpath = '***'
file_name = '***'  # this is the calc file used
xmin = 0  # left most longitude
xmax = 0  # right most longitude
ymin = 0  # lowest latitude
ymax = 0  # highest latitude
area_name = '***'  # what to call the region (e.g. West_Africa, Burkina_Faso)
plotter = '***'  # this will send through the type of plot wanted
season = []  # this will be the timeslice used in the metric calculation file
overwrite = 'No'
#############################################################################
#
# Now we wish to provide choices for the user to select from.
# This is the main advantage of the GUI as any new ideas we have can be updated
# centrally.
#
# With the excetion of the calc_ files, the variable choices are stored
# in dictionaries as this allows the best method to contain and update
# various choices
#
# Dictionaries are set up with the following key names.
# Say we have a dictionary that looks like
#
# dictionary = {1:'I love Leeds',
#               2: 'Yes I do'}
#
# The numbers "1" and "2" are called the dictionary keys.
# These are what will appear in the list box.
#
# The phrases "I love Leeds" and "Yes I do" are called the dictionary values.
# When I call "1" from the dictionary, this will return me the value "I love Leeds"
##############################################################################

# list of calc files is special
# What this does, is find any files beginning with the phrase "calc" in the 
# same directory as ultimo_burrito, and return this as the list of possible
# metric calculations.
# Therefore, every time a new metric file is made, the list will automatically
# update on the user's local drive

list_of_calc_files = glob.glob('calc*.py')
#print list_of_calc_files[:]

# Season dictionary is a slightly redundant dictionary
# This is because the time slicing is done in each calc_ file.
# However, here, we determine the season to pass through to the calc_
# files

season_dictionary = {'ann': 'ann',
                     'mj': 'mj',
                     'jj': 'jj',
                     'ja': 'ja',
                     'as': 'as',
                     'so': 'so',
                     'jan': 'jan',
                     'feb': 'feb',
                     'mar': 'mar',
                     'apr': 'apr',
                     'may': 'may',
                     'jun': 'jun',
                     'jul': 'jul',
                     'aug': 'aug',
                     'sep': 'sep',
                     'oct': 'oct',
                     'nov': 'nov',
                     'dec': 'dec',
                     'djf': 'djf',
                     'mam': 'mam',
                     'jja': 'jja',
                     'jas': 'jas',
                     'jjas': 'jjas',
                     'mjjas': 'mjjas',
                     'son': 'son'
                     }

# This dictionary contains lists as its dictionary values.
# This is for efficiency as we want the selection
# of a given region to return all four latitude and
# longitude values. Dictionaries can contain lists and handle these 
# just fine

boundary_dictionary = {'West_Africa': [-10., 10., 5., 25.],
                       'Senegal': [-20., -13., 12.5, 17.5],
                       'Burkina_Faso': [-14., -9., 8., 12.],
                       'Sahel': [-10., 10., 8., 12.],
                       'Guinea_Coast': [-10., 10., 4., 6.]
                       }

# plot_dictionary is where we use another trick
# The string in each entry value (plot_line, scatter etc.)
# is actually going to refer later to a python code
# Normally, when we import python codes, we do not treat their
# names as strings (e.g. you never write import "iris")
# However, by trating the name of a code as a string, you can vary which
# code is imported and called each time you run ultimo_burrito.
# (We do a similar thing with the metric calculation files).
#
# To see how this works, look at the annotations in master.py

list_of_plot_files = glob.glob('plot*.py')
#print list_of_plot_files[:]

bcs_dictionary = {'0.5 deg': '0.5x0.5',
                  'Bias corrected 0.5 deg': 'BC_0.5x0.5',
                  'Bias corrected model resolution': 'BC_mdlgrid',
                  'Model resolution': 'mdlgrid',
                  'WA subset 0.5deg': 'WA_0.5x0.5'
                  }

variables_dictionary = {'precipitation': 'pr',
                        'minimum daily temp': 'tasmin',
                        'average daily temperature': 'tas',
                        'rsds': 'rsds',
                        'maximum daily temperature': 'tasmax',
                        'surface wind speed': 'wind'
                        }

period_dictionary = {'historical': 'historical',
                     'rcp2.6': 'rcp26',
                     'rcp4.5': 'rcp45',
                     'rcp8.5': 'rcp85'
                     }

overwrite_dictionary = {'Overwrite files': 'Yes',
                        'Do not overwrite': 'No'
                        }


######################################################################################
#
# In the following section, we start to define the functions that will run when
# a user interacts with the GUI.
#
# This is (if you like), the back end of the code.
#
#######################################################################################


# runmaster is the function that runs the master script once all global varaibles have been chosen.
def runmaster(variable, scenario, bc_and_resolution, inpath, outpath, season, region, calc_file, xmin, xmax, ymin, ymax,
              plotter, overwrite):
    import master
    print 'you have selected calc file: ' + str(file_name)
    print 'you have selected inpath: ' + str(inpath)
    print 'you have selected outpath: ' + str(outpath)
    print 'you have selected scenario: ' + str(period)
    print 'you have selected varaible: ' + str(variable)
    print 'you have selected resolution: ' + str(bc)
    print 'you have selected plot type: ' + str(plotter)
    print 'you have selected season: ' + str(season)
    print 'you have selected region: ' + str(area_name)
    print 'you have selected x boundaries: ' + str(xmin), str(xmax)
    print 'you have selected y boundaries: ' + str(ymin), str(ymax)
    #   print 'Please type Y to continue'
    continu = raw_input('Please type Y to continue ---->')
    if continu == 'Y' or continu == 'y':
        master.master(variable, scenario, bc_and_resolution, inpath, outpath, season, region, calc_file, xmin, xmax,
                      ymin, ymax, plotter, overwrite)
        print 'You have finished the burrito'
        #     season = []
        #     bc = []
        #     period = []
    else:
        print "Burrito not running, please hit 'Run code' to try again."


# RUN_THE_BURRITO is a work in progress. I have attached some notes for myself but it does not work prfectly right now
# It will also take a LONG time to run so do not hit go unless you really want to run it.
def RUN_THE_BURRITO():
    # So this is the big one
    # This button will run all codes for all time slices and all boundary conditions for the West Africa
    # Region
    # This is the whole enchaliada
    # Let's have some fun

    # First preset all the things that will not change
    import master
    global area_name
    global xmin
    global xmax
    global ymin
    global ymax
    global boundary_dictionary
    area_name = 'West_Africa'
    xmin = boundary_dictionary[area_name][0]
    xmax = boundary_dictionary[area_name][1]
    ymin = boundary_dictionary[area_name][2]
    ymax = boundary_dictionary[area_name][3]
    global outpath
    outpath = askdirectory()

    # now pull in all scenarios and all BC
    global period_dictionary
    global period
    period = period_dictionary.values()

    global bcs_dictionary
    global bc
    bc = bcs_dictionary.values()

    # Ok here is the sweet bit
    global list_of_calc_files
    global file_name
    for item in list_of_calc_files:
        print item

        string = item.split('calc_')[-1]
        item = string.split(".")[0]
        calc_file = 'calc_' + str(item)
        findvar = __import__(calc_file)
        global variable
        global season
        global plotter

        temp = findvar.variable_setter('plot_type')
        if temp != "plot type":
            plotter = temp
        temp = findvar.variable_setter('seas')
        if temp != "seas":
            season = temp
        temp = findvar.variable_setter('var')
        if temp != "var":
            variable = temp
        print "Plot type preset to: '%s'" % plotter
        print "Season preset to: '%s'" % season
        print "Variable preset to: '%s'" % variable
        for p in period:
            for b in bc:
                print variable, p, b, outpath, season, area_name, item, xmin, xmax, ymin, ymax, plotter
                master.master(variable, p, b, outpath, season, area_name, item, xmin, xmax, ymin, ymax, plotter)


# The set of functions called "OnDouble___(event)
# are each set to a different listbox in the GUI
# I will explain briefly what each one does in the modules
# Each module is only triggered on a given event.
# In ultimo_burrito, this event is alway double clicking a certain option (this is set in the list boxes)
# In order to reset a variable in the who ultimo_burrito file, we need to call in the global variable
# This is what happens on any line that starts with "global". See the first section of this code to 
# see where we first created the dummy variables to pass into master.py
#
# Here to save my sanity, I have fully explained the first three OnDouble... events and the last
# one as these use four different techniques, the others are all variations on a theme


def popupWindow():
    global area_name
    global xmin
    global xmax
    global ymin
    global ymax
    area_name = tkSimpleDialog.askstring("area name", "Insert a name for your area(no spaces)")
    xmin = tkSimpleDialog.askfloat("xmin", "Insert the west most longitude")
    xmax = tkSimpleDialog.askfloat("xmax", "Insert the east most longitude")
    ymin = tkSimpleDialog.askfloat("ymin", "Insert the south most latitude")
    ymax = tkSimpleDialog.askfloat("ymax", "Insert the north most latitude")
    print area_name, xmin, xmax, ymin, ymax


def OnDoubleBoundary(event):  # this module will set the region we use going forward
    global boundary_dictionary  # pull in the boundary dictionary for future reference
    global xmin  # we will want to edit this variable in the whole script, so call the global variable xmin
    global xmax  # as for above
    global ymin
    global ymax
    global area_name
    # we want to add the option of custom boundaries



    # The next three lines are the bit of magic that presets the code to pull in the right part of boundary_dictionary
    # Bit of terminology here. The listboxes that appear on the GUI are known as "widgets".
    # The event of selecting a certain thing from the listbox is known as the "curselection"
    # so, what the three lines below translate as in simple English is:
    # - in the listbox on the GUI, wait for a certain event (double clicking some selection) to occur
    # - when that event occurs, tell me what was selected
    # - get this selections value (i.e. the dictionary key)
    widget = event.widget
    selection = widget.curselection()[0]
    key = widget.get(selection)

    # now, we have the dictionary key, we can use this to grab the relevant values
    # from the dictionary for our global variables
    # Remember, boundary_dictionary had a list as it's values
    # these were always set in the order [xmin,xmax,ymin,ymax]
    # So we don't need to mess around any more, just pull the list item for each one
    # In simple text, what each of the four below lines do is say
    # xmin(or xmax etc.) = the 0th element in the boundary_dictionary on whatever row had the dictionary key of "key"
    if key != 'Custom':
        xmin = boundary_dictionary[key][0]
        xmax = boundary_dictionary[key][1]
        ymin = boundary_dictionary[key][2]
        ymax = boundary_dictionary[key][3]
        # We can cheat here. We set the boundary keys as the options in the listbox
        # Well, these are the relevant options for area_name.
        # So all we need to do is set area_name to "key"
        area_name = key

    print "selection:", selection, ": '%s'" % xmin


# So OnDoubleCalc will load the metric calculation file we plan to use
# and then also preset a couple of other variables.
# This is why all metric calculation files need to be set up in a specific way
# (see help menu for the file explaining the calc file set up standard parctice)
# (or reference calc_Regional_Onset_with_notes.py)

def OnDoubleCalc(event):
    global list_of_calc_files  # for this code, the dictionary was actually a list of files (see how we made list_of_calc_files earlier in the script
    global file_name  # we will want to edit this variable in the whole script, so call the global variable file_name
    widget = event.widget  # same as before
    selection = widget.curselection()[0]
    key = widget.get(selection)
    file_name = key
    print "selection:", selection, ": '%s'" % key
    # There is a slight fudge here
    # in more detail, what happened when we created the list box was
    # we stripped the word "calc_" and ".py" from all the metric calculation files
    # in order to make the GUI look prettier.
    # So, if we wanted to open file calc_Regional_Onset_with_notes.py,
    # we would select from the list box, the value "Regional_Onset_with_notes.
    # BUT...
    # There is no file called "Regional_Onset_with_notes, it is called calc_Regional_Onset_with_notes
    # So, to open it, we need to put the word calc_ back on the front

    # So we add the calc_ back on
    calc_file = 'calc_' + str(file_name)
    print calc_file  # and print to make sure it is all good to go
    # Here is the trick we talked about earlier
    # normally, import does not like strings
    # but __import__ loves them.
    # So we can change what we call in every time we run the burrito
    # by setting it is a string and using __import__
    # we can also assign this as a variable.
    #
    # If you ever want to test this, try this in python
    # nump = __import__("numpy")
    # lst = [1,2,3,4,5]
    # print(nump.average(lst))
    #
    # 3? Sweet.
    findvar = __import__(calc_file)
    # print dir(findvar) will show you what modules are in your metric calc file
    # this is for an easy debug. If the output here does not show something called
    # variable_setter, then look again at the help file on setting up a calc_ file.
    print findvar.main.__doc__

    global variable  # we can now edit the global variable, season and plotter...
    global season
    global plotter
    temp = findvar.variable_setter('plot_type')
    if temp != "plot type":
        plotter = temp
    temp = findvar.variable_setter('seas')
    if temp != "seas":
        season.extend([temp])
    temp = findvar.variable_setter('var')
    if temp != "var":
        variable = temp
    print "Plot type preset to: '%s'" % plotter  # print to screen to double check it worked right. Errors will come up with '****' as your plot type, season or variable
    print "Season preset to: '%s'" % season
    print "Variable preset to: '%s'" % variable


# The season finding dictionary is much more straghtforward
# all we do is open the dictionary, and return whatever corresponds to our event click (key) in the dictionary.
# and set season to the corresponding value
def OnDoubleSeason(event):
    global season_dictionary
    global season  # we will want to edit this variable in the whole script, so call the global variable season
    widget = event.widget
    selection = widget.curselection()[0]
    key = widget.get(selection)
    season.extend([season_dictionary[key]])
    #        season = season_dictionary[key]
    print "selection:", selection, ": '%s'" % season


def OnDoubleVariable(event):
    global variables_dictionary
    global variable
    widget = event.widget
    selection = widget.curselection()[0]
    key = widget.get(selection)
    variable = variables_dictionary[key]
    print "selection:", selection, ": '%s'" % variable


def OnDoublePeriod(event):
    global period_dictionary
    global period
    widget = event.widget
    selection = widget.curselection()[0]
    key = widget.get(selection)
    period.extend([period_dictionary[key]])
    #        period = period_dictionary[key]
    print "selection:", selection, ": '%s'" % period


# Little note here. Although we set plot type in the file opening event. Maybe you want to change the
# recommended plot type (or the metric file did not actually set a suitable plot type.
# You can overwrite the option given in the OnDoubleCalc here
def OnDoublePlot(event):
    global list_of_plot_files  # for this code, the dictionary was actually a list of files (see how we made list_of_calc_files earlier in the script
    global plotter  # we will want to edit this variable in the whole script, so call the global variable file_name
    widget = event.widget  # same as before
    selection = widget.curselection()[0]
    key = widget.get(selection)
    plotter = key
    print "selection:", selection, ": '%s'" % plotter
    plotter = 'plot_' + str(plotter)
    print ('Plot type:', plotter)  # and print to make sure it is all good to go

def OnDoubleBC(event):
    global bcs_dictionary
    global bc
    widget = event.widget
    selection = widget.curselection()[0]
    value = widget.get(selection)
    bc.extend([bcs_dictionary[value]])
    #        bc = bcs_dictionary[value]
    print "selection:", selection, ": '%s'" % bc


# So outpath, and inpath, will be set by the user choosing their own directory (to remove the risk of silly syntax errors).
# In tkinter, this is just one line. We just say, outpath = askdirectory(), then a box will open up that asks the user to choose
# a directory. Once they hit ok on the box, bam! Outbox is set.
def findoutpath():
    global outpath  # we will want to edit this variable in the whole script, so call the global variable outpath
    import filepaths
    outer = filepaths.main('outp')
    if outer != 'outp':
        outpath = outer
    else:
        outpath = askdirectory()
    print "outpath set to " + outpath


def findinpath():
    global inpath
    import filepaths
    inner = filepaths.main('inp')
    if inner != 'inp':
        inpath = inner
    else:
        inpath = askdirectory()
    print "inpath set to " + inpath


def load_gen_help():
    filelist = glob.glob('general_help.txt')
    print filelist
    file_read = open(filelist[0], 'r')
    #    print file_read
    print file_read.read()


def load_var_choices():
    filelist = glob.glob('variable_choices.txt')
    print filelist
    file_read = open(filelist[0], 'r')
    #    print file_read
    print file_read.read()


def load_calc_maker():
    filelist = glob.glob('set_up_calc_file.txt')
    print filelist
    file_read = open(filelist[0], 'r')
    #    print file_read
    print file_read.read()


def OnDoubleOverwrite(event):
    global overwrite_dictionary
    global overwrite
    widget = event.widget
    selection = widget.curselection()[0]
    key = widget.get(selection)
    overwrite = overwrite_dictionary[key]
    print "selection:", selection, ": '%s'" % overwrite


def copytemplate():
    newfilename = tkSimpleDialog.askstring("new file name", "Insert a new file name (format 'calc_something.py')")
    shutil.copy('template.py', newfilename)
    print newfilename + ' is ready to edit. Have fun!'


def clearlists():
    global season
    global bc
    global period
    season = []
    bc = []
    period = []
    print "season, bc, and period reset"


############################################################################################
#
#
# OK so the final part of the code is setting up the actual GUI window.
# This is all the user will see, so make it pretty otherwise they will not
# use it.
#
# Note, this is not yet fully pretty. If this was monopoly, we wouldn't even
# win second prize in the beauty contest. But hey, learn to love the one you are with...
#
# Will explain the code in sections so you can see how to build your own GUI if you
# ever feel like your job is not stressful enough
############################################################################################
#
# We use a new type of python data thing here. Namely classes. Not too sure what they
# do so will not write too much here to explain it (because I will be wrong).
# Just trust that from my reading into GUIs this seems to be the best way to make this work
############################################################################################
#
# We can also use classes to make pop up windows. This will appear in the runmaster module
# once ultimo_burrito is made more ultimo (ULTIMO_burrito? burritus_maximus? suggestions welcome)
############################################################################################



class mainWindow(
    object):  # everything in here will appear in the main window of the GUI (what appears when you hit run)
    def __init__(self, master):
        self.master = master  # whenever I mention self.master from now on, this is the master window

        #########################
        #
        # Let's make a help menu
        #
        #########################

        menu = Menu(root)
        root.config(menu=menu)
        helpMenu = Menu(menu)
        menu.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="General Help", command=load_gen_help)
        helpMenu.add_command(label="Selecting variables", command=load_var_choices)
        helpMenu.add_command(label="Setting up metric calc files", command=load_calc_maker)

        createMenu = Menu(menu)
        menu.add_cascade(label='Create new file', menu=createMenu)
        createMenu.add_command(label='create template file', command=copytemplate)

        buttons = Frame(root)
        lists = Frame(root)
        labels = Frame(root)
        buttons.pack(side='top', fill='x')
        labels.pack(side='top', fill='both')
        lists.pack(side='bottom', fill='both', expand=True)

        # In the main GUI window, there are three types of widget used. Buttons, Listboxes and Menus
        # I have grouped these so you can see what does what

        ###################################################################################################################################################################
        # BUTTONS #
        ###########

        # Buttons are made with at least three instructions:
        # - where do you want the button (typically root, or the root GUI window), think this is the same as master but not 100% (I am still learning)
        # - What do you want to button to say (text)?
        # - What do you want the button to do (command)?

        # Commands can be set up in two ways. Either simple commands (e.g. outpathbutton) where we just say on click, run a module
        # or complex (lambda) commands. Where we pass variables to the module we click on (see runmaster)
        # Where possible, use simple commands, but do not be afraid of lambda commands. They are fiddly but as long as you set up the dummy global
        # variables at the start of the code (first part of the code), the worst that happens is the master code fails and tells you why (i.e. you did not set one of the variables)

        # When you set a widget, you need to pack it. This places it on the GUI window (root) somewhere. You can set this as a grid, or (as it is now)
        # just throw things on the left or right of the screen and ask Tkinter to sort it out.

        runbutton = Button(buttons, text='Run code',
                           command=lambda: runmaster(variable, period, bc, inpath, outpath, season, area_name,
                                                     file_name, xmin, xmax, ymin, ymax, plotter, overwrite))
        runbutton.pack(side="left")

        BURRITObutton = Button(buttons, text='Clear choices', command=clearlists)
        BURRITObutton.pack(side="left")

        #        BURRITObutton = Button(buttons,text='Run all codes (WA)', command = RUN_THE_BURRITO )
        #        BURRITObutton.pack(side = "left")

        outpathbutton = Button(buttons, text='Set Outpath', command=findoutpath)
        outpathbutton.pack(side="left")

        inpathbutton = Button(buttons, text='Set Inpath', command=findinpath)
        inpathbutton.pack(side="left")

        customboundarybutton = Button(buttons, text='Create custom region', command=popupWindow)
        customboundarybutton.pack(side="left")

        ####################################################################################################################################################################
        #
        # So next let's talk about list boxes.
        # These are really cool.
        #
        #
        # Lesson over.
        #
        # Ok, in seriousness, you can make a listbox from any set of values, but dictionaries work best.
        # This is because we want something to happen when a user clicks on a selection.
        #
        # We also want the things that go into the list boxes to mean something.
        # I.E. for this file, it makes sense for the options in each listbox to relate to options
        # people can choose from the dictionaries (e.g. plot types, metric files etc.)
        #
        # This is another advantage of dictionaries as I already have listed all possible options in part 2 of the code
        # and I know those were my dictionary keys. So I can call them to populate the listbox with no extra effort.
        #
        # There are other ways of doing this, though if I do not use a dictionary. The alternative method is used for the list_of_calc_files listbox at the bottom.
        #
        # Listbox needs at least four lines, but these four lines vary depending on whether you are using a dictionary or a list
        #
        # - first (for dictionary) - get the dictionary keys
        # - second - make the listbox (and if you have a dictionary, fill it with the keys here)
        # - 2a - for a list, fill it here (see the lbcalc below)
        # - third - tell Tkinter what to do with the listbox and when to do it (i.e. bind a command to an event)
        # - fourth - pack the listbox so it appears on root
        #
        # Below I have annotated lbplot and lbcalc. The other list boxes are almost exact copies of lbplot
        ###################################################################################################################


        scrollbar = Scrollbar(lists, orient=VERTICAL)
        labelcalc = Label(labels, text='Please select \n metric file', width=15, height=2)
        labelcalc.pack(side='left')
        # So what do we do when we don't have a dictionary?
        # Also, because the list_of_calc_files was made using glob, it is going to have
        # a load of gunk in front of the actual part of the file name that tells me what the file does.
        # Lets do these two here.
        # as before, we want a global list (list_of_calc_files) from part 1 of the code
        global list_of_calc_files
        # Now we make the listbox, but it is empty.
        lbcalc = Listbox(lists, yscrollcommand=scrollbar.set, width=15, height=5, exportselection=False)
        scrollbar.config(command=lbcalc.yview)
        scrollbar.pack(side=LEFT, fill=Y)
        # Let's fill it, with all the calc files in list_of_calc_files 
        # which if we remember is a list of strings
        for item in list_of_calc_files:  # for anything in list_of_calc_files
            string = item.split('calc_')[-1]  # take that string, and whenever it says "calc_" (which it will)
            # split the code in 2 here and only keep the last bit
            # so for /nfs/a266/homes/earv061/metrics_workshop/Teacher/calc_Regional_Onset_with_notes.py
            # this will leave me with Regional_Onset_with_notes.py .
            # But for the purpose of importing a file, we do not need the ".py" bit...
            just_name = string.split(".")[0]  # ...so cut that off to!
            # Next what we do is populate the listbox, with the string just_name that we just made.
            # We can do this several ways, but the easiest is to insert it at the end of the list as it currently stands
            # This ensures that we always get the whole list and don't risk overwriting things in the list
            lbcalc.insert(END, just_name)
        # bind as normal    
        lbcalc.bind("<Double-Button-1>", OnDoubleCalc)
        # keep it clean
        lbcalc.pack(side="left", expand=True)

        labelbcs = Label(labels, text='Please select \n Model resolution', width=15, height=2)
        labelbcs.pack(side='left')
        global bcs_dictionary
        items = StringVar(value=tuple(sorted(bcs_dictionary.keys())))
        lbbc = Listbox(lists, listvariable=items, width=15, height=5, exportselection=False)
        lbbc.bind("<Double-Button-1>", OnDoubleBC)
        lbbc.pack(side="left", expand=True)

        labelper = Label(labels, text='Please select \n scenario', width=15, height=2)
        labelper.pack(side='left')
        global period_dictionary
        items = StringVar(value=tuple(sorted(period_dictionary.keys())))
        lbper = Listbox(lists, listvariable=items, width=15, height=5, exportselection=False)
        lbper.bind("<Double-Button-1>", OnDoublePeriod)
        lbper.pack(side="left", expand=True)

        labelbound = Label(labels, text='Please select \n region', width=15, height=2)
        labelbound.pack(side='left')
        global boundary_dictionary
        items = StringVar(value=tuple(sorted(boundary_dictionary.keys())))
        lbbound = Listbox(lists, listvariable=items, width=15, height=5, exportselection=False)
        lbbound.bind("<Double-Button-1>", OnDoubleBoundary)
        lbbound.pack(side="left", expand=True)

        labelseas = Label(labels, text='Please select \n season/month', width=15, height=2)
        labelseas.pack(side='left')
        global season_dictionary
        items = StringVar(value=tuple(sorted(season_dictionary.keys())))
        lbbound = Listbox(lists, listvariable=items, yscrollcommand=scrollbar.set, width=15, height=5,
                          exportselection=False)
        scrollbar.config(command=lbbound.yview)
        scrollbar.pack(side=LEFT, fill=Y)
        lbbound.bind("<Double-Button-1>", OnDoubleSeason)
        lbbound.pack(side="left", expand=True)

        #        labelvar = Label(labels,text='Please select \n varaible', width = 15, height = 2)
        #        labelvar.pack(side='left')
        #        global variables_dictionary
        #        items = StringVar(value=tuple(sorted(variables_dictionary.keys())))
        #        lbvar = Listbox(lists, listvariable=items, width=15, height=5, exportselection=False)
        #        lbvar.bind("<Double-Button-1>", OnDoubleVariable)
        #        lbvar.pack(side="left",expand=True)

        labelplot = Label(labels, text='Please select \n plot type', width=15, height=2)
        labelplot.pack(side='left')

        global list_of_plot_files
        # Same as for calc files here
        lbplot = Listbox(lists, yscrollcommand=scrollbar.set, width=15, height=5, exportselection=False)
    #    scrollbar.config(command=lbplot.yview)
     #   scrollbar.pack(side=, fill=Y)

        for item in list_of_plot_files:  # for anything in list_of_plot_files
            string = item.split('plot_')[-1]
            just_name = string.split(".")[0]  # ...so cut that off to!
            lbplot.insert(END, just_name)
        # bind as normal
        lbplot.bind("<Double-Button-1>", OnDoublePlot)
        # keep it clean
        lbplot.pack(side="left", expand=True)

        OVERvar = Label(labels, text='Overwrite \n existing files?', width=15, height=2)
        OVERvar.pack(side='left')
        global overwrite_dictionary
        items = StringVar(value=tuple(sorted(overwrite_dictionary.keys())))
        lbover = Listbox(lists, listvariable=items, width=15, height=5, exportselection=False)
        lbover.bind("<Double-Button-1>", OnDoubleOverwrite)
        lbover.pack(side="left", expand=True)


# Still with me? Wow, you are good. Like,
# ...
# ...
# really good.
#
#
# If you were a variable (do not read "if you were variable"), it would read:
# you = that_darn_good
#
# But, you are not finished yet.
# Now we need to call the code, and set up the main window when the GUI is called from
# the command line.
#
# Again, not 100% on this so cannot teach in too much depth, but the last 4 lines of this file will always
# work for this file. So maybe learn more if you plan to be more complex, but for now keep them as they are.


if __name__ == "__main__":
    root = Tk()
    m = mainWindow(root)
    root.mainloop()

# Go get a coffee, you have earned it.
