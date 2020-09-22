import pygame
import pygame_helper.exceptions as exceptions


class Timer(object):
    
    def __init__(self, countdown, auto_start=False, set_timer_to_completed_when_reset=True):
        if not pygame.display.get_init():
            raise exceptions.PygameInitError
        
        self._time_started_seconds = None
        self._countdown = None
        self.countdown = countdown
        self._is_timer_completed_when_reset = set_timer_to_completed_when_reset
        self._is_reset_called = True

        if auto_start:
            self._start_new_timer()


    def _start_new_timer(self):
        self._time_started_seconds = self._current_time
        self._is_reset_called = False

    def start(self):
        if self._time_started_seconds is None or self.is_completed():
            self._start_new_timer()

    def restart(self):
        self._start_new_timer()

    def reset(self):
        self._time_started_seconds = None
        self._is_reset_called = True


    def is_running(self):
        return not self.is_completed()

    def is_completed(self):
        if self._is_reset_called:
            return self._is_timer_completed_when_reset
        else:
            return self._time_started_seconds + self._countdown <= self._current_time


    @property
    def _current_time(self):
        return float(pygame.time.get_ticks()) / 1000

    @property
    def time_remaining(self):
        if self._time_started_seconds is None:
            return float(0)

        time_remaining_seconds = (self._time_started_seconds + self._countdown) - self._current_time
        if time_remaining_seconds < 0:
            time_remaining_seconds = 0
        return time_remaining_seconds

    @property
    def countdown(self):
        return self._countdown

    @countdown.setter
    def countdown(self, countdown):
        if countdown < 0:
            raise ValueError("Must provide a valid countdown time (in seconds)")
        self._countdown = float(countdown)


    def __repr__(self):
        return f"Timer(countdown={self._countdown}, set_timer_to_completed_when_reset={self._is_timer_completed_when_reset})"

    def __str__(self):
        time_remaining_seconds = round(self.time_remaining, 5)
        return f"Time remaining: {time_remaining_seconds} seconds"