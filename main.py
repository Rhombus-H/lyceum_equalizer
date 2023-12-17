import os
import sqlite3
import sys
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtCore import QByteArray, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QInputDialog, QListWidgetItem, \
    QFileDialog
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from pydub import AudioSegment
from pydub.generators import Sine

from transliterate import translit


class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path = Path()
        uic.loadUi("static/main_window.ui", self)
        self.initUI()

        self.player = QMediaPlayer()
        self.content = QMediaContent()

    def initUI(self):
        self.preset_delete_button.clicked.connect(self.delete_preset_button_clicked)
        self.preset_add_button.clicked.connect(self.add_preset_button_clicked)

        self.set_presets_list()
        self.load_track_button.clicked.connect(self.add_audio_button_clicked)
        self.preset_apply_button.clicked.connect(self.apply_preset_button_clicked)

        self.play_track_button.clicked.connect(self.play_audio_button_clicked)
        self.pause_track_button.clicked.connect(self.pause_audio)

    def set_presets_list(self):
        """
        Set the presets list.

        Retrieves the names of presets from the 'presets' table in the 'presets_base.db' database.
        Each name is added as a QListWidgetItem to the 'presets_list' QListWidget.

        Parameters:
            None

        Returns:
            None
        """
        cursor = sqlite3.connect('presets_base.db').cursor()
        cursor.execute('SELECT name FROM presets')
        names = cursor.fetchall()
        for name in names:
            QListWidgetItem(name[0], self.presets_list)

    def add_preset_button_clicked(self):
        """
        Function comment for add_preset_button_clicked.

        Function is called when preset_add_button is clicked. It opens a dialog box to get the name of the preset. 
        Then it adds it to the database if it doesn't exist, othewise - returns sqlite3 exception

        Parameters:
        - self: The instance of the class that this method belongs to.

        Returns:
        - None
        """
        index = self.presets_list.currentRow()
        preset_name, ok = QInputDialog.getText(self, "Новый пресет", "Название пресета")
        try:
            if preset_name and ok:
                self.create_preset(preset_name)
                self.presets_list.insertItem(index, preset_name)
        except sqlite3.OperationalError:
            # self.preset_name_field.setplaceholderText("Такой пресет уже существует.")
            pass

    def play_audio_button_clicked(self):
        if self.path:
            return self.play_audio()
        pass

    def apply_preset_button_clicked(self):
        """
        Click event handler for the "Apply Preset" button.
        Sets the values of the volume amplification and frequency sliders based on the selected preset.
        Parameters:
            None

        Returns:
            None
        """
        index = self.presets_list.currentRow()
        if index == -1:
            return QMessageBox.information(
                self,
                "Пресет не выбран",
                "Вы не выбрали пресет"
            )
        preset_name = self.presets_list.item(index).text()
        self.set_slider_values(preset_name)
        self.set_preamp_value(preset_name)

    def add_audio_button_clicked(self):
        file, ok = QFileDialog.getOpenFileName(
            self,
            'Выберите аудиофайл',
            'C:\\',
            'Аудиофайлы (*.mp3 *.wav *.ogg *.wma)'
        )
        if file and ok:
            path = Path(file)
            self.load_track_button.text = 'Файл загружен'
            self.path = path
            self.load_track_button.setText(f'Загружен файл {self.path.name}')
            return path
        return

    def delete_preset_button_clicked(self):
        """
        Deletes the selected preset on click.

        This function is triggered when the delete preset button is clicked. It retrieves the index of the selected preset from the presets list and obtains the corresponding preset name. If the presets list is empty, an error message is displayed. Otherwise, the function calls the `delete_preset` method passing the preset name as an argument. If the preset name is `None`, the function returns without further actions.

        After the `delete_preset` method is called, a confirmation message box is shown to the user, asking if they want to delete the preset. If the user clicks "Yes", the function removes the item from the presets list.

        Parameters:
            self (QWidget): The reference to the current instance of the class.

        Returns:
            None
        """
        index = self.presets_list.currentRow()
        if index == -1:
            return QMessageBox.information(
                self,
                "Пресет не выбран",
                "Вы не выбрали пресет"
            )
        preset_name = self.presets_list.item(index).text()
        if not self.presets_list.count():
            alert = QMessageBox.about(self, "Ошибка", "")
        else:
            self.delete_preset(str(preset_name))
            if preset_name is None:
                return

            question = QMessageBox.question(self, "Удаление пресета",
                                            "Вы хотите удалить пресет " + str(preset_name) + '?',
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
        for i in range(10):
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
        cursor.execute('''SELECT frequency_1, frequency_2, frequency_3, frequency_4, frequency_5, 
        frequency_6, frequency_7, frequency_8, frequency_9, frequency_10 WHERE name=?''', (preset,))
        slider_values = cursor.fetchall()
        return slider_values

    def get_preamp_value_from_ui(self):
        """
        Returns the value of the preamp slider from the user interface.

        :return: The value of the preamp slider.
        """
        return getattr(self, 'preamp_slider').value()

    def get_preamp_value_from_db(self, preset):
        """
        Retrieves the preamp value associated with a given preset from the 'presets_base.db' database.

        Args:
            preset (str): The name of the preset.

        Returns:
            list: A list containing the preamp value(s) associated with the preset.
        """
        cursor = sqlite3.connect('presets_base.db').cursor()
        cursor.execute('SELECT preamp WHERE name=?', (preset,))
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
        for i in range(10):
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
        data = self.get_slider_values_from_ui() | {'preamp': self.get_preamp_value_from_ui()}
        data = list(data.values())
        connection = sqlite3.connect('presets_base.db')
        cursor = connection.cursor()
        cursor.execute('SELECT name FROM presets WHERE name=?', (preset_name,))
        if cursor.fetchall():
            return sqlite3.OperationalError
        else:
            query = f'''INSERT INTO presets 
            VALUES ({', '.join([f"'{preset_name}'", str(data['slider_1']), str(data['slider_2']), str(data['slider_3']),
                                str(data['slider_4']), str(data['slider_5']), str(data['slider_6']), str(data['slider_7']),
                                str(data['slider_8']), str(data['slider_8']), str(data['slider_8'])])})'''
            cursor.execute(query)
            connection.commit()
            cursor.close()

    def delete_preset(self, preset_name):
        connection = sqlite3.connect('presets_base.db')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM presets WHERE name=?', (preset_name,))
        connection.commit()
        cursor.close()

    def play_audio(self):
        data = self.get_slider_values_from_ui().values()
        frequencies = [10, 21, 42, 83, 166, 333, 577, 1000, 2000, 4000]
        frequency_values = {i: j for i, j in zip(frequencies, data)}
        # Read the audio file
        # Read the audio file using pydub
        audio = AudioSegment.from_file(str(self.path))

        # Create a silence audio segment with the same duration as the original audio
        silence = AudioSegment.silent(duration=len(audio))

        # Apply equalization by adding sine waves to the silence audio segment
        for frequency, value in frequency_values.items():
            sine_wave = Sine(frequency).to_audio_segment(duration=len(audio))
            equalized_segment = sine_wave.apply_gain(value)
            silence = silence.overlay(equalized_segment)

        # Mix the original audio with the equalized audio
        audio = audio.overlay(silence)
        audio = audio + self.get_preamp_value_from_ui()

        # Save the equalized audio file
        audio.export(self.path.name, format='mp3')
        self.content = QMediaContent(QUrl.fromLocalFile(os.path.abspath(self.path.name)))
        self.player.setMedia(self.content)
        self.player.play()

    def pause_audio(self):
        self.player.pause()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.exit(app.exec_())
