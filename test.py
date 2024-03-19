def do_create(self, args):
        """ Create an object of any class"""
        try:
            if not args:
                print("** class name missing **")
                return
            args = args.split()
            class_name = args[0]
            params = {}
            for arg in args[1:]:
                split_arg = arg.split("=")
                split_arg[1] = eval(split_arg[1])
            if isinstance(split_arg[1], str):
                split_arg[1] = split_arg[1].replace('_', '" "').replace('"', '\\"')
                params[split_arg[0]] = split_arg[1]
            if class_name not in HBNBCommand.classes:
                raise NameError("** class doesn't exist **")
           
            new_instance = HBNBCommand.classes[arg_list[0]](**params)
            new_instanice.save()
            print(new_instance.id)
            
        except SyntaxError as e:
            print(e)
        except NameError as e:
            print(e)

Old script
def do_create(self, args):
        """ Create an object of any class"""
        if not args:
            print("** class name missing **")
            return
        elif args not in HBNBCommand.classes:
            print("** class doesn't exist **")
            return
        new_instance = HBNBCommand.classes[args]()
        storage.save()
        print(new_instance.id)
        storage.save()
