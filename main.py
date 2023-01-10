#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import sys
import requests

# try which gir is available prioritising Gtk3
try:
    from gi.repository import AyatanaAppIndicator3 as AppIndicator
except ImportError:
    try:
        from gi.repository import AppIndicator3 as AppIndicator
    except ImportError:
        from gi.repository import AppIndicator
from gi.repository import Gtk, GLib
from datetime import datetime

REGION = "SE3"
SEK = "SEK_per_kWh"
BASE_URL = "https://www.elprisetjustnu.se/api/v1/prices"


class SwedishPowerIndicator:

    def __init__(self):
        self.indicator = AppIndicator.Indicator.new(
            "eldata-se-powercost-indicator",
            "calendar-tray",
            AppIndicator.IndicatorCategory.OTHER,
        )
        self.indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
        self.menu_setup()
        self.indicator.set_menu(self.menu)

    def menu_setup(self):
        self.menu = Gtk.Menu()
        self.to_bs_menu = Gtk.MenuItem(label="Refresh data")
        self.to_bs_menu.connect("activate", self.refresh_data)
        self.to_bs_menu.show()

        self.quit_item = Gtk.MenuItem(label="Exit")
        self.quit_item.connect("activate", self.quit)
        self.quit_item.show()

    def refresh_data(self, widget=None):
        self.indicator.set_label(f"Refreshing data...", "")

        day_price = self.get_day_price()
        month_price = self.query_month_price()

        self.indicator.set_label(f"{day_price}  {month_price}", "")

        # Auto update once an hour
        GLib.timeout_add_seconds(60 * 60, self.refresh_data)

    def set_date_label(self):
        self.indicator.set_label("ERROR...", "")
        return True

    def calculate_average(self, numbers):
        total = 0
        count = 0

        for number in numbers:
            total += number
            count += 1

        return round(total / count, 3)

    def query_month_price(self):
        ll = []

        # Figure out how many days in a month we shold query
        today = datetime.now()
        num_days = 32

        for counter in range(1, num_days):
            try:
                print(counter)
                c = "{:02d}".format(counter)
                r = requests.get(f"{BASE_URL}/{today.year}/{today.month:02d}-{c}_{REGION}.json")
                l = [
                    float(hour_data[SEK])
                    for hour_data in r.json()
                ]
                ll += l
            except Exception as e:
                break

        return f"M: {self.calculate_average(ll)}:-"

    def get_day_price(self):
        # Format the day of the month with two digits
        today = datetime.now()
        day_of_month = today.strftime("%d")

        r = requests.get(f"{BASE_URL}/{today.year}/{today.month:02d}-{day_of_month}_{REGION}.json")
        try:
            data = r.json()
        except Exception:
            print("ERROR", r.content)

        l = []

        for index, hour_data in enumerate(data):
            l.append(float(hour_data[SEK]))

        return f"D: {self.calculate_average(l)}:-"

    def main(self):
        self.indicator.set_label(f"...", "")

        GLib.timeout_add_seconds(2, self.refresh_data)

        self.menu.append(self.to_bs_menu)
        self.menu.append(self.quit_item)

        Gtk.main()

    def quit(self, widget):
        widget.destroy()
        sys.exit(0)


if __name__ == "__main__":
    SwedishPowerIndicator().main()
