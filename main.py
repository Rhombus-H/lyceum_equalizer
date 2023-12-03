import sqlite3
import sys

import test_qrc  # resource for a picture
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog

import sqlite3
import logging
from pydub import AudioSegment
from pydub import effects
from transliterate import translit


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("static/main_window.ui", self)
        self.initUI()

    def initUI(self):
        self.change_color_button.clicked.connect(self.change_color_of_buttons)
        self.preset_delete_button.clicked.connect(self.delete_preset_button_clicked)
        self.preset_add_button.clicked.connect(self.add_preset_button_clicked)

    def add_preset_button_clicked(self):
        index = self.presets_list.currentRow()
        preset_name, ok = QInputDialog.getText(self, "Новый пресет", "Название пресета")
        try:
            self.create_preset(preset_name)
        except sqlite3.OperationalError:
            # self.preset_name_field.setplaceholderText("Такой пресет уже существует.")
            pass
        if preset_name and ok:
            self.presets_list.insertItem(index, preset_name)

    def delete_preset_button_clicked(self):
        index = self.presets_list.currentRow()
        preset_name = self.presets_list.item(index)
        if not self.presets_list.count():
            alert = QMessageBox.about(self, "Ошибка", "")
        else:
            self.delete_preset(str(preset_name))
            if preset_name is None:
                return

            question = QMessageBox.question(self, "Удаление пресета",
            "Вы хотите удалить пресет " + preset_name.text() + '?',
                                        QMessageBox.Yes | QMessageBox.No)

            if question == QMessageBox.Yes:
                item = self.presets_list.takeItem(index)
                del item
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
        cursor = sqlite3.connect('presets_base.db').cursor()
        cursor.execute('SELECT frequency_1, frequency_2, frequency_3, frequency_4, frequency_5, frequency_6 FROM ?', (preset,))
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
        cursor = sqlite3.connect('presets_base.db').cursor()
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

    def format_preset_name(self, ru_preset_name):
        """
        Format the given preset name into database-allowed format.

        Args:
            ru_preset_name (str): The Russian preset name to be formatted.

        Returns:
            str: The formatted preset name in uppercase with underscores.
        """
        return '_'.join(translit(ru_preset_name, 'ru', reversed=True).split()).upper()

    def create_preset(self, preset_name):
        data = self.get_slider_values_from_ui() | {'preamp': self.get_preamp_value_from_ui}
        cursor = sqlite3.connect('presets_base.db').cursor()
        cursor.execute('SELECT name FROM presets_base WHERE name=?', (self, preset_name))
        if cursor.fetchall():
            return sqlite3.OperationalError
        else:
            cursor.execute(f'INSERT INTO presets VALUES ({format(tuple(data.values()))})')
            cursor.fetchall()

    def delete_preset(self, preset_name):
        cursor = sqlite3.connect('presets_base.db').cursor()
        cursor.execute('DELETE FROM presets WHERE name=?', (preset_name,))
        cursor.fetchall()

    def apply_preset(self):
        self.set_preamp_value
        self.set_slider_values


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
