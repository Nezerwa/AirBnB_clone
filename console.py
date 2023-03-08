#!/usr/bin/python3

"""An interactive shell"""

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.state import State
from models.review import Review
import shlex


class HBNBCommand(cmd.Cmd):
    """Interactive command for HBNB project"""

    prompt = "(hbnb)  "

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }
    __cmd = ['create', 'show', 'update', 'all', 'destroy', 'count']

    def precmd(self, arg):
        """parses command input"""
        if '.' in arg and '(' in arg and ')' in arg:
            cls = arg.split('.')
            cnd = cls[1].split('(')
            args = cnd[1].split(')')
            if cls[0] in type(self).__classes and cnd[0] in type(self).__cmd:
                arg = cnd[0] + ' ' + cls[0] + ' ' + args[0]
        return arg

    def do_EOF(self, line):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def do_create(self, args):
        """Creates a new instance of BaseModel

        Args:
            arg(line):  BaseModel command
        """
        args_split = args.split()

        if (len(args_split) == 0):
            print("** class name missing **")
        elif (args_split[0] not in type(self).__classes):
            print("** class doesn't exist **")
        else:
            print(eval(args_split[0])().id)
            storage.save()
            # objInstance = eval(args_split[0])()
            # objInstance.save()
            # print(objInstance.id)

    def do_show(self, args):
        """Prints the string representation of an instance
            based on the class name and id

            Args:
                arg(line)
        """
        args_split = args.split()

        if (len(args_split) == 0):
            print("** class name missing **")
        else:
            cls_name = args_split[0]
            if ((cls_name in type(self).__classes and len(args_split) < 2)):
                print("** instance id missing **")
            elif (cls_name not in type(self).__classes):
                print("** class doesn't exist **")
            else:
                try:
                    cls_id = args_split[1]
                    key = cls_name + "." + cls_id
                    all_objs = storage.all()
                    print(all_objs[key])

                except KeyError:
                    print("** no instance found **")

    def do_destroy(self, args):
        """Destroy the string representation of an instance
            based on the class name and id

            Args:
                arg(line)
        """
        args_split = args.split()

        if (len(args_split) == 0):
            print("** class name missing **")
        else:
            cls_name = args_split[0]
            if ((cls_name in type(self).__classes and len(args_split) < 2)):
                print("** instance id missing **")
            elif (cls_name not in type(self).__classes):
                print("** class doesn't exist **")
            else:
                try:
                    cls_id = args_split[1]
                    key = cls_name + "." + cls_id
                    all_objs = storage.all()
                    del all_objs[key]
                    storage.save()

                except KeyError:
                    print("** no instance found **")

    def do_all(self, args):
        """Prints all string representation of all instances based
        or not on the class name

        Args:
            args (line): command line arguement
        """
        all_objs = storage.all()
        obj_list = []
        if len(args) == 0:
            for key in all_objs.keys():
                obj_list.append(str(all_objs[key]))
            print(obj_list)

        else:
            args_split = args.split()
            if len(args_split) == 1:
                cls_name = args_split[0]
                if cls_name not in type(self).__classes:
                    print("** class doesn't exist **")
                else:
                    for key, value in all_objs.items():
                        key_split = key.split('.')
                        if cls_name == key_split[0]:
                            obj_list.append(str(all_objs[key]))
                    print(obj_list)

    def do_update(self, args):
        """Updates an instance based on the class name and id
        by adding or updating attribute
         Args:
            args (line): command line arguement
        """

        all_objs = storage.all()
        args_split = shlex.split(args)
        len_args = len(args_split)
        if len_args == 0:
            print("** class name missing **")
            return False
        else:
            cls_name = args_split[0]
            if (cls_name not in type(self).__classes):
                print("** class doesn't exist **")
                return False
            else:
                try:
                    cls_id = args_split[1]
                    key = cls_name + "." + cls_id
                    try:
                        unused = all_objs[key]
                    except KeyError:
                        print("** no instance found **")
                        return False
                except IndexError:
                    print('** instance id missing **')
                    return False
                if len_args < 3:
                    print("** attribute name missing **")
                    return False
                elif len_args < 4:
                    print("** value missing **")
                    return False

        key = cls_name + "." + cls_id
        if len_args > 2:
            if len_args > 3:
                setattr(storage.all()[key], args_split[2], args_split[3])
                storage.all()[key].save()
            else:
                return

    def do_count(self, args):
        """Count instance of class
            Args:
            args (line): command line arguement
        """
        count = 0
        all_objs = storage.all()
        for key in all_objs.keys():
            key_split = key.split(".")
            key_cls = key_split[0]
            if key_cls == args:
                count = count + 1
        print(count)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
