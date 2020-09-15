from pygame_helper.input.abstract_input_component import AbstractInputComponent


class TileInputComponent(AbstractInputComponent):

    def __init__(self, movement_component, keybinder, movement_type, direction_control, direction_control_y=None):
        super().__init__(movement_component, keybinder, movement_type, direction_control, direction_control_y)
        self.tile_geometry = self.movement.tile_geometry

    def process_movement_input(self):
        if self.movement_type == AbstractInputComponent.FOUR_WAY_MOVEMENT:
            if self.direction_control == AbstractInputComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_velocity_in_one_direction_only()
            elif self.direction_control == AbstractInputComponent.DIRECTION_ONLY:
                self._change_absolute_direction()

        elif self.movement_type == AbstractInputComponent.EIGHT_WAY_MOVEMENT:
            if self.direction_control == AbstractInputComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_velocity_x()
            elif self.direction_control == AbstractInputComponent.DIRECTION_ONLY:
                self._change_direction_x()

            if self.direction_control_y == AbstractInputComponent.DIRECTION_AND_MAGNITUDE:
                self._apply_velocity_y()
            elif self.direction_control_y == AbstractInputComponent.DIRECTION_ONLY:
                self._change_direction_y()

            self.movement.ensure_velocity_does_not_exceed_maximum()

    def _apply_velocity_in_one_direction_only(self):
        self.keybinder.track_keys_for_multiple_options("right", "left", "up", "down")
        self.keybinder.update_pressed_keys_order()

        if self.keybinder.is_key_most_recently_pressed_for_option("left"):
            self.movement.velocity.x -= self.keybinder.get_value_for_option("left") * self.tile_geometry.width
            self.movement.velocity.y = 0
        if self.keybinder.is_key_most_recently_pressed_for_option("right"):
            self.movement.velocity.x += self.keybinder.get_value_for_option("right") * self.tile_geometry.width
            self.movement.velocity.y = 0
        if self.keybinder.is_key_most_recently_pressed_for_option("up"):
            self.movement.velocity.y -= self.keybinder.get_value_for_option("up") * self.tile_geometry.height
            self.movement.velocity.x = 0
        if self.keybinder.is_key_most_recently_pressed_for_option("down"):
            self.movement.velocity.y += self.keybinder.get_value_for_option("down") * self.tile_geometry.height
            self.movement.velocity.x = 0

    def _change_absolute_direction(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.movement.constant_velocity_delta.x = -abs(self.movement.default_velocity_delta.x)
            self.movement.constant_velocity_delta.y = 0
            self.movement.velocity.y = 0
        elif self.keybinder.is_key_pressed_for_option("right"):
            self.movement.constant_velocity_delta.x = abs(self.movement.default_velocity_delta.x)
            self.movement.constant_velocity_delta.y = 0
            self.movement.velocity.y = 0
        elif self.keybinder.is_key_pressed_for_option("up"):
            self.movement.constant_velocity_delta.x = 0
            self.movement.constant_velocity_delta.y = -abs(self.movement.default_velocity_delta.y)
            self.movement.velocity.x = 0
        elif self.keybinder.is_key_pressed_for_option("down"):
            self.movement.constant_velocity_delta.x = 0
            self.movement.constant_velocity_delta.y = abs(self.movement.default_velocity_delta.y)
            self.movement.velocity.x = 0

    def _apply_velocity_x(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.movement.velocity.x -= self.keybinder.get_value_for_option("left") * self.tile_geometry.width
        if self.keybinder.is_key_pressed_for_option("right"):
            self.movement.velocity.x += self.keybinder.get_value_for_option("right") * self.tile_geometry.width

    def _change_direction_x(self):
        if self.keybinder.is_key_pressed_for_option("left"):
            self.movement.constant_velocity_delta.x = -abs(self.movement.constant_velocity_delta.x)
        elif self.keybinder.is_key_pressed_for_option("right"):
            self.movement.constant_velocity_delta.x = abs(self.movement.constant_velocity_delta.x)
        self.movement.velocity.x = self.movement.constant_velocity_delta.x

    def _apply_velocity_y(self):
        if self.keybinder.is_key_pressed_for_option("up"):
            self.movement.velocity.y -= self.keybinder.get_value_for_option("up") * self.tile_geometry.height
        if self.keybinder.is_key_pressed_for_option("down"):
            self.movement.velocity.y += self.keybinder.get_value_for_option("down") * self.tile_geometry.height

    def _change_direction_y(self):
        if self.keybinder.is_key_pressed_for_option("up"):
            self.movement.constant_velocity_delta.y = -abs(self.movement.constant_velocity_delta.y)
        elif self.keybinder.is_key_pressed_for_option("down"):
            self.movement.constant_velocity_delta.y = abs(self.movement.constant_velocity_delta.y)
        self.movement.velocity.y = self.movement.constant_velocity_delta.y