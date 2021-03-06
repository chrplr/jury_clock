#! /usr/bin/env python
# Time-stamp: <2019-03-05 12:08:10 christophe@pallier.org>


""" An application that shows the expected time of completion of a series of evaluation.  """

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
        self.pack()
        self.ntotal = n_events
        self.current = 1
        self.remaining = n_events - 1
        self.remaining_time = interval * n_events
        self.t0 = time.time()
        self.t1 = self.t0
        self.target_interval = interval
        self.interval = interval
        self.interval_avg = interval
        self.remaining_time_avg = self.remaining_time
        self.pause_durations = 0  # not implemented yet TODO

        self.customFont = font.Font(root, ("courier new", 40, "bold"))
        self.create_widgets()
        self.update()

    def create_widgets(self):
        self.w_current = tk.Label(self, font=self.customFont)
        self.w_current.pack(side="top")

        self.w_current_time = tk.Label(self, font=self.customFont)
        self.w_current_time.pack(side='top')

        self.w_start_clock = tk.Label(self, font=self.customFont)
        self.w_start_clock.pack()

        self.w_interval_target = tk.Label(self, font=self.customFont)
        self.w_interval_target.pack()

        self.w_interval =  tk.Label(self, font=self.customFont)
        self.w_interval.pack(side="top")

        self.w_interval_avg = tk.Label(self, font=self.customFont)
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

    def update(self):
        self.w_current["text"] = "Current Project #{:d}/{:d} ({:d})".format(self.current,
                                                                    self.ntotal,
                                                                    self.remaining)
        # update displayed time
        self.w_current_time["text"] = "Project Start Time {} ({})".format(pretty_format_timestamp(self.t1),
                                                                          pretty_format_duration(time.time() - self.t1))
        # schedule timer to call myself after 1 second

        self.w_start_clock["text"] = "Session Start Time {} ({})".format(pretty_format_timestamp(self.t0),
                                                                         pretty_format_duration(time.time() - self.t0 - self.pause_durations))

        self.w_interval_target["text"] = "Target interval={} ETA={} ({})".format(pretty_format_duration(self.target_interval * 60),
                                                                                 pretty_format_timestamp(self.t1 + self.target_interval * (1 + self.remaining) * 60),
                                                                                 pretty_format_duration(self.target_interval * (1 + self.remaining) * 60))

        self.w_interval["text"] = "Last interval={} ETA={} ({})".format(pretty_format_duration(self.interval * 60),
                                                                        pretty_format_timestamp(self.t1 + self.interval * (1 + self.remaining) * 60),
                                                                        pretty_format_duration(self.interval * (1 + self.remaining) * 60))
        self.w_interval_avg["text"] = " Avg interval={} ETA={} ({})".format(pretty_format_duration(self.interval_avg * 60),
                                                                            pretty_format_timestamp(self.t1 + self.interval_avg * (1 + self.remaining) * 60),
                                                                            pretty_format_duration(self.interval_avg * (1 + self.remaining) * 60))

        self.after(1000, self.update)

    def inc(self):
        prev_time = self.t1
        self.t1 = time.time()
        self.current += 1
        self.remaining = self.ntotal - self.current
        self.interval = (self.t1 - prev_time) / 60
        self.interval_avg = (self.t1 - self.t0) / (self.current - 1) / 60
        self.update()


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
