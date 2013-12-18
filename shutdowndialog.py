#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  shutdowndialog.py
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

    def restart(self, widget=None):
        obj = self.__bus.get_object(self.ConsoleKitService, self.ConsoleKitPath)
        manager = dbus.Interface(obj, self.ConsoleKitInterface)
        if manager.CanRestart():
            manager.Restart()
            self.logout()
 
    def shutdown(self, widget=None):
        obj = self.__bus.get_object(self.ConsoleKitService, self.ConsoleKitPath)
        manager = dbus.Interface(obj, self.ConsoleKitInterface)
        if manager.CanStop():
            manager.Stop()
            self.logout()
 
    def suspend(self, widget=None):
        obj = self.__bus.get_object(self.UPowerService, self.UPowerPath)
        manager = dbus.Interface(obj, self.UPowerInterface)
        if manager.SuspendAllowed():
            manager.Suspend()
            self.cancel()
 
    def hibernate(self, widget=None):
        obj = self.__bus.get_object(self.UPowerService, self.UPowerPath)
        manager = dbus.Interface(obj, self.UPowerInterface)
        if manager.HibernateAllowed():
            manager.Hibernate()
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
        self.set_size_request(0, 60)
 
class OBShutdown(object):
	
    def __init__(self):
        self.executor = DBusExecutor()
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#1A1A1A'))
        self.window.set_size_request(360,160)
        self.window.set_decorated(False)
        self.window.set_border_width(5)

        self.window.connect("destroy", self.executor.cancel)

        self.box0 = gtk.VBox(False, 0)
        self.box1 = gtk.HBox(False, 0)
        self.box2 = gtk.HBox(False, 0)
        self.box3 = gtk.HBox(False, 0)
        self.box4 = gtk.VBox(False, 0)
        self.window.add(self.box0)

        # Add the vertical elementals
        self.label = gtk.Label()
        self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color('#ccc'))
        self.label.set_line_wrap(False)
        self.label.set_use_markup(True)
        self.label.set_markup("Save all programs and select one action or cancel")
        
        self.box0.pack_start(self.box3, False, False, 0)
        self.box0.pack_start(self.box4, False, False, 0)
        
        self.box0.pack_start(self.label, False, False, 3)
        self.box0.pack_start(self.box1, False, False, 4)
        self.box0.pack_start(self.box2, False, False, 0)
 
        icon_size = gtk.ICON_SIZE_DIALOG
        
        #cancel_btn = gtk.Button(' X ')
        #cancel_btn.set_border_width(0)
        #cancel_btn.connect('clicked', self.executor.cancel)
        #self.box3.pack_start(cancel_btn, False, False, 325)
        
        sep = gtk.HSeparator()
        sep.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#444'))
        self.box4.pack_start(sep, False, False, 3)

        #Cancel
        cancel_btn = gtk.Button()
        cancel_btn.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#1A1A1A'))
        icon = gtk.image_new_from_icon_name('application-exit', icon_size)
        icon.set_pixel_size(16)
        cancel_btn.set_property('image', icon)
        cancel_btn.connect('clicked', self.executor.cancel)
        self.box3.pack_start(cancel_btn, False, False, 325)
        
        #text = gtk.Label('Cancel')
        #text.set_size_request(60, 25)
        #self.box5.pack_start(text, True, True, 25)

        #Restart
        restart_btn = BiggerButton()
        restart_btn.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#1A1A1A'))
        icon = gtk.image_new_from_icon_name('gnome-session-reboot', icon_size)
        icon.set_pixel_size(50)
        restart_btn.set_property('image', icon)
        restart_btn.connect('clicked', self.executor.restart)
        self.box1.pack_start(restart_btn, True, True, 40)
        
        text = gtk.Label('Restart')
        text.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color('#ccc'))
        text.set_size_request(50, 15)
        self.box2.pack_start(text, True, True, 40)
 
        #Hibernate
        hibernate_btn = BiggerButton()
        hibernate_btn.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#1A1A1A'))
        icon = gtk.image_new_from_icon_name('gnome-session-hibernate', icon_size)
        icon.set_pixel_size(50)
        hibernate_btn.set_property('image', icon)
        hibernate_btn.connect('clicked', self.executor.hibernate)
        self.box1.pack_start(hibernate_btn, True, True, 0)

        text = gtk.Label('Hibernate')
        text.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color('#ccc'))
        text.set_size_request(50, 0)
        self.box2.pack_start(text, True, True, 0)

        #Shutdown
        shutdown_btn =BiggerButton()
        shutdown_btn.modify_bg(gtk.STATE_NORMAL, gtk.gdk.Color('#1A1A1A'))
        icon = gtk.image_new_from_icon_name('gnome-shutdown', icon_size)
        icon.set_pixel_size(50)
        shutdown_btn.set_property('image', icon)
        shutdown_btn.connect('clicked', self.executor.shutdown)
        self.box1.pack_start(shutdown_btn, True, True, 40)
 
        text = gtk.Label('Shutdown')
        text.modify_fg(gtk.STATE_NORMAL, gtk.gdk.Color('#ccc'))
        text.set_size_request(50, 0)
        self.box2.pack_start(text, True, True, 40)
 
        self.window.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
        self.window.set_skip_taskbar_hint(True)
        self.window.stick()
        self.window.show_all()

    def main(self):
        try:
            gtk.main()
        except KeyboardInterrupt:
            pass
 
if __name__ == "__main__":
    obs = OBShutdown()
    obs.main()

