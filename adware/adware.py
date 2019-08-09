#!/usr/bin/env python3

""" Implementation of simple adware that pops multiple
windows with the advertisements.
"""

import logging
import sys
import random

from PySide2.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout


class AdWindow(QDialog):
    """ This class represents ad window shown on the screen. """

    def __init__(self, ad_slogan, parent=None):
        super(AdWindow, self).__init__(parent)
        self.setWindowTitle("Advertisement!")

        # Create a layout so that the ad slogan is shown.
        self.label = QLabel(ad_slogan)
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        self.setLayout(layout)

    def closeEvent(self, event):
        # Ignore the close event so that the ad
        # can't be closed by pressing close button.
        event.ignore()


class Adware(QApplication):
    """ This class represents implementation of adware. """

    def __init__(self, args):
        super(Adware, self).__init__(args)

    @property
    def advert_slogans(self):
        """ Slogans of the promoted adds. """
        return (
            'Buy the milk in the milk shops!',
            'Buy the clothes in the wool shops!',
            'Buy the food in the food shops!'
        )

    def create_ad_window(self, ad_slogan):
        """ Creates a windows showing the advertisement
        slogan.

        :param str ad_slogan: Text of the ad.
        """
        window = AdWindow(ad_slogan=ad_slogan)
        window.show()
        return window

    def show_ads(self):
        """ Creates the main GUI application and shows
        the ads based on `:class:~Adware.advert_slogans`
        """
        ad_windows = []
        for advert in self.advert_slogans:
            # Create a new ad window.
            ad_window = self.create_ad_window(advert)
            # Move this window to random location on screen.
            x_coordinate, y_coordinate = random.randint(1, 800), random.randint(1, 600)
            ad_window.move(x_coordinate, y_coordinate)
            ad_windows.append(ad_window)

        return ad_windows


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    # Create our adware and show the ads.
    adware = Adware(sys.argv)
    windows = adware.show_ads()

    sys.exit(adware.exec_())
