
# Data Analysis Project - Sensor Monitoring

## Overview
This project analyzes sensor data from a monitoring log file. It includes implementations in both **C** and **Python** that perform statistical analysis on data from sensors.

## Features
- **CSV Data Parsing**: Reads and processes monitoring data from CVS file, checking for correct data types.
- **Statistical Analysis**:
    - mean (average value)
    - median (middle value)
    - mode (most frequent value)
    - variance and standard deviation (data spread)
    - and standard error on mean (confidence in the mean estimate).
- **Visualization**: Python version includes multi-axis time-series graphs.
- **Dual Output**: Console display and file logging (C version).

## Files
- `analisi_dati.c` - C implementation with statistical functions, print stats on terminale and produces log file.
- `analisi_dati.py` - Python implementation with matplotlib visualization, also print stats on terminal.

## Sensors Tracked
- `fridge_black_accel_y` - Refrigerator Y-axis acceleration (m/s²), identifies accension of fridge motor.
- `airq_black_temperature` - Identifies external air temperature (°C).
- `fridge_black_probe_temperature` - Identifies internal probe temperature (°C).

## Sensors NOT Tracked
- `fridge_black_accel_x` and `fridge_black_accel_z` - Refrigerator X and Z axis acceleration not relevant, Z alway flat, X always -9.8 (gravity).
- `fridge_black_gyro_x/y/z` - Refrigeretor gyroscope, data is not relevant.
- `airq_black_temperature_sen55` - External temperature sensor, same as `airq_black_temperature`, duplicate not relevant.
- `fridge_black_internal_temperature` - Temperature of microprocessor CPU, not relevant for fridge status analysis.

## Requirements
### Python
- Python 3.8+
- matplotlib
- numpy
- pandas

### C
- GCC compiler

## Installation
### Python
```bash
pip install matplotlib numpy pandas
```
Check official intallation guides for better instructions.
### C
No external dependencies required beyond standard C library.

## Usage

### C
```bash
gcc analisi_dati.c
./analisi_dati
```
Output saved to `analized_data.log`: shows statistical analysis on data for each sensor.

### Python
```bash
python analisi_dati.py
```
Output shows statistical data on terminal and plots sensor data showing 3 graphs:
- **External temperature vs Acc Y**: shows how fridge motor accension impact on external temperature and the delay of such interaction.
- **Internal temperature vs Acc Y**: shows how fridge motor accension impact on internal temperature and the delay of such interaction.
- **External temperature vs Internal temperature**: shows how internal and external temperatures relates to each other, a prolonged accension of the fridge shows slightly longer external temperture raise but a strong and prolonged decrease in internal teperature.