from PyQt5 import uic
import sys
import io
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QLabel, QTableWidget, QLineEdit, QSlider, QApplication

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>770</width>
    <height>497</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>PyLizer</string>
  </property>
  <property name="autoFillBackground">
   <bool>false</bool>
  </property>
  <property name="styleSheet">
   <string notr="true"/>
  </property>
  <property name="toolButtonStyle">
   <enum>Qt::ToolButtonFollowStyle</enum>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QWidget" name="horizontalLayoutWidget">
    <property name="geometry">
     <rect>
      <x>170</x>
      <y>80</y>
      <width>501</width>
      <height>151</height>
     </rect>
    </property>
    <layout class="QHBoxLayout" name="SliderLayout">
     <item>
      <widget class="QSlider" name="Slider1">
       <property name="orientation">
        <enum>Qt::Vertical</enum>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QSlider" name="Slider2">
       <property name="orientation">
        <enum>Qt::Vertical</enum>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QSlider" name="Slider3">
       <property name="orientation">
        <enum>Qt::Vertical</enum>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QSlider" name="Slider4">
       <property name="orientation">
        <enum>Qt::Vertical</enum>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QSlider" name="Slider5">
       <property name="orientation">
        <enum>Qt::Vertical</enum>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QSlider" name="Slider6">
       <property name="orientation">
        <enum>Qt::Vertical</enum>
       </property>
      </widget>
     </item>
    </layout>
   </widget>
   <widget class="QSlider" name="VolumeSlider">
    <property name="geometry">
     <rect>
      <x>280</x>
      <y>30</y>
      <width>391</width>
      <height>21</height>
     </rect>
    </property>
    <property name="orientation">
     <enum>Qt::Horizontal</enum>
    </property>
   </widget>
   <widget class="QLabel" name="Volumelabel">
    <property name="geometry">
     <rect>
      <x>40</x>
      <y>20</y>
      <width>201</width>
      <height>41</height>
     </rect>
    </property>
    <property name="sizePolicy">
     <sizepolicy hsizetype="Ignored" vsizetype="Preferred">
      <horstretch>0</horstretch>
      <verstretch>0</verstretch>
     </sizepolicy>
    </property>
    <property name="font">
     <font>
      <pointsize>8</pointsize>
      <weight>75</weight>
      <bold>true</bold>
     </font>
    </property>
    <property name="lineWidth">
     <number>1</number>
    </property>
    <property name="text">
     <string>Усиление звука</string>
    </property>
    <property name="scaledContents">
     <bool>true</bool>
    </property>
   </widget>
   <widget class="QLabel" name="Frequencylabel">
    <property name="geometry">
     <rect>
      <x>670</x>
      <y>230</y>
      <width>91</width>
      <height>41</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>8</pointsize>
      <weight>75</weight>
      <bold>true</bold>
     </font>
    </property>
    <property name="mouseTracking">
     <bool>false</bool>
    </property>
    <property name="tabletTracking">
     <bool>false</bool>
    </property>
    <property name="text">
     <string>Частоты</string>
    </property>
    <property name="wordWrap">
     <bool>true</bool>
    </property>
   </widget>
   <widget class="QPushButton" name="AcceptButton">
    <property name="geometry">
     <rect>
      <x>240</x>
      <y>360</y>
      <width>71</width>
      <height>31</height>
     </rect>
    </property>
    <property name="text">
     <string>Принять</string>
    </property>
   </widget>
   <widget class="QWidget" name="verticalLayoutWidget">
    <property name="geometry">
     <rect>
      <x>590</x>
      <y>300</y>
      <width>151</width>
      <height>131</height>
     </rect>
    </property>
    <layout class="QVBoxLayout" name="ClearSaveLayout">
     <item>
      <widget class="QPushButton" name="ClearButton">
       <property name="text">
        <string>Очистить</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="SaveButton">
       <property name="text">
        <string>Сохранить</string>
       </property>
      </widget>
     </item>
    </layout>
   </widget>
   <widget class="QLabel" name="Presetslabel">
    <property name="geometry">
     <rect>
      <x>70</x>
      <y>250</y>
      <width>101</width>
      <height>51</height>
     </rect>
    </property>
    <property name="font">
     <font>
      <pointsize>8</pointsize>
      <weight>75</weight>
      <bold>true</bold>
     </font>
    </property>
    <property name="text">
     <string>Пресеты</string>
    </property>
   </widget>
   <widget class="QLineEdit" name="VolumeEdit">
    <property name="geometry">
     <rect>
      <x>220</x>
      <y>30</y>
      <width>51</width>
      <height>20</height>
     </rect>
    </property>
   </widget>
   <widget class="QWidget" name="horizontalLayoutWidget_2">
    <property name="geometry">
     <rect>
      <x>190</x>
      <y>240</y>
      <width>461</width>
      <height>21</height>
     </rect>
    </property>
    <layout class="QHBoxLayout" name="ButtonLayout">
     <item>
      <widget class="QLineEdit" name="SliderEdit1"/>
     </item>
     <item>
      <widget class="QLineEdit" name="SliderEdit2"/>
     </item>
     <item>
      <widget class="QLineEdit" name="SliderEdit3"/>
     </item>
     <item>
      <widget class="QLineEdit" name="SliderEdit4"/>
     </item>
     <item>
      <widget class="QLineEdit" name="SliderEdit5"/>
     </item>
     <item>
      <widget class="QLineEdit" name="SliderEdit6"/>
     </item>
    </layout>
   </widget>
   <widget class="QWidget" name="horizontalLayoutWidget_3">
    <property name="geometry">
     <rect>
      <x>300</x>
      <y>290</y>
      <width>211</width>
      <height>31</height>
     </rect>
    </property>
    <layout class="QHBoxLayout" name="PlayStopLayout">
     <item>
      <widget class="QPushButton" name="PlayButton">
       <property name="text">
        <string>Играть</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="StopButton">
       <property name="text">
        <string>Стоп</string>
       </property>
      </widget>
     </item>
    </layout>
   </widget>
   <widget class="QTableWidget" name="TableWidget">
    <property name="geometry">
     <rect>
      <x>20</x>
      <y>290</y>
      <width>201</width>
      <height>171</height>
     </rect>
    </property>
   </widget>
   <widget class="QLabel" name="label">
    <property name="geometry">
     <rect>
      <x>50</x>
      <y>170</y>
      <width>71</width>
      <height>61</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
    <property name="pixmap">
     <pixmap>seagull.jpg</pixmap>
    </property>
    <property name="scaledContents">
     <bool>true</bool>
    </property>
   </widget>
   <widget class="QLabel" name="label_2">
    <property name="geometry">
     <rect>
      <x>50</x>
      <y>80</y>
      <width>71</width>
      <height>71</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
    <property name="pixmap">
     <pixmap>rhomb.jpg</pixmap>
    </property>
    <property name="scaledContents">
     <bool>true</bool>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>770</width>
     <height>18</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
"""

class PyLizer(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)
        self.PlayButton.clicked.connect(lambda: print("a"))
        self.StopButton.clicked.connect(lambda: print("s"))
        self.ClearButton.clicked.connect(lambda: print("a"))
        self.SaveButton.clicked.connect(lambda: print("a"))
        self.AcceptButton.clicked.connect(lambda: print("a"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PyLizer()
    ex.show()
    sys.exit(app.exec_())
