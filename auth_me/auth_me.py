#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pprint
import hashlib
import time
import getpass

try:
    from errors_me import *
except (ImportError, ModuleNotFoundError):
    from auth_me.errors_me import *


class LoginManager:
    """ Stores Username and hash passwords"""
    def __init__(self, group_manager):
        # 1 = SuperUser :: 0 = Normal
        self.users = {'AQR': ('90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809', 1),
                      'Raizen': ('90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809', 1)}

        self.GroupManager = group_manager

    def add_user(self):
        """ Add a user to users attribute"""
        username = self.ask_username()

        if self.check_user_exist(username):
            print(f'Username ("{username}") already exist. Please try again.')
            time.sleep(2)
            self.add_user()
        else:
            encrypted_pw = self.ask_password(username)
            user_type = self.ask_user_type()

            self.users[username] = encrypted_pw, user_type

            time.sleep(2)
            print(f'Successfully added new user "{username}" in Database!')

            return True

    def del_user(self):
        """ Delete a user from the users attribute and from the GroupManager instance """
        users = list(self.users.keys())

        time.sleep(2)
        print('List of Current Users: {0}'.format(users))

        username = self.ask_username()

        self.users.pop(username, None)

        # cascade delete
        self.GroupManager.casc_delete_usr(username)

        time.sleep(2)
        print(f'Successfully deleted user "{username}" in Database')

        return True

    def check_valid_user(self, username, password):
        """  Checks if a user-password combination is valid
        Returns an InvalidPassword error if encrypted passwords do not match and
        UserDoesNotExist if the username does not exist"""
        try:
            encrypted_pw, user_type = self.users[username]
            if encrypted_pw == password:
                return
            else:
                raise InvalidPassword
        except KeyError:
            raise UserDoesNotExist

    def check_user_exist(self, username):
        """ Checks if a user exist as key in groups
        Returns a bool, if it does not exist: False"""
        try:
            info = self.users[username]
            raise UserAlreadyExist(username)
        except KeyError:
            return False
        except UserAlreadyExist:
            return True

    def check_superuser(self, username):
        return True if self.users[username][1] == 1 else False

    def ask_password(self, username):
        """ Ask password input """
        init_pw = getpass.getpass(f'Enter password of Username ("{username}") to be added: ')
        ver_pw = getpass.getpass(f'Reenter password of Username ("{username}") to be added: ')

        if init_pw != ver_pw:
            print('Error! Password not verified!')
            self.ask_password(username)
        else:
            encrypted_pw = self.hash_pw(init_pw)
            return encrypted_pw

    def ask_user_type(self):
        """ Ask user_type input"""
        user_type = input('Enter number for type of user[0:user | 1:superuser]: ')
        try:
            user_type = int(user_type)

            if user_type not in [0, 1]:
                raise ValueError
            return user_type
        except ValueError:
            print('User Type entered incorrect. Please enter "0" or "1".')
            self.ask_user_type()

    @staticmethod
    def ask_username():
        """ Ask username input"""
        username = input('Please enter username: ')

        return username

    @staticmethod
    def hash_pw(password):
        """ Encrypt password using SHA224 """
        encrypted_pw = hashlib.sha224(password.encode('utf8')).hexdigest()
        return encrypted_pw


class PermissionManager:
    def __init__(self):
        self.permissions = {'MIT': ['dance']}

    def add_action(self):
        """ Adds permission to a specific Group key"""
        group_name = self.ask_group()
        permission_name = self.ask_permission()

        if not self.check_group_exist(group_name) or not self.check_permission_exist(group_name, permission_name):
            print(f'Group "{group_name}" does not exist or '
                  f'Permission "{permission_name}" already exist. Please try again.')
            time.sleep(2)
            self.add_action()
        else:
            self.permissions.get(group_name).append(permission_name)
            time.sleep(2)
            print(f'Successfully added new permission "{permission_name}" to group "{group_name}"!')
            return True

    def del_action(self):
        """ Deletes a permission from a specific Group key"""
        group_name = self.ask_group()
        permission_name = self.ask_permission()

        if not self.check_group_exist(group_name):
            print(f'Group "{group_name}" does not exist. Please try again.')
        else:
            try:
                perm_list = self.permissions[group_name]
                perm_list.remove(permission_name)
                print(f'Successfully deleted permission "{permission_name}" from group "{group_name}"!')
            except ValueError:
                print(f'Permission name "{permission_name}" does not exist for group "{group_name}". Please try again.')
            finally:
                time.sleep(2)
                return True

    def check_group_exist(self, group_name):
        """ Checks if a group name exist as key in permissions attribute
        Raises an GroupAlreadyExist error if it does not exist """
        try:
            group = self.permissions[group_name]
            raise GroupAlreadyExist(group_name)
        except KeyError:
            return False
        except GroupAlreadyExist:
            return True

    def check_permission_exist(self, group_name, permission):
        """ Checks if a permission exist in a specific group
        Returns an boolean, if permission or group does not exist: True"""
        try:
            perm_list = self.permissions[group_name]
            if permission not in perm_list:
                raise PermissionDoesNotExist
            else:
                raise PermissionAlreadyExist
        except (KeyError, PermissionAlreadyExist):
            return False
        except PermissionDoesNotExist:
            return True

    @staticmethod
    def ask_permission():
        """ Ask permission name input"""
        permission_name = input('Please enter permission name: ')
        return permission_name

    @staticmethod
    def ask_group():
        """ Ask group name input """
        group_name = input('Please enter group name: ')
        return group_name


class GroupManager:
    """ Stores groups that contains respective permissions and users"""
    def __init__(self):
        self.groups = {'MIT': ['AQR', 'Raizen']}
        self.PermissionManager = PermissionManager()

    def add_group(self):
        """ Adds group name key in GroupManager and PermissionManager"""
        group_name = self.PermissionManager.ask_group()

        if self.PermissionManager.check_group_exist(group_name):
            print(f'Group ("{group_name}") already exist. Please try again.')
            time.sleep(2)
            self.add_group()
        else:

            self.groups.setdefault(group_name, [])
            self.PermissionManager.permissions.setdefault(group_name, [])

            time.sleep(2)
            print(f'Successfully added new group "{group_name}"!')
            return True

    def del_group(self):
        """ Deletes group name key in GroupManager and PermissionManager"""
        group_name = self.PermissionManager.ask_group()

        group_gm = self.groups.pop(group_name, None)
        group_pm = self.PermissionManager.permissions.pop(group_name, None)

        time.sleep(2)

        if group_gm is None or group_pm is None:
            print(f'Failed to delete. "{group_name}" group does not exist!')
        else:
            print(f'Successfully deleted group "{group_name}"!')

        return True

    # cascade delete user in every group
    def casc_delete_usr(self, username):
        """ Used by LoginManager class to cascade delete a user to the value of groups attribute """
        for group, usr_lst in self.groups.items():
            if username in usr_lst:
                usr_lst.remove(username)
                time.sleep(2)
                print(f'Successfully deleted user "{username}" in group "{group}"!')

        return True


# Used SHA224 to encrypt password
class User:
    """ User class"""
    def __init__(self, username, password):
        self.GroupManager = GroupManager()
        self.LoginManager = LoginManager(self.GroupManager)

        self.username = username
        self._encrypted_pw = self.LoginManager.hash_pw(password)

        try:
            self.LoginManager.check_valid_user(self.username, self._encrypted_pw)
        except (UserDoesNotExist, InvalidPassword):
            raise InvalidPassword('Error! Username or Password is incorrect. Please try again.')

        self.issuperuser = self.LoginManager.check_superuser(self.username)

        self.usr_groups = []        # not used
        self.usr_permissions = {}

        self.get_groups()
        self.get_permissions()

    def make_action(self):
        self.get_permissions()
        action = self.ask_action()

        actions_lst = set([perm for group, perm_list in self.usr_permissions.items() for perm in perm_list])

        if action not in actions_lst:
            print(f'Sorry, you do not have access to do action "{action}". Please contact admin and try again.')
        else:
            print(f'Successfully done action "{action}"!')
        return True

    def get_groups(self):           # not used
        groups = []
        for group, usr_lst in self.GroupManager.groups.items():
            if self.username in usr_lst:
                groups.append(group)

        self.usr_groups = groups

    def get_permissions(self):
        permissions = {}
        for gm_group in self.usr_groups:
            for pm_group, perm_lst in self.GroupManager.PermissionManager.permissions.items():
                if gm_group == pm_group:
                    permissions[gm_group] = perm_lst

        self.usr_permissions = permissions

    def show_usr_groups(self):      # not used
        format_groups = ', '.join(repr(usr) for usr in self.usr_groups)
        print('User "{0}" current groups: {1}'.format(self.username, format_groups))
        return True

    def show_usr_permissions(self):
        self.get_permissions()
        print(f'User "{self.username}" current groups and permissions:')
        pprint.pprint(self.usr_permissions)
        return True

    def show_super_permissions(self):
        print('\nAll users in LoginManager:')
        time.sleep(2)
        pprint.pprint([user for user, _ in self.LoginManager.users.items()])

        print('\nAll groups in GroupManager:')
        time.sleep(2)
        pprint.pprint(self.GroupManager.groups)

        print('\nAll permissions in PermissionManager:')
        time.sleep(2)
        pprint.pprint(self.GroupManager.PermissionManager.permissions)
        print('\n')

        return True

    @staticmethod
    def ask_action():
        """ Ask input from user for the group name """
        action = input('Please enter action: ')
        return action
