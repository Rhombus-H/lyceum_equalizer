import sqlite3
import sys

import test_qrc  # resource for a picture
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QColorDialog
from widgets import main_window, equalize

import sqlite3
import logging
from pydub import AudioSegment
from pydub import effects


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("static/main_window.ui", self)
        self.initUI()

    def initUI(self):
        self.change_color_button.clicked.connect(self.change_color_of_buttons)

    def change_color_of_buttons(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.change_color_button.setStyleSheet(
                "background-color: {}".format(color.name()))
            self.pushButton.setStyleSheet(
                "background-color: {}".format(color.name()))
            self.accept_button.setStyleSheet(
                "background-color: {}".format(color.name()))


    def get_slider_values_from_ui(self):
        """
        Retrieves the values of the sliders from the UI and returns them as a dictionary.

        Returns:
            slider_values (dict): A dictionary containing the names of the sliders as keys and their corresponding values as values.
        """
        slider_values = {}
        for i in range(6):
            slider_name = f"slider_{i + 1}"
            slider_value = getattr(self, slider_name).value()
            slider_values[slider_name] = slider_value
        return slider_values

    def get_slider_values_from_db(self, preset):
        """
        Retrieves the slider values from the database for a given preset.

        Parameters:
            preset (str): The name of the preset.

        Returns:
            list: A list of slider values retrieved from the database.
        """
        cursor = self.connection.cursor('presets_base.db')
        cursor.execute('SELECT freqency_1, freqency_2, freqency_3, freqency_4, freqency_5, freqency_6 FROM ?', (preset,))
        slider_values = cursor.fetchall()
        return slider_values

    def get_preamp_value_from_ui(self):
        """
        Returns the value of the preamp slider from the user interface.

        :return: The value of the preamp slider.
        """
        return self.preamp_slider.value()

    def get_preamp_value_from_db(self, preset):
        """
        Retrieves the preamp value associated with a given preset from the 'presets_base.db' database.

        Args:
            preset (str): The name of the preset.

        Returns:
            list: A list containing the preamp value(s) associated with the preset.
        """
        cursor = self.connection.cursor('presets_base.db')
        cursor.execute('SELECT preamp FROM ?', (preset,))
        preamp_value = cursor.fetchall()
        return preamp_value

    def set_slider_values(self, preset):
        """
        Sets the values of sliders based on the given preset.

        Parameters:
            preset (str): The name of the preset.

        Returns:
            None
        """
        slider_values = self.get_slider_values_from_db(preset)
        for i in range(6):
            slider_name = f"slider_{i + 1}"
            slider_value = slider_values[i]
            setattr(self, slider_name, slider_value)

    def set_preamp_value(self, preset):
        """
        Set the value of the preamp slider based on the given preset.

        Parameters:
            preset (str): The name of the preset to set the preamp value for.

        Returns:
            None
        """
        value = self.get_preamp_value_from_db(preset)
        self.preamp_slider.setValue(value)

    def create_preset(self):
        pass



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
