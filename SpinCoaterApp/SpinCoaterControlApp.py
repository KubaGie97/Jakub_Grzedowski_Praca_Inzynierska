import serial
import serial.tools.list_ports
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox
)
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import QTimer

import pyqtgraph as pg
import time

import csv
from PyQt5.QtWidgets import QFileDialog
from datetime import datetime


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.ser = None

        self.start_time = time.time()

        self.time_data = []
        self.rpm_data = []
        self.pwm_data = []

        self.current_rpm = 0
        self.current_pwm = 0
        self.rpm_target = 0

        self.csv_file = None
        self.csv_write = None
        self.logging_active = False

        self.serial_timer = QTimer()

        self.serial_timer.timeout.connect(
            self.read_serial
        )

        self.serial_timer.start(100)

        self.setWindowTitle("Spin Coater Control")
        self.resize(1400, 800)

        # ===== COM =====

        self.com_label = QLabel("Port COM")

        self.com_box = QComboBox()
        self.refresh_ports()

        self.refresh_button = QPushButton("Odśwież")
        self.connect_button = QPushButton("Połącz")

        self.disconnect_button = QPushButton("Rozłącz")
        self.disconnect_button.clicked.connect(
            self.disconnect_serial
        )

        # ===== RPM =====

        self.rpm_label = QLabel("RPM Target")

        self.rpm_input = QLineEdit()
        self.rpm_input.setValidator(QIntValidator(0, 10000))

        self.rpm_button = QPushButton("Wyślij RPM")
        self.rpm_button.clicked.connect(self.send_rpm)

        # ===== PWM =====

        self.pwm_label = QLabel("PWM Target")

        self.pwm_input = QLineEdit()
        self.pwm_input.setValidator(QIntValidator(0, 255))

        self.pwm_button = QPushButton("Wyślij PWM")
        self.pwm_button.clicked.connect(self.send_pwm)

        # ===== STATUS =====

        self.status_label = QLabel("Status: Nie połączono")

        self.rpm_actual = QLabel("RPM aktualne: 0")
        self.pwm_actual = QLabel("PWM aktualne: 0")

        # ===== STOP =====

        self.stop_button = QPushButton("STOP")
        self.stop_button.clicked.connect(self.stop_motor)
        self.refresh_button.clicked.connect(
            self.refresh_ports
        )

        self.connect_button.clicked.connect(
            self.connect_serial
        )

        # ===== Zapisywanie do CSV =====

        self.start_log_button = QPushButton("START POMIARU")
        self.start_log_button.clicked.connect(
            self.start_logging
        )

        self.stop_log_button = QPushButton("STOP POMIARU")
        self.stop_log_button.clicked.connect(
            self.stop_logging
        )

        # ===== LAYOUT =====

        # ===== WYKRES RPM =====

        self.rpm_plot = pg.PlotWidget()

        self.rpm_plot.setTitle(
            "RPM w funkcji czasu"
        )

        self.rpm_plot.setLabel(
            "left",
            "RPM"
        )

        self.rpm_plot.setLabel(
            "bottom",
            "Czas [s]"
        )

        self.rpm_plot.showGrid(
            x=True,
            y=True
        )

        self.rpm_plot.setYRange(0,6500)

        self.rpm_curve = self.rpm_plot.plot(
            pen='b'
        )

        # ===== WYKRES PWM =====

        self.pwm_plot = pg.PlotWidget()

        self.pwm_plot.setTitle(
            "PWM w funkcji czasu"
        )

        self.pwm_plot.setLabel(
            "left",
            "PWM"
        )

        self.pwm_plot.setLabel(
            "bottom",
            "Czas [s]"
        )

        self.pwm_plot.showGrid(
            x=True,
            y=True
        )

        self.pwm_curve = self.pwm_plot.plot(
            pen='r'
        )

        self.pwm_plot.setYRange(
            0,
            255
        )

        # ===== PANEL STEROWANIA =====

        left_panel = QVBoxLayout()

        com_layout = QHBoxLayout()
        com_layout.addWidget(self.com_label)
        com_layout.addWidget(self.com_box)
        com_layout.addWidget(self.refresh_button)
        com_layout.addWidget(self.connect_button)
        com_layout.addWidget(self.disconnect_button)

        left_panel.addLayout(com_layout)

        left_panel.addSpacing(15)

        left_panel.addWidget(self.rpm_label)
        left_panel.addWidget(self.rpm_input)
        left_panel.addWidget(self.rpm_button)

        left_panel.addSpacing(15)

        left_panel.addWidget(self.pwm_label)
        left_panel.addWidget(self.pwm_input)
        left_panel.addWidget(self.pwm_button)

        left_panel.addSpacing(20)

        left_panel.addWidget(self.rpm_actual)
        left_panel.addWidget(self.pwm_actual)
        left_panel.addWidget(self.status_label)

        left_panel.addSpacing(20)

        left_panel.addWidget(self.stop_button)

        left_panel.addSpacing(20)

        left_panel.addWidget(
            self.start_log_button
        )

        left_panel.addWidget(
            self.stop_log_button
        )

        left_panel.addStretch()

        right_panel = QVBoxLayout()

        right_panel.addWidget(
            self.rpm_plot
        )

        right_panel.addWidget(
            self.pwm_plot
        )

        # ===== UKŁAD GŁÓWNY =====

        main_layout = QHBoxLayout()

        main_layout.addLayout(
            left_panel,
            1
        )

        main_layout.addLayout(
            right_panel,
            3
        )

        self.setLayout(
            main_layout
        )

        # ===== TIMER WYKRESÓW =====

        self.timer = QTimer()

        self.timer.timeout.connect(
            self.update_plot
        )

        self.timer.start(100)

    # ===== TEST KOMEND =====

    def send_rpm(self):

        rpm = self.rpm_input.text()

        if rpm == "":
            return

        self.rpm_target = int(rpm)

        command = f"R{rpm}"

        if self.ser and self.ser.is_open:
            
            try:

                self.ser.write(
                    (command + "\n").encode()
                )

                print(f"Wysłano: {command}")

                self.status_label.setText(f"Status: Wysłano{command}")

            except Exception as e:

                print(e)

        else:
            
            self.status_label.setText(
                "Status: Brak połączenia"
            )

    def send_pwm(self):

        pwm = self.pwm_input.text()

        if pwm == "":
            return

        command = f"P{pwm}"

        print(command)

        if self.ser and self.ser.is_open:

            try:

                self.ser.write(
                    (command + "\n").encode()
                )

                print(f"Wysłano: {command}")

                self.status_label.setText(
                    f"Status: Wysłano {command}"
                )

            except Exception as e:

                print(e)

        else:

            self.status_lable.setText(
                "Status: Brak Połączenia"
            )

    def stop_motor(self):

        commands = ["P0", "R0"]

        if self.ser and self.ser.is_open:
            try:
                for command in commands:
                    self.ser.write((command + "\n").encode())

                print("STOP: wysłano P0 i R0")
                self.status_label.set.Text("Status: STOP")

            except Exception as e:
                print(e)
        else:
            self.status_label.setText("Status: Brak połączenia")

        if self.ser and self.ser.is_open:

            try:

                self.ser.write(
                    (command + "\n").encode()
                )

                print("STOP")

                self.status_label.setText(
                    "Status: STOP"
                )

            except Exception as e:

                print(e)

        else:

            self.status_label.setText(
                "Status: Brak połączenia"
            )

    def refresh_ports(self):

        self.com_box.clear()

        ports = serial.tools.list_ports.comports()

        for port in ports:
            self.com_box.addItem(port.device)

    def connect_serial(self):

        if self.ser and self.ser.is_open:

            self.status_label.setText(
                "Status: Już połączono"
            )

            return

        port = self.com_box.currentText()

        if port == "":

            self.status_label.setText(
                "Status: Brak portu COM"
            )

            return

        print(f"Próba połączenia z {port}")

        try:

            self.ser = serial.Serial(
                port,
                115200,
                timeout=1
            )

            self.status_label.setText(
                f"Status: Połączono z {port}"
            )

            print(f"Połączono z {port}")

        except Exception as e:

            print(f"Błąd połączenia: {e}")

            self.status_label.setText(
                f"Błąd: {e}"
            )

    def disconnect_serial(self):

        if self.ser and self.ser.is_open:

            self.ser.close()
            self.ser = None

            self.status_label.setText(
                "Status: Rozłączono"
            )

            print("Port zamknięty")

        else:

            self.status_label.setText(
                "Status: Brak aktywnego połączenia"
            )

    def start_logging(self):

        print("START LOGGING")

        if self.logging_active:
            return

        default_name = datetime.now().strftime(
            "pomiar_%Y%m%d_%H%M%S.csv"
        )

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Zapisz pomiar",
            default_name,
            "CSV Files (*.csv)"

        )

        if not filename:
            return

        self.csv_file = open(
            filename,
            "w",
            newline=""
        )

        print("PLIK OTWARTY")

        self.csv_writer = csv.writer(
            self.csv_file
        )

        self.csv_writer.writerow(
            [
                "Time",
                "Set RPM",
                "RPM",
                "PWM"
            ]
        )

        self.time_data.clear()
        self.rpm_data.clear()
        self.pwm_data.clear()

        self.rpm_curve.setData([], [])
        self.pwm_curve.setData([],[])

        self.start_time = time.time()

        self.logging_active = True

        self.status_label.setText(
            f"Zapis: {filename}"
        )

    def stop_logging(self):

        if self.csv_file:

            self.csv_file.close()

            self.csv_file = None
            self.csv_writer = None

        self.logging_active = False

        self.status_label.setText(
            "Pomiar zakończony"
        )

    def update_plot(self):

        t = time.time() - self.start_time

        self.time_data.append(t)

        self.rpm_data.append(
            self.current_rpm
        )

        self.pwm_data.append(
            self.current_pwm
        )

        if len(self.time_data) > 300:

            self.time_data.pop(0)
            self.rpm_data.pop(0)
            self.pwm_data.pop(0)

        self.rpm_curve.setData(
            self.time_data,
            self.rpm_data
        )

        self.pwm_curve.setData(
            self.time_data,
            self.pwm_data
        )

    def read_serial(self):
        if not self.ser or not self.ser.is_open:
            return

        try:
            while self.ser.in_waiting:
                line = self.ser.readline().decode(
                    "utf-8", errors="replace"
                ).strip()

                if not line:
                    continue

                fields = line.split(",")

                if len(fields) != 2:
                    print(f"Pominięto nieznany komunikat: {line}")
                    continue

                try:
                    rpm = float(fields[0])
                    pwm = float(fields[1])
                except ValueError:
                    print(f"Niepoprawne dane: {line}")
                    continue

                import math
                if not math.isfinite(rpm) or not math.isfinite(pwm):
                    print(f"Nieprawidłowe wartości: {line}")
                    continue

                self.current_rpm = rpm
                self.current_pwm = pwm

                self.rpm_actual.setText(
                    f"RPM aktualne: {rpm:.1f}"
                )
                self.pwm_actual.setText(
                    f"PWM aktualne: {pwm:.0f}"
                )

                if self.logging_active and self.csv_writer:
                    t = time.time() - self.start_time

                    self.csv_writer.writerow([
                        round(t, 3),
                        self.rpm_target,
                        rpm,
                        pwm
                    ])

        except (serial.SerialException, OSError) as e:
            print(f"Błąd komunikacji szeregowej: {e}")
            self.status_label.setText(
                "Status: Błąd komunikacji"
            )

app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())