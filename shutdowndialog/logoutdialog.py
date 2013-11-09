#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  logoutdialog.py
#  Versi 2.0
#  Copyright 2013 Azis Ws <azis.astrojim@surabaya.di.blankon.in>
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
#  

import dbus
import gtk
import os
 
class DBusExecutor(object):
# ConsoleKit - to reboot and shutdown (system bus) 
    ConsoleKitService = 'org.freedesktop.ConsoleKit'
    ConsoleKitPath = '/org/freedesktop/ConsoleKit/Manager'
    ConsoleKitInterface = 'org.freedesktop.ConsoleKit.Manager'
# UPower - to hibernate and suspend (system bus)
    UPowerService = 'org.freedesktop.UPower'
    UPowerPath = '/org/freedesktop/UPower'
    UPowerInterface = UPowerService
 
    def __init__(self):
        self.__bus = dbus.SystemBus()
 
    def logout(self, widget=None):
        os.system("dbus-send --session --type=method_call --print-reply --dest=org.gnome.SessionManager /org/gnome/SessionManager org.gnome.SessionManager.Logout uint32:1")
        self.cancel()
 
    def suspend(self, widget=None):
        obj = self.__bus.get_object(self.UPowerService, self.UPowerPath)
        manager = dbus.Interface(obj, self.UPowerInterface)
        if manager.SuspendAllowed():
            manager.Suspend()
            self.cancel()
 
    def cancel(self, widget=None):
        # Check if we're already in gtk.main loop
        if gtk.main_level() > 0:
            gtk.main_quit()
        else:
            exit(1)
 
class BiggerButton(gtk.Button):
    def __init__(self, label=None):
        gtk.Button.__init__(self, label, use_underline=True)
        self.set_size_request(0, 80)
 
class OBLogout(object):
    def __init__(self):
        self.executor = DBusExecutor()
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("")
        self.window.set_size_request(330, 165)
        self.window.set_border_width(10)
        self.window.connect("destroy", self.executor.cancel)

        self.box0 = gtk.VBox(False, 0)
        self.box1 = gtk.HBox(False, 0)
        self.box2 = gtk.HBox(False, 0)
        self.window.add(self.box0)

        # Add the vertical elementals
        self.label = gtk.Label()
        self.label.set_line_wrap(False)
        self.label.set_use_markup(True)
        self.label.set_markup("<span>Select one action or cancel</span>")
        
        self.box0.pack_start(self.label, 0, False, 5)
        self.box0.pack_start(self.box1, False, False, 5)
        self.box0.pack_start(self.box2, False, False, 0)
 
        icon_size = gtk.ICON_SIZE_DIALOG
 
        #Cancel
        cancel_btn = BiggerButton()
        icon = gtk.image_new_from_icon_name('application-exit', icon_size)
        icon.set_pixel_size(70)
        cancel_btn.set_property('image', icon)
        cancel_btn.connect('clicked', self.executor.cancel)
        self.box1.pack_start(cancel_btn, True, True, 10)
        
        text = gtk.Label('Cancel')
        text.set_size_request(80, 20)
        self.box2.pack_start(text, True, True, 10)

        #sep = gtk.VSeparator()
        #self.box1.pack_start(sep, True, True, 0)
 
        #Suspend
        suspend_btn = BiggerButton()
        icon = gtk.image_new_from_icon_name('gnome-session-suspend', icon_size)
        icon.set_pixel_size(70)
        suspend_btn.set_property('image', icon)
        suspend_btn.connect('clicked', self.executor.suspend)
        self.box1.pack_start(suspend_btn, True, True, 10)

        text = gtk.Label('Suspend')
        text.set_size_request(80, 20)
        self.box2.pack_start(text, True, True, 10)

        #Logout
        logout_btn = BiggerButton()
        icon = gtk.image_new_from_icon_name('gnome-session-logout', icon_size)
        icon.set_pixel_size(70)
        logout_btn.set_property('image', icon)
        logout_btn.connect('clicked', self.executor.logout)
        self.box1.pack_start(logout_btn, True, True, 10)
 
        text = gtk.Label('Log Out')
        text.set_size_request(80, 20)
        self.box2.pack_start(text, True, True, 10)
 
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self.window.set_skip_taskbar_hint(True)
        self.window.stick()
        self.window.set_decorated(True)
        self.window.show_all()

    def main(self):
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass
 
if __name__ == "__main__":
    obl = OBLogout()
    obl.main()

