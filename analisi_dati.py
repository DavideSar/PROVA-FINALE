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

    acc_x = lines[lines["entity_id"] == "fridge_black_accel_x"]
    acc_y = lines[lines["entity_id"] == "fridge_black_accel_y"]
    acc_z = lines[lines["entity_id"] == "fridge_black_accel_z"]
    gyro_x = lines[lines["entity_id"] == "fridge_black_gyro_x"]
    gyro_y = lines[lines["entity_id"] == "fridge_black_gyro_y"]
    gyro_z = lines[lines["entity_id"] == "fridge_black_gyro_z"]
    temp = lines[lines["entity_id"] == "airq_black_temperature"]
    temp_sen55 = lines[lines["entity_id"] == "airq_black_temperature_sen55"]
    temp_cpu = lines[lines["entity_id"] == "fridge_black_internal_temperature"]
    temp_probe = lines[lines["entity_id"] == "fridge_black_probe_temperature"]

    sensors = [
        acc_x,
        acc_y,
        acc_z,
        gyro_x,
        gyro_y,
        gyro_z,
        temp,
        temp_sen55,
        temp_cpu,
        temp_probe,
    ]

    total_anomalies = 0
    anomalies = 0

    for sensor in sensors:
        mean = get_mean(sensor)
        std = get_std(sensor)
        print(f'{sensor["entity_id"].iloc[0]} \nMEDIA: {mean} \nSTD: {std}')

        print(f'total lines: {len(sensor)}')

        for line in sensor.itertuples():
            if abs(line._2 - mean) > 3 * std:
                print(f"Valore anomalo: {line._2}")
                anomalies += 1
                total_anomalies += 1

        sensor = sensor[abs(sensor["_value"] - mean) < 3 * std]

        print(f'lines after cleaning: {len(sensor)}')
        print(f'anomalies: {anomalies}')
        anomalies = 0
        print()

    print(total_anomalies)

if __name__ == "__main__":
    main()
