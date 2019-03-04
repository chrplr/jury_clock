#! /usr/bin/env python
# Time-stamp: <2019-03-04 15:34:24 christophe@pallier.org>


""" An application that shows the expected time of completion of a series of of evaluation.  """

import time
import sys
import argparse
from datetime import datetime

import tkinter as tk
from tkinter import font

def pretty_format_duration(seconds):
    """ return a duration in seconds as a string with a format h:m:s """
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    periods = [('h', hours), ('m', minutes), ('s', seconds)]
    return ':'.join('{:.0f}{}'.format(value, name) for name, value in periods if value)


def pretty_format_timestamp(timestamp):
    """ converts a timestamp (seconds elapsed since epoch) into a string HH:MM """
    return datetime.fromtimestamp(int(timestamp)).strftime("%H:%M")


class Application(tk.Frame):
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        # super().__init__(master)
        self.pack()
        #self.customFont = "-size 40"

        self.customFont = font.Font(root, ("courier new", 40, "bold"))
        self.create_widgets()

    def create_widgets(self):

        self.n = n_events
        self.current = 1
        self.remaining = n_events - 1
        self.remaining_time = interval * n_events

        self.t0 = time.time()
        self.t1 = self.t0

        self.w_clock = tk.Label(self, font=self.customFont)
        self.w_clock["text"] = "Starting Time {}".format(pretty_format_timestamp(self.t0))
        self.w_clock.pack()

        self.w_current = tk.Label(self, font=self.customFont)
        self.w_current["text"] = "Current {:d}/{:d} ({:d}) @ {}".format(self.current,
                                                                        self.n,
                                                                        self.remaining,
                                                                        pretty_format_timestamp(self.t1))
        self.w_current.pack(side="top")

        self.interval = interval
        self.w_interval =  tk.Label(self, font=self.customFont)
        self.w_interval["text"] = "---"
        self.w_interval.pack(side="top")

        self.interval_avg = interval
        self.remaining_time_avg = self.remaining_time
        self.w_interval_avg = tk.Label(self, font=self.customFont)
        self.w_interval_avg["text"] = "Average interval: {} ETA: {}".format(pretty_format_duration(self.interval_avg * 60),
                                                                            pretty_format_duration(self.remaining_time_avg * 60))
        self.w_interval_avg.pack(side="top")

        self.event = tk.Button(self, text="NEXT", fg="red", font=self.customFont, 
                               command=self.inc)
        self.event.pack(side="top")

        # self.pause = tk.Button(self, text="PAUSE", fg="red", font=self.customFont, 
        #                        command=self.pause)
        # self.pause.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",  font=self.customFont,
                              command=root.destroy)
        self.quit.pack(side="bottom")


    def pause(self):
        None  # TODO

    def inc(self):

        prev_time = self.t1
        self.t1 = time.time()

        self.current += 1
        self.remaining = self.n - self.current

        self.interval = (self.t1 - prev_time) / 60
        self.remaining_time = (self.interval * (1 + self.remaining))

        self.interval_avg = (self.t1 - self.t0) / (self.current - 1) / 60
        self.remaining_time_avg = self.interval_avg * (1 + self.remaining)

        if self.current <= self.n:
            self.w_clock["text"] = "Start Time {} ({})".format(pretty_format_timestamp(self.t0),
                                                               pretty_format_duration(self.t1 - self.t0))
            self.w_current["text"] = "Current file {:d}/{:d} ({:d}) @ {}".format(self.current,
                                                                                 self.n,
                                                                                 self.remaining,
                                                                                 pretty_format_timestamp(self.t1))
            self.w_interval["text"] = "Last interval={} ETA={} ({})".format(pretty_format_duration(self.interval * 60),
                                                                                   pretty_format_timestamp(self.t1 + self.remaining_time * 60),
                                                                                   pretty_format_duration(self.remaining_time * 60))
            self.w_interval_avg["text"] = " Avg interval={} ETA={} ({})".format(pretty_format_duration(self.interval_avg * 60),
                                                                                        pretty_format_timestamp(self.t1 + self.remaining_time_avg * 60),
                                                                                        pretty_format_duration(self.remaining_time_avg * 60))
        else:
            self.w_current["text"] = "{:d}/{:d}".format(self.n, self.n)
            self.w_interval["text"] = "Finished in " + pretty_format_duration(self.t1 - self.t0)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--nprojects", type=int, required=True)
    args.add_argument("--interval", help="target interval in minutes", type=int,
                      required=True)
    x = args.parse_args()

    n_events = x.nprojects
    interval = x.interval

    root = tk.Tk()

    app = Application(root)
    app.mainloop()
