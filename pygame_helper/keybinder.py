import pygame


class Keybinder(dict):

    def __init__(self, *args):
        super().__init__()

        for arg in args:
            self.add_new_option(arg)


    def add_new_option(self, option_name):
        self[option_name] = {"keybinds": set(), "value": 0}

    def add_keybinds_and_value_to_multiple_options(self, *args):
        for arg in args:
            self.add_keybinds_and_value_to_option(*arg)

    def add_keybinds_and_value_to_option(self, option_name, keys, value):
        if option_name not in self:
            raise KeyError(f"'{option_name}' is not in keybinder")
        if isinstance(keys, str):
            raise TypeError("'keys' must be an iterable, not a string")

        self.add_multiple_keybinds_to_option(option_name, keys)
        self.assign_value_to_option(option_name, value)

    def add_multiple_keybinds_to_option(self, option_name, keys):
        if option_name not in self:
            raise KeyError(f"'{option_name}' is not in keybinder")

        for key in keys:
            self.add_keybind_to_option(option_name, key)

    def add_keybind_to_option(self, option_name, key):
        if option_name not in self:
            raise KeyError(f"'{option_name}' is not in keybinder")

        self[option_name]["keybinds"].add(key)

    def assign_value_to_option(self, option_name, value):
        if option_name not in self:
            raise KeyError(f"'{option_name}' is not in keybinder")

        self[option_name]["value"] = value


    def reset(self):
        self.remove_all_keybinds_from_all_options()
        self.reset_all_values()

    def remove_all_keybinds_from_all_options(self):
        for option_name in self:
            self[option_name]["keybinds"] = set()

    def remove_all_keybinds_from_option(self, option_name):
        if option_name not in self:
            raise KeyError(f"'{option_name}' is not in keybinder")

        self[option_name]["keybinds"] = set()

    def remove_keybind_from_option(self, option_name, key):
        if option_name not in self:
            raise KeyError(f"'{option_name}' is not in keybinder")

        self[option_name]["keybinds"].discard(key)

    def reset_all_values(self):
        for option_name in self:
            self[option_name]["value"] = 0

        
    def is_key_pressed_for_option(self, option_name, keys_pressed=None):
        if option_name not in self:
            raise KeyError(f"'{option_name}' is not in keybinder")

        keys_pressed = pygame.key.get_pressed() if keys_pressed == None else keys_pressed
        for key in self[option_name]["keybinds"]:
            if keys_pressed[key]:
                return True
        return False

    def get_value_for_option(self, option_name):
        if option_name not in self:
            raise KeyError(f"'{option_name}' is not in keybinder")

        return self[option_name]["value"]


    def __repr__(self):
        option_names_joined = ", ".join(self.keys())
        return f"{self.__class__.__name__}({option_names_joined})"

    def __str__(self):
        option_names_with_its_values = [f"{option_name}={values}" for option_name, values in self.items()]
        option_names_and_values_joined = ", ".join(option_names_with_its_values)
        option_names_and_values_joined = option_names_and_values_joined.replace("set()", "{}")
        return f"{self.__class__.__name__}({option_names_and_values_joined})"