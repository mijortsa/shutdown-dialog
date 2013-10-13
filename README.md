<h3>pygtk shutdown, reboot, hibernate and logout dialog sending sign dbus</h3> 

- Shutdown, Reboot, Hibernate :

dbus-send --session --dest=org.freedesktop.PowerManagement --type=method_call /org/freedesktop/PowerManagement org.freedesktop.PowerManagement.Shutdown, reboot, hibernate


- Logout :

dbus-send --session --type=method_call --print-reply --dest=org.gnome.SessionManager /org/gnome/SessionManager org.gnome.SessionManager.Logout uint32:1


