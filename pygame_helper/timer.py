import pygame
import pygame_helper.exceptions as exceptions


class Timer(object):
    
    def __init__(self, countdown):
        if not pygame.display.get_init():
            raise exceptions.PygameInitError
        
        self._time_started_seconds = None
        self._countdown = None
        self.set_new_delay(countdown)

    def set_new_delay(self, countdown):
        if countdown <= 0:
            raise ValueError("Must provide a valid delay time (in seconds)")

        self._countdown = float(countdown)

    def _start_new_timer(self):
        self._time_started_seconds = self.get_current_time()

    def start(self):
        if self.is_completed():
            self._start_new_timer()

    def reset(self):
        if self.is_completed():
            self._start_new_timer()

    def force_reset(self):
        self._start_new_timer()

    def is_running(self):
        return not self.is_completed()

    def is_completed(self):
        return (
            self._time_started_seconds is None
            or self._time_started_seconds + self._countdown <= self.get_current_time()
        )

    def get_current_time(self):
        return float(pygame.time.get_ticks() / 1000)

    def get_time_remaining(self):
        if self._time_started_seconds is None:
            return float(0)

        time_remaining_seconds = (self._time_started_seconds + self._countdown) - self.get_current_time()
        if time_remaining_seconds < 0:
            time_remaining_seconds = 0
        return time_remaining_seconds

    def __repr__(self):
        return f"Timer(countdown={self._countdown})"

    def __str__(self):
        time_remaining = round(self.get_time_remaining(), 5)
        return f"Time remaining: {time_remaining} seconds"

    def __setattr__(self, name, time_seconds):
        if time_seconds is not None and time_seconds < 0:
            raise ValueError("Must provide a valid delay time (in seconds)")

        super().__setattr__(name, time_seconds)

    def __delattr__(self, name):
        raise exceptions.DeleteError("Cannot delete attribute")