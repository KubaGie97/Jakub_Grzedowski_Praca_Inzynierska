# SpinCoater

**Projekt inżynierski / Engineering project**

- **Autor / Author:** Jakub Grzędowski
- **Uczelnia / University:** Uniwersytet Wrocławski / University of Wrocław
- **Cel / Purpose:** urządzenie typu *spin coater* do zastosowań w laboratorium elektrochemicznym / a spin-coating device for use in an electrochemical laboratory.

---

## 🇵🇱 Opis projektu

Repozytorium zawiera materiały uzupełniające do pracy inżynierskiej dotyczącej projektu i wykonania urządzenia typu **spin coater**, przeznaczonego do zastosowań w laboratorium elektrochemicznym.

Projekt obejmuje konstrukcję mechaniczną urządzenia, sterowanie silnikiem BLDC za pomocą mikrokontrolera Arduino Mega 2560, aplikację komputerową oraz dane i opracowania z badań urządzenia.

### Struktura i zawartość repozytorium

#### `SpinCoaterControl/` — oprogramowanie mikrokontrolera
- `SpinCoaterControl.ino` — kod obsługujący mikrokontroler Arduino Mega 2560.

#### `SpinCoaterControlApp/` — aplikacja interfejsu użytkownika
- `SpinCoaterControlApp.py` — kod źródłowy aplikacji interfejsu użytkownika.
- `SpinCoaterControl.exe` — aplikacja wykonywalna dla systemu Windows.
- `dist/` — katalog związany z dystrybucją aplikacji.

#### Pliki STL — modele do druku 3D
- `Pokrywa.stl` — model pokrywy obudowy urządzenia.
- `Podstawa.stl` — model podstawy obudowy urządzenia.
- `Top_Holder.stl` — model górnej części uchwytu silnika i wału roboczego.
- `Bot_Holder.stl` — model dolnej części uchwytu silnika i wału roboczego.
- `Klosz.stl` — model osłony obszaru roboczego.
- `Talerz.stl` — model pierwszej wersji talerza obszaru roboczego.
- `Talerz_scianka.stl` — model drugiej wersji talerza obszaru roboczego.

#### Filmy demonstracyjne
- `Wideo_Test_Pracy.mp4` — nagranie z pracy układu.
- `Wideo_Test_Uchwytu.mp4` — nagranie z pracy układu z zamontowaną próbką.

#### `Pliki z Pomiarów/` — surowe dane pomiarowe
Pliki CSV zawierające dane zarejestrowane podczas badań:
- `Badanie_Stabilności_Pracy.csv`
- `Badanie_Zachowania_PWM.csv`
- `Badanie_Zachowania_RPM.csv`
- `Maksymalne_RPM_12V.csv`
- `Maksymalne_RPM_18V.csv`
- `Maksymalne_RPM_24V.csv`
- `Maksymalne_RPM_30V.csv`

Pliki CSV stanowią dane źródłowe do dalszej analizy. Interpretację kolumn i szczegóły procedury pomiarowej należy odczytywać łącznie z dokumentacją i opisem badań w pracy inżynierskiej.

#### `Opracowania Pomiarów/` — opracowanie danych w arkuszach kalkulacyjnych
Pliki Excel zawierające opracowania pomiarów:
- `Badanie_Stabilności_Pracy.xlsx`
- `Badanie_Zachowania_PWM.xlsx`
- `Badanie_Zachowania_RPM.xlsx`
- `Maksymalne_RPM_12V.xlsx`
- `Zestawienie_Prędkości` — zestawienie prędkości; rozszerzenie pliku należy potwierdzić.

### Informacje techniczne

- **Mikrokontroler:** Arduino Mega 2560.
- **Napęd:** silnik BLDC.
- **Sterownik silnika:** BLD-120A.
- **Pomiar prędkości:** czujniki Halla; w badaniach wykorzystywano również tachometr.
- **Napięcia zasilania objęte badaniami:** 12 V, 18 V, 24 V i 30 V w plikach dotyczących maksymalnej prędkości obrotowej.

Szczegółowe parametry komponentów, konfigurację połączeń oraz procedurę uruchomienia należy weryfikować na podstawie kodu i dokumentacji projektu.

### Uruchomienie

**Oprogramowanie Arduino**
1. Otwórz plik `SpinCoaterControl.ino` w Arduino IDE.
2. Wybierz właściwą płytkę i port komunikacyjny.
3. Przed wgraniem programu sprawdź połączenia i konfigurację sprzętową.

Wersja Arduino IDE, wymagane biblioteki oraz dokładne ustawienia kompilacji: **do uzupełnienia**.

**Aplikacja komputerowa**
- Uruchom `SpinCoaterControl.exe`, jeśli jest to wersja przeznaczona dla Twojego systemu.
- Plik `SpinCoaterControlApp.py` zawiera kod źródłowy aplikacji.

Wymagania systemowe, zależności i instrukcja ponownego zbudowania aplikacji: **do uzupełnienia po weryfikacji projektu**.

### Modele 3D

Pliki STL zawierają modele wybranych elementów mechanicznych urządzenia. Przed wydrukiem należy sprawdzić skalę, jednostki i dopasowanie części do konstrukcji. Parametry druku oraz materiały nie są określone w tym pliku README.

### Licencja

Repozytorium nie ma obecnie przypisanej licencji. Nie należy zakładać, że zawartość może być dowolnie kopiowana, modyfikowana lub rozpowszechniana. Przed dodaniem licencji należy sprawdzić prawa do kodu, bibliotek i pozostałych materiałów.

---

## 🇬🇧 Project description

This repository contains supplementary materials for an engineering thesis on the design and construction of a **spin-coating device** intended for use in an electrochemical laboratory.

The project includes the mechanical design, BLDC motor control using an Arduino Mega 2560, a desktop application, and measurement data and analyses from device testing.

### Repository structure and contents

#### `SpinCoaterControl/` — microcontroller firmware
- `SpinCoaterControl.ino` — firmware for the Arduino Mega 2560 microcontroller.

#### `SpinCoaterControlApp/` — user interface application
- `SpinCoaterControlApp.py` — application source code.
- `SpinCoaterControl.exe` — executable application for Windows.
- `dist/` — application distribution directory.

#### STL files — 3D-printable models
- `Pokrywa.stl` — enclosure cover.
- `Podstawa.stl` — enclosure base.
- `Top_Holder.stl` — upper part of the motor and working-shaft holder.
- `Bot_Holder.stl` — lower part of the motor and working-shaft holder.
- `Klosz.stl` — cover for the working area.
- `Talerz.stl` — first version of the working-area plate.
- `Talerz_scianka.stl` — second version of the working-area plate.

#### Demonstration videos
- `Wideo_Test_Pracy.mp4` — video showing the device in operation.
- `Wideo_Test_Uchwytu.mp4` — video showing the device operating with a sample mounted.

#### `Pliki z Pomiarów/` — raw measurement data
CSV files containing data recorded during testing:
- `Badanie_Stabilności_Pracy.csv`
- `Badanie_Zachowania_PWM.csv`
- `Badanie_Zachowania_RPM.csv`
- `Maksymalne_RPM_12V.csv`
- `Maksymalne_RPM_18V.csv`
- `Maksymalne_RPM_24V.csv`
- `Maksymalne_RPM_30V.csv`

These CSV files are source data for further analysis. Column definitions and measurement procedures should be interpreted together with the project documentation and the relevant sections of the thesis.

#### `Opracowania Pomiarów/` — processed data in spreadsheets
Excel files containing processed measurement results:
- `Badanie_Stabilności_Pracy.xlsx`
- `Badanie_Zachowania_PWM.xlsx`
- `Badanie_Zachowania_RPM.xlsx`
- `Maksymalne_RPM_12V.xlsx`
- `Zestawienie_Prędkości` — speed summary; the file extension needs to be confirmed.

### Technical information

- **Microcontroller:** Arduino Mega 2560.
- **Drive:** BLDC motor.
- **Motor driver:** BLD-120A.
- **Speed measurement:** Hall sensors; a tachometer was also used during testing.
- **Supply voltages covered by maximum-speed tests:** 12 V, 18 V, 24 V, and 30 V.

Detailed component specifications, wiring configuration, and startup procedures should be verified against the project source files and documentation.

### Setup

**Arduino firmware**
1. Open `SpinCoaterControl.ino` in the Arduino IDE.
2. Select the correct board and serial port.
3. Check the hardware wiring and configuration before uploading the firmware.

Arduino IDE version, required libraries, and exact build settings: **to be completed**.

**Desktop application**
- Run `SpinCoaterControl.exe` if it is compatible with your operating system.
- `SpinCoaterControlApp.py` contains the application source code.

System requirements, dependencies, and instructions for rebuilding the application: **to be completed after verifying the project files**.

### 3D models

The STL files contain models of selected mechanical components. Before printing, verify scale, units, and fit with the physical assembly. Printing parameters and materials are not specified in this README.

### License

No license is currently assigned to this repository. Users should not assume that its contents may be freely copied, modified, or redistributed. Verify the rights to the code, libraries, and other materials before adding a license.

---

## Do uzupełnienia / To be completed

- [ ] Potwierdzić rozszerzenie pliku `Zestawienie_Prędkości` / Confirm the extension of `Zestawienie_Prędkości`.
- [ ] Uzupełnić wersję Arduino IDE i wymagane biblioteki / Add Arduino IDE version and required libraries.
- [ ] Uzupełnić wymagania i zależności aplikacji / Add application requirements and dependencies.
- [ ] Dodać schemat połączeń, jeśli jest dostępny / Add the wiring diagram if available.
- [ ] Sprawdzić prawa do publikacji wszystkich materiałów / Verify publication rights for all materials.
