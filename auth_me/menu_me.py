import getpass
import time

try:
    from auth_me import User
except (ImportError, ModuleNotFoundError):
    from auth_me.auth_me import User


class Menu:
    def __init__(self):
        user = getpass.getuser()
        pw = getpass.getpass(f'Hello {user}!\nPlease enter your password: ')

        self._auth = User(user, pw)

        self._options = {1: self._auth.make_action,
                         2: self._auth.show_usr_permissions,
                         3: self._close}

        self._super_options = {1: self._auth.LoginManager.add_user,
                               2: self._auth.GroupManager.add_group,
                               3: self._auth.GroupManager.PermissionManager.add_action,
                               4: self._auth.LoginManager.add_membership,
                               5: self._auth.LoginManager.del_user,
                               6: self._auth.GroupManager.del_group,
                               7: self._auth.GroupManager.PermissionManager.del_action,
                               8: self._auth.LoginManager.del_membership,
                               9: self._auth.show_super_permissions,
                               10: self._back,
                               11: self._close}

    def display_options(self):
        options = 'Please select an option number:' \
                  '\n1  -   Make Action' \
                  '\n2  -   View your Groups and Permissions' \
                  '\n3  -   Exit Program\n'

        add_super_option = ''

        if self._auth.issuperuser:
            add_super_option = '9  -   SuperUser Actions\n'
            dict_opt = {9: self.display_super_options}

            self._options = {**self._options, **dict_opt}

        selected_option = input(options + add_super_option)

        try:
            selected_option = int(selected_option)
            state = self._options[selected_option]()
            return state
        except (KeyError, ValueError):
            print('Invalid Option! Please enter a valid option number.')
            time.sleep(2)
            self.display_options()

    def display_super_options(self):
        selected_option = input('Please select an option number:'
                                '\n1    -   Add User'
                                '\n2    -   Add Group'
                                '\n3    -   Add Permission'
                                '\n4    -   Add Membership'
                                '\n5    -   Delete User'
                                '\n6    -   Delete Group'
                                '\n7    -   Delete Permission'
                                '\n8    -   Delete Membership'
                                '\n9    -   View all Users, Groups and Permissions'
                                '\n10   -   Back to Main Menu'
                                '\n11   -   Exit Program\n')

        try:
            selected_option = int(selected_option)
            state = self._super_options[selected_option]()
            return state
        except (KeyError, ValueError):
            print('Invalid Option! Please enter a valid option number.')
            time.sleep(2)
            self.display_super_options()

    def _update_usr_vars(self):
        self._auth.get_groups()
        self._auth.get_permissions()

    def _back(self):
        self.display_options()

    @staticmethod
    def _close():
        time.sleep(2)
        print('Closing Program...')
        return False
