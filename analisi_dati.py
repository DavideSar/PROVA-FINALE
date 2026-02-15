import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def get_mean(lines):
    mean = np.mean(lines["_value"])
    return mean

def get_std(lines):
    std = np.std(lines["_value"])
    return std

def remove_anomalies(lines):
    mean = get_mean(lines)
    std = get_std(lines)
    cleaned_lines = lines[abs(lines["_value"] - mean) < 3 * std]
    anomalies = len(lines) - len(cleaned_lines)
    print(f'Sensore: {lines["entity_id"].iloc[0]}')
    print(f'Media: {mean:.2f}')
    print(f'STD: {std:.2f}')
    print(f'Anomalie: {anomalies}')
    print()
    return cleaned_lines

def main():

    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, "log_monitoraggio_25-07-2022.csv")

    if not os.path.exists(csv_path):
        print(f"Errore: Il file {csv_path} non esiste.")
        return

    lines = pd.read_csv(
        csv_path,
        comment="#",
        usecols=["_time", "_value", "entity_id"],
        skipinitialspace=True,
    )

    lines["_time"] = pd.to_datetime(lines["_time"], format="mixed", utc=True)
    lines["_value"] = pd.to_numeric(lines["_value"], errors="coerce")
    lines = lines.dropna(subset=["_value"])

    acc_x = remove_anomalies(lines[lines["entity_id"] == "fridge_black_accel_x"])
    acc_y = remove_anomalies(lines[lines["entity_id"] == "fridge_black_accel_y"])
    acc_z = remove_anomalies(lines[lines["entity_id"] == "fridge_black_accel_z"])
    gyro_x = remove_anomalies(lines[lines["entity_id"] == "fridge_black_gyro_x"])
    gyro_y = remove_anomalies(lines[lines["entity_id"] == "fridge_black_gyro_y"])
    gyro_z = remove_anomalies(lines[lines["entity_id"] == "fridge_black_gyro_z"])
    temp = remove_anomalies(lines[lines["entity_id"] == "airq_black_temperature"])
    temp_sen55 = remove_anomalies(lines[lines["entity_id"] == "airq_black_temperature_sen55"])
    temp_cpu = remove_anomalies(lines[lines["entity_id"] == "fridge_black_internal_temperature"])
    temp_probe = remove_anomalies(lines[lines["entity_id"] == "fridge_black_probe_temperature"])


if __name__ == "__main__":
    main()
