# pimenu.py
# Jakob Zielinski
# Menus for Raspberry Pi 128x32 screen


class option():
    def __init__(self, string, action, args=None):
        self.action = action
        self.string = string
        self.args = args


    def __str__(self):
        return(self.string)


    def execute(self):
        if self.args is not None:
            self.action(*self.args)
        else:
            self.action()


class menu():
    def __init__(self):
        self.options = []
        self.current = 0
        self.action = None
        self.args = None


    # Move the cursor up
    def move_up(self):
        self.current = self.current-1
        if self.current < 0:
            self.current = len(self.options)-1


    # Move the cursor down
    def move_down(self):
        self.current = self.current+1
        if self.current == len(self.options):
            self.current = 0

    
    # Add an option to the option list
    def add_option(self, o):
        self.options.append(o)


    def current_option(self):
        return self.options[self.current]


    def option_string_list(self):
        string_list = []
        for o in self.options:
            if o is self.options[self.current]:
                string_list.append('> '+o.string)
            else:
                string_list.append(o.string)

        return string_list


    def execute(self, menu, args):
        if self.action is not None:
            self.action(menu, *args)


    def update_execute(self, func, args=None):
        self.action = func
        self.args = args


    def __str__(self):
        return '\n'.join(self.option_string_list())


def main():

    def test():
        print('option executed')
    m = menu()
    m.add_option(option('System Information', test))
    m.add_option(option('HID', test))
    m.add_option(option('Ping', test))
    m.add_option(option('Reboot', test))
    m.add_option(option('Shutdown', test))
    print(m)
    m.move_down()
    m.move_down()
    m.move_down()
    m.move_down()
    m.move_down()
    m.move_up()
    print(m)


if __name__ == '__main__':
    main()


