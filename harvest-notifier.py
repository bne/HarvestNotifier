import pygtk
import gtk

from harvest import Harvest

# temporary import till we figure out config loading
import scratch

class HarvestNotifier:
    
    def __init__(self):
        
        self.harvest = Harvest(scratch.url, scratch.username, scratch.password)
        
        self.statusIcon = gtk.StatusIcon()
        self.statusIcon.set_from_stock(gtk.STOCK_ABOUT)
        self.statusIcon.set_visible(True)
        self.statusIcon.set_tooltip("Hello World")
    
        self.menu = gtk.Menu()
        
        project_menu = gtk.Menu()
        
        for client, projects in self.harvest.get_project_in_categories().iteritems():
            
            client_item = gtk.MenuItem(client)
            project_menu.append(client_item)
            
            for project in projects:
                task_menu = gtk.Menu()
                p = gtk.MenuItem(project['name'])
                
                for task in project['tasks']:
                    t = gtk.MenuItem(task['name'])
                    t.connect('activate', self.task_cb, self.menu)
                    task_menu.append(t)
                
                p.set_submenu(task_menu)
                project_menu.append(p)
            sep = gtk.SeparatorMenuItem()
            project_menu.append(sep)
        
        
        self.menuItem = gtk.MenuItem('Projects')
        self.menuItem.set_submenu(project_menu)
        self.menu.append(self.menuItem)
        
        self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.menuItem.connect('activate', self.quit_cb, self.statusIcon)
        self.menu.append(self.menuItem)
    
        self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)
        self.statusIcon.set_visible(1)
    
        gtk.main()
        
    def task_cb(self, widget, event, data = None):
        window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        window.set_border_width(10)
    
        button = gtk.Button("Hello World")
        button.connect_object("clicked", gtk.Widget.destroy, window)
    
        window.add(button)
        button.show()
        window.show()
        
    def quit_cb(self, widget, data = None):
        gtk.main_quit()
        
    def popup_menu_cb(self, widget, button, time, data = None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, gtk.status_icon_position_menu,
                           3, time, self.statusIcon)
        
if __name__ == "__main__":
    notifier = HarvestNotifier()