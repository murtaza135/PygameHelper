import pygame


class Keybinder(dict):

    def __init__(self, *args):
        super().__init__()
        self.tracked_keys = set()
        self.pressed_keys_order = list()

        for arg in args:
            self.add_new_option(arg)


    def add_new_option(self, option_name):
        self[option_name] = {"keybinds": set(), "value": 0}

    def add_keybinds_and_value_to_multiple_options(self, *args):
        for arg in args:
            self.add_keybinds_and_value_to_option(*arg)

    def add_keybinds_and_value_to_option(self, option_name, keys, value):
        self._raise_key_error_if_option_name_invalid(option_name)
        if isinstance(keys, str):
            raise TypeError("'keys' must be an iterable, not a string")

        self.add_multiple_keybinds_to_option(option_name, keys)
        self.assign_value_to_option(option_name, value)

    def add_multiple_keybinds_to_option(self, option_name, keys):
        self._raise_key_error_if_option_name_invalid(option_name)
        for key in keys:
            self.add_keybind_to_option(option_name, key)

    def add_keybind_to_option(self, option_name, key):
        self._raise_key_error_if_option_name_invalid(option_name)
        self[option_name]["keybinds"].add(key)

    def assign_value_to_option(self, option_name, value):
        self._raise_key_error_if_option_name_invalid(option_name)
        self[option_name]["value"] = value

    def track_keys_for_multiple_options(self, *option_names):
        for option_name in option_names:
            self.track_keys_for_option(option_name)

    def track_keys_for_option(self, option_name):
        self._raise_key_error_if_option_name_invalid(option_name)
        for key in self[option_name]["keybinds"]:
            self.tracked_keys.add(key)


    def reset(self):
        self.remove_all_keybinds_from_all_options()
        self.reset_all_values()

    def remove_all_keybinds_from_all_options(self):
        for option_name in self:
            self[option_name]["keybinds"] = set()
        self.tracked_keys = set()

    def remove_all_keybinds_from_option(self, option_name):
        self._raise_key_error_if_option_name_invalid(option_name)
        self.remove_tracked_keys_for_option(option_name)
        self[option_name]["keybinds"] = set()

    def remove_keybind_from_option(self, option_name, key):
        self._raise_key_error_if_option_name_invalid(option_name)
        self[option_name]["keybinds"].discard(key)
        self.remove_tracked_key(key)

    def reset_all_values(self):
        for option_name in self:
            self[option_name]["value"] = 0

    def remove_tracked_keys_for_option(self, option_name):
        self._raise_key_error_if_option_name_invalid(option_name)
        for key in self[option_name]["keybinds"]:
            self.remove_tracked_key(key)

    def remove_tracked_key(self, key):
        self.tracked_keys.discard(key)

        
    def is_key_pressed_for_option(self, option_name):
        self._raise_key_error_if_option_name_invalid(option_name)
        keys_pressed = pygame.key.get_pressed()
        for key in self[option_name]["keybinds"]:
            if keys_pressed[key]:
                return True
        return False

    def is_key_most_recently_pressed_for_option(self, option_name):
        if len(self.pressed_keys_order) == 0:
            return False

        most_recently_pressed_key = self.pressed_keys_order[-1]
        for key in self[option_name]["keybinds"]:
            if key == most_recently_pressed_key:
                return True
        return False

    def update_pressed_keys_order(self):
        pressed_keys = pygame.key.get_pressed()

        for key in self.tracked_keys:
            if pressed_keys[key]:
                if key not in self.pressed_keys_order:
                    self.pressed_keys_order.append(key)
            else:
                try:
                    self.pressed_keys_order.remove(key)
                except ValueError:
                    pass

    def get_value_for_option(self, option_name):
        self._raise_key_error_if_option_name_invalid(option_name)
        return self[option_name]["value"]

    
    def _raise_key_error_if_option_name_invalid(self, option_name):
        if option_name not in self:
            raise KeyError(f"'{option_name}' is not in keybinder")

    def __repr__(self):
        option_names_joined = ", ".join(self.keys())
        return f"{self.__class__.__name__}({option_names_joined})"

    def __str__(self):
        option_names_with_its_values = [f"{option_name}={values}" for option_name, values in self.items()]
        option_names_and_values_joined = ", ".join(option_names_with_its_values)
        option_names_and_values_joined = option_names_and_values_joined.replace("set()", "{}")
        return f"{self.__class__.__name__}({option_names_and_values_joined})"