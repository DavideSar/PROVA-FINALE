import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def print_mean(sensor):
    name = sensor["entity_id"].iloc[0]
    mean = np.mean(sensor["_value"])
    print(f"{name} MEAN: {mean}")


def print_std(sensor):
    name = sensor["entity_id"].iloc[0]
    std = np.std(sensor["_value"])
    print(f"{name} STD: {std}")

def main():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'log_monitoraggio_25-07-2022.csv')

    if not os.path.exists(csv_path):
        print(f'Errore: Il file {csv_path} non esiste.')
        return

    lines = pd.read_csv(
        csv_path,
        comment='#',
        usecols=['_time', '_value', 'entity_id'],
        skipinitialspace=True
    )

    lines['_time'] = pd.to_datetime(lines['_time'], format='mixed', utc=True)
    lines['_value'] = pd.to_numeric(lines['_value'], errors='coerce')
    lines = lines.dropna(subset=['_value'])

    acc_x_lines = lines[lines['entity_id'] == 'fridge_black_accel_x']
    acc_y_lines = lines[lines['entity_id'] == 'fridge_black_accel_y']
    acc_z_lines = lines[lines['entity_id'] == 'fridge_black_accel_z']
    gyro_x_lines = lines[lines['entity_id'] == 'fridge_black_gyro_x']
    gyro_y_lines = lines[lines['entity_id'] == 'fridge_black_gyro_y']
    gyro_z_lines = lines[lines['entity_id'] == 'fridge_black_gyro_z']
    temp_lines = lines[lines['entity_id'] == 'airq_black_temperature']
    temp_sen55_lines = lines[lines['entity_id'] == 'airq_black_temperature_sen55']
    temp_cpu_lines = lines[lines['entity_id'] == 'fridge_black_internal_temperature']
    temp_probe_lines = lines[lines['entity_id'] == 'fridge_black_probe_temperature']

    sensors = [
        acc_x_lines,
        acc_y_lines,
        acc_z_lines,
        gyro_x_lines,
        gyro_y_lines,
        gyro_z_lines,
        temp_lines,
        temp_sen55_lines,
        temp_cpu_lines,
        temp_probe_lines,
    ]

    for sensor in sensors:
        print_mean(sensor)
        print_std(sensor)
        print()

if __name__ == '__main__':
    main()
