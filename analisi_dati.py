import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

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

    acc_x_mean = acc_x_lines['_value'].mean()
    acc_y_mean = acc_y_lines['_value'].mean()
    acc_z_mean = acc_z_lines['_value'].mean()
    gyro_x_mean = gyro_x_lines['_value'].mean()
    gyro_y_mean = gyro_y_lines['_value'].mean()
    gyro_z_mean = gyro_z_lines['_value'].mean()
    temp_mean = temp_lines['_value'].mean()
    temp_sen55_mean = temp_sen55_lines['_value'].mean()
    temp_cpu_mean = temp_cpu_lines['_value'].mean()
    temp_probe_mean = temp_probe_lines['_value'].mean()

    print(f"Mean values:")
    print(f"Acc X: {acc_x_mean}")
    print(f"Acc Y: {acc_y_mean}")
    print(f"Acc Z: {acc_z_mean}")
    print(f"Gyro X: {gyro_x_mean}")
    print(f"Gyro Y: {gyro_y_mean}")
    print(f"Gyro Z: {gyro_z_mean}")
    print(f"Temp: {temp_mean}")
    print(f"Temp SEN55: {temp_sen55_mean}")
    print(f"Temp CPU: {temp_cpu_mean}")
    print(f"Temp Probe: {temp_probe_mean}")

    acc_x_std = acc_x_lines['_value'].std()
    acc_y_std = acc_y_lines['_value'].std()
    acc_z_std = acc_z_lines['_value'].std()
    gyro_x_std = gyro_x_lines['_value'].std()
    gyro_y_std = gyro_y_lines['_value'].std()
    gyro_z_std = gyro_z_lines['_value'].std()
    temp_std = temp_lines['_value'].std()
    temp_sen55_std = temp_sen55_lines['_value'].std()
    temp_cpu_std = temp_cpu_lines['_value'].std()
    temp_probe_std = temp_probe_lines['_value'].std()

    print(f"Std values:")
    print(f"Acc X: {acc_x_std}")
    print(f"Acc Y: {acc_y_std}")
    print(f"Acc Z: {acc_z_std}")
    print(f"Gyro X: {gyro_x_std}")
    print(f"Gyro Y: {gyro_y_std}")
    print(f"Gyro Z: {gyro_z_std}")
    print(f"Temp: {temp_std}")
    print(f"Temp SEN55: {temp_sen55_std}")
    print(f"Temp CPU: {temp_cpu_std}")
    print(f"Temp Probe: {temp_probe_std}")

if __name__ == '__main__':
    main()
