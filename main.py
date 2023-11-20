import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow
from widgets import main_window

import sqlite3
import logging
from pydub import AudioSegment
from pydub.effects import equalize

# yep it does NOT work for now it's just some kind of stub or draft
def get_slider_values():
    """
    Retrieves the slider values from the database.

    Returns:
        dict: A dictionary containing the slider values.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('presets_base.db')
        cursor = conn.cursor()

        # Retrieve slider values from the database
        cursor.execute("SELECT * FROM sliders")
        rows = cursor.fetchall()

        slider_values = {}
        for row in rows:
            slider_name, slider_value = row
            slider_values[slider_name] = slider_value

        # Close the database connection
        conn.close()

        return slider_values
    except Exception as e:
        logging.error(f"Error retrieving slider values: {e}")
        return {}


def save_slider_values(slider_values):
    """
    Saves the slider values to the database.

    Args:
        slider_values (dict): A dictionary containing the slider values.
    """
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('presets_base.db')
        cursor = conn.cursor()

        # Clear the existing slider values in the database
        cursor.execute("DELETE FROM sliders")

        # Save the new slider values to the database
        for slider_name, slider_value in slider_values.items():
            cursor.execute("INSERT INTO sliders VALUES (?, ?)", (slider_name, slider_value))

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(f"Error saving slider values: {e}")


def apply_equalization(audio_file):
    """
    Applies equalization to the given audio file using the slider values.

    Args:
        audio_file (str): The path to the input audio file.
    """
    try:
        # Retrieve slider values from the database
        slider_values = get_slider_values()

        # Load the audio file
        audio = AudioSegment.from_file(audio_file)

        # Apply equalization using the slider values
        equalized_audio = equalize(audio, bands=slider_values)

        # Export the equalized audio to a new file
        equalized_audio.export('output.wav', format='wav')
    except Exception as e:
        logging.error(f"Error applying equalization: {e}")

# Example usage
    # slider_values = {'80Hz': 4, '200Hz': 2, '800Hz': 0, '2kHz': -2, '5kHz': -4, '12kHz': -6}
    # save_slider_values(slider_values)
    # apply_equalization('input.wav')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.show()
    sys.exit(app.exec_())
