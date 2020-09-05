from movement_component import MovementComponent
from rotator2 import Rotator2


class AccelerationMovementComponent(MovementComponent):

    def __init__(self, parent, rect, constant_acceleration_delta, friction, default_position=(0, 0), 
                default_rotation=Rotator2.RIGHT, default_velocity=(0, 0), default_acceleration=(0, 0),
                window_size=(800, 600), after_bounce_velocity_ratios=(0, 0, 0, 0), should_wrap_screen=(True, True)):

        super().__init__(parent, rect, constant_acceleration_delta, friction, default_position=(0, 0), 
                        default_rotation=Rotator2.RIGHT, default_velocity=(0, 0), default_acceleration=(0, 0),
                        window_size=(800, 600), after_bounce_velocity_ratios=(0, 0, 0, 0), should_wrap_screen=(True, True))
        