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

    # acc_x = remove_anomalies(lines[lines["entity_id"] == "fridge_black_accel_x"])
    acc_y = remove_anomalies(lines[lines["entity_id"] == "fridge_black_accel_y"])
    # acc_z = remove_anomalies(lines[lines["entity_id"] == "fridge_black_accel_z"])
    gyro_x = remove_anomalies(lines[lines["entity_id"] == "fridge_black_gyro_x"])
    gyro_y = remove_anomalies(lines[lines["entity_id"] == "fridge_black_gyro_y"])
    gyro_z = remove_anomalies(lines[lines["entity_id"] == "fridge_black_gyro_z"])
    temp_avg = remove_anomalies(lines[lines["entity_id"] == "airq_black_temperature"])
    # temp_sen55 = remove_anomalies(lines[lines["entity_id"] == "airq_black_temperature_sen55"])
    temp_cpu = remove_anomalies(lines[lines["entity_id"] == "fridge_black_internal_temperature"])
    temp_probe = remove_anomalies(lines[lines["entity_id"] == "fridge_black_probe_temperature"])

    series = [
        (
            "Gyroscope",
            [
                (gyro_x, "Gyro X", "tab:orange"),
                (gyro_y, "Gyro Y", "tab:blue"),
                (gyro_z, "Gyro Z", "tab:green"),
            ],
        ),
        ("Temp CPU", [(temp_cpu, "Temp CPU", "tab:purple")]),
        ("Temp Probe", [(temp_probe, "Temp Probe", "tab:brown")]),
    ]

    fig, axes = plt.subplots(nrows=len(series) + 1, ncols=1, figsize=(14, 20), sharex=True)

    for ax, (group_key, group) in zip(axes, series):
        for data, label, color in group:
            ax.plot(data["_time"], data["_value"], linewidth=0.5, color=color, label=label)
        ax.minorticks_on()
        ax.grid(which='major', linestyle='-', linewidth='0.8', color='black', alpha=0.3)
        ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black', alpha=0.2)
        ax.set_ylabel(group_key, fontsize=8)
        if len(group) > 1:
            ax.legend(fontsize=7, loc="upper right", frameon=True, framealpha=1, edgecolor='black')

    acc_ax = axes[-1]
    line1 = acc_ax.plot(acc_y['_time'], acc_y['_value'], linewidth=0.3, color='blue', label='Acc Y')
    acc_ax.set_ylabel("Acc Y", fontsize=8)

    temp_ax = acc_ax.twinx()
    line2 = temp_ax.plot(temp_avg['_time'], temp_avg['_value'], linewidth=1, color='red', label='Temp')
    temp_ax.set_ylabel("Temp", fontsize=8)

    # temp_prob_ax = acc_ax.twinx()
    # temp_prob_ax.plot(temp_probe['_time'], temp_probe['_value'], linewidth=1, color='purple', label='Temp')
    # temp_prob_ax.set_ylabel("Temp", fontsize=8)

    acc_ax.minorticks_on()
    acc_ax.grid(which='major', linestyle='-', linewidth='0.8', color='black', alpha=0.3)
    acc_ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black', alpha=0.2)

    fig.suptitle("Sensors Data - 25/07/2022", fontsize=14, fontweight="bold", y=1)
    axes[-1].set_xlabel("Time")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
