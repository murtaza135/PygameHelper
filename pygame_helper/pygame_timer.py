import pygame
import exceptions


class PygameTimer(object):
    
    def __init__(self, delay_seconds):
        if not pygame.display.get_init():
            raise exceptions.PygameInitError
        
        self.time_started_seconds = None
        self.delay_seconds = None
        self.set_new_delay(delay_seconds)

    def set_new_delay(self, delay_seconds):
        if delay_seconds <= 0:
            raise ValueError("Must provide a valid delay time (in seconds)")

        self.delay_seconds = float(delay_seconds)

    def is_running(self):
        return not self.is_completed()

    def is_completed(self):
        return (
            self.time_started_seconds is None
            or self.time_started_seconds + self.delay_seconds <= self.get_current_time()
        )

    def get_current_time(self):
        return float(pygame.time.get_ticks() / 1000)

    def get_time_remaining(self):
        if self.time_started_seconds is None:
            return float(0)

        time_remaining_seconds = (self.time_started_seconds + self.delay_seconds) - self.get_current_time()
        if time_remaining_seconds < 0:
            time_remaining_seconds = 0
        return time_remaining_seconds

    def reset(self):
        self.time_started_seconds = self.get_current_time()

    def __repr__(self):
        return f"Timer(delay_seconds={self.delay_seconds})"

    def __str__(self):
        time_remaining = round(self.get_time_remaining(), 5)
        return f"Time remaining: {time_remaining} seconds"

    def __setattr__(self, name, time_seconds):
        if time_seconds is not None and time_seconds <= 0:
            raise ValueError("Must provide a valid delay time (in seconds)")

        super().__setattr__(name, time_seconds)

    def __delattr__(self, name):
        raise exceptions.DeleteError("Cannot delete attribute")