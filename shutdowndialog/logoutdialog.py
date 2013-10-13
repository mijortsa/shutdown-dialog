#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  logout.py
#  
#  Copyright 2013 Azis Ws aka mijortsa<azis.astrojim@surabaya.di.blankon.in>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  

import pygtk
import subprocess
pygtk.require("2.0")
import gtk
import os
import sys

class ShutDownDialog:

    """init function - draws the window and does setup"""
    def __init__(self):
		
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("")
        self.window.set_size_request(260,170)
        self.window.set_position(gtk.WIN_POS_CENTER) 
        self.window.set_resizable(False)
        self.window.set_decorated(False)

        # Create packing boxes. Outer level is vertical containing
        # Label upper, then horizontal box lower.
        self.box0 = gtk.VBox(False, 15)
        self.box1 = gtk.HBox(False, 0)
        

        # Add the veritcal box to the window
        self.window.add(self.box0)
    
        # hook up delete callback to event
        #self.window.connect("delete_event", self.delete_event)
    
        # hook up destroy callback to event
        #self.window.connect("destroy", self.destroy)
    
        # Sets the border width of the window.
        self.window.set_border_width(10)
       
        # Label for message
        self.label = gtk.Label()
        self.label.set_line_wrap(False)
        self.label.set_use_markup(True)
        self.label.set_markup("<span size='12000'>Log Out Manokwari Account</span>")
        
        # Add the vertical elementals
        self.box0.pack_start(self.label, False, False, 0)
        self.box0.pack_start(self.box1, False, False, 0)
        
        # Creates Shutdown buttons        
        image1 = gtk.Image()
        image1.set_from_file("/usr/share/shutdowndialog/logout.png")
        image1.show()
        self.logout_button = gtk.Button()
        self.logout_button.add(image1)
        self.logout_button.show()
        
           # Creates Cancel buttons
        image4 = gtk.Image()
        image4.set_from_file("/usr/share/shutdowndialog/cancel.png")
        image4.show()
        self.cancel_button = gtk.Button()
        self.cancel_button.add(image4)
        self.cancel_button.show()
    
        # Hook up enable button to callback on click event
        self.logout_button.connect("clicked", self.logout)
    
        # Hook up the cancel button to destroy callback on click event
        self.cancel_button.connect_object("clicked", gtk.Widget.destroy, self.window)
    
        # This packs the buttons into the horizontal box (container).
        self.box1.pack_start(self.cancel_button, True, True, 10)
        self.cancel_button.show()

        self.box1.pack_start(self.logout_button, True, True, 10)
        self.logout_button.show()

        # Make the items visible...
        self.label.show()
        self.box1.show()
        self.box0.show()
    
        # Make the window visible...
        self.window.show()
    
    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()      
 
    def logout(self, widget = None, data = None):
        os.system("dbus-send --session --type=method_call --print-reply --dest=org.gnome.SessionManager /org/gnome/SessionManager org.gnome.SessionManager.Logout uint32:1")
        gtk.main_quit()
     
# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    launcher = ShutDownDialog()
    launcher.main()
