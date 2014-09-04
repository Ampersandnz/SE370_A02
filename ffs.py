# SoftEng 370 Assignment 2
# "Tree" file system
# Michael Lo
# mlo450
# 5530588

# Resources:
# Assignment 1 code.

import shlex
import os


class FSDirectory:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.children = []
        self.files = []
        self.is_root = name is '-'

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        if self.is_root:
            print ('Cannot rename root!')
        elif new_name.contains('-'):
            print ('Directory names cannot contain \"-\"!')
        else:
            self.name = new_name

    def get_parent(self):
        if not self.is_root:
            return self.parent

    def set_parent(self, new_parent):
        if self.is_root:
            print('Cannot set the parent of root!')
        elif new_parent is None:
            print('Directories cannot have null parents!')
        elif new_parent is not FSDirectory:
            print('Directories must have parents of type FSDirectory!')
        else:
            self.parent = new_parent

    def contains_child(self, child_name):
        for d in self.children:
            if d.get_name() == child_name:
                return True
        return False

    def contains_file(self, file_name):
        for f in self.files:
            if f.get_name() == file_name:
                return True
        return False

    def get_child(self, child_name):
        for d in self.children:
            if d.get_name() == child_name:
                return d
        print('Directory not found: ' + child_name)
        return False

    def get_file(self, file_name):
        for f in self.files:
            if f.get_name() == file_name:
                return f
        print('File not found: ' + file_name)
        return False

    def add_child(self, child):
        if child is FSDirectory:
            self.children.append(child)
            return True
        else:
            return False

    def add_file(self, new_file):
        if new_file is FSFile:
            self.files.append(new_file)
            return True
        else:
            return False

    def remove_child(self, child_name):
        for c in self.children:
            if c.get_name() == child_name:
                self.children.remove(c)
                return True
        print('Directory not found: ' + child_name)
        return False

    def remove_file(self, file_name):
        for f in self.files:
            if f.get_name() == file_name:
                self.files.remove(f)
                return True
        print('File not found: ' + file_name)
        return False

    def remove_all_children(self):
        for c in self.children:
            c.delete()
            self.children.remove(c)

    def remove_all_files(self):
        for f in self.files:
            f.delete()
            self.files.remove(f)

    def delete(self):
        self.remove_all_children()
        self.remove_all_files()


class FSFile:
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        #TODO: Create file with correct name
        #TODO: Save reference to that file in the object

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        if new_name.contains('-'):
            print ('File names cannot contain \"-\"!')
        else:
            self.name = new_name

    def get_parent(self):
        return self.parent

    def set_parent(self, new_parent):
        if new_parent is None:
            print('Files cannot have null parents!')
        elif new_parent is not FSDirectory:
            print('Files must have parents of type FSDirectory!')
        else:
            self.parent = new_parent

    def delete(self):
        #TODO: Delete the real file representing this file
        pass

# Lists the commands that will be executed by this program.
fileSystemCommandList = ['pwd', 'cd', 'ls', 'rls', 'tree', 'clear', 'create', 'add', 'cat', 'delete', 'dd', 'quit', 'q']

home_dir = "-"
current_dir = home_dir


# Accepts user input, and runs the commands when they are entered.
def main():
    while 1:
        try:
            user_input = input('ffs> ')
            if user_input.strip() != '':
                try:
                    do_command(user_input)
                except:
                    print("SOME KIND OF ERROR OCCURRED")
                    exit()
        except KeyboardInterrupt:
            print('')
        except EOFError:
            exit()


# Parses the string into its command and arguments, then executes that command with those arguments.
def do_command(user_input):
    command_with_args = parse_input(user_input)
    command = command_with_args[0]

    if command in fileSystemCommandList:
        fileSystemCommands[command](command_with_args)
    else:
        print(command + ': command not found')
    return


# Takes in the full typed string and returns the command split into its component arguments.
def parse_input(user_input):
    lexer = shlex.shlex(user_input, posix=True)
    lexer.whitespace_split = False
    lexer.wordchars += '#$+-,./?@^='
    args = list(lexer)
    return args


# Print the current working directory.
def fs_pwd(arguments):
    print(current_dir)


# Change the current working directory.
def fs_cd(command_with_args):
    if len(command_with_args) == 1:
        new_dir = home_dir

    # elif command_with_args[1].startswith('..'):
    #     pass

    # elif arguments[1].startswith('.'):
    #     add_to_path = (arguments[1])[1:]
    #     new_path = os.getcwd() + add_to_path

    # elif arguments[1].startswith('/'):
    #     new_path = arguments[1]

    # elif command_with_args[1].startswith('-'):
    #     new_path = os.path.expanduser(arguments[1])

    # else:
    #     new_path = os.getcwd() + '/' + arguments[1]

    global current_dir
    current_dir = new_dir

    #print('ffs: cd: ' + command_with_args[1] + ': No such file or directory')
    return


# List the contents of the named directory.
def fs_ls(command_with_args):
    #If no argument, use current working directory
    pass


# List verbosely the contents of the real assignment directory.
def fs_rls(command_with_args):
    child_pid = os.fork()
    if child_pid == 0:
        os.execvp("ls", ["ls", "-l"])
    else:
        os.wait()


# Print the "tree" structure of the file system from the current working directory downwards.
def fs_tree(command_with_args):
    pass


# Remove all files in the file system.
def fs_clear(command_with_args):
    pass


# Create a file with the specified name.
def fs_create(command_with_args):
    pass


# Appends text to the named file.
def fs_add(command_with_args):
    pass


# Display the contents of the named file.
def fs_cat(command_with_args):
    pass


# Delete the named file.
def fs_delete(command_with_args):
    if len(command_with_args == 1):
        print('No file specified for deletion')
    else:
        file_to_delete = fs_get_file(command_with_args[1])
        file_to_delete.delete()


# Delete the named directory, plus all subdirectories and contained files.
def fs_dd(command_with_args):
    if len(command_with_args == 1):
        print('No directory specified for deletion')
    else:
        dir_to_delete = fs_get_directory(command_with_args[1])
        dir_to_delete.delete()
    #TODO: Ensure that the current working directory is changed when it is one of the
    # (sub)directories that are being deleted.


# Exit this program.
def fs_quit(command_with_args):
    exit()


# This function returns the file described by the given absolute or relative path.
def fs_get_file(path):
    #TODO: Write this.
    if path[0] == '-':
        #Absolute path
        pass
    else:
        #Relative path
        pass


# This function returns the directory described by the given absolute or relative path.
def fs_get_directory(path):
    #TODO: Write this.
    if path[0] == '-':
        #Absolute path
        pass
    else:
        #Relative path
        pass

# Map the inputs to the function blocks.
fileSystemCommands = {
    fileSystemCommandList[0]: fs_pwd,
    fileSystemCommandList[1]: fs_cd,  # TODO: Incomplete
    #fileSystemCommandList[2]: fs_ls,  # TODO: Not started
    fileSystemCommandList[3]: fs_rls,
    #fileSystemCommandList[4]: fs_tree,  # TODO: Not started
    #fileSystemCommandList[5]: fs_clear,  # TODO: Not started
    #fileSystemCommandList[6]: fs_create,  # TODO: Not started
    #fileSystemCommandList[7]: fs_add,  # TODO: Not started
    #fileSystemCommandList[8]: fs_cat,  # TODO: Not started
    fileSystemCommandList[9]: fs_delete,  # TODO: Incomplete
    fileSystemCommandList[10]: fs_dd,  # TODO: Incomplete
    fileSystemCommandList[11]: fs_quit,
    fileSystemCommandList[12]: fs_quit
}

if __name__ == '__main__':
    main()