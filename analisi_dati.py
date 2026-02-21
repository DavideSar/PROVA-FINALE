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
    print(f"Media: {mean:.2f}")
    print(f"STD: {std:.2f}")
    print(f"Anomalie: {anomalies}")
    print()
    return cleaned_lines


def make_graph(graph, value1, label1, linewidth1, value2, label2, linewidth2):
    line1 = graph.plot(value1["_time"], value1["_value"], linewidth=linewidth1, color="red", label=label1)
    graph.set_ylabel(label1, fontsize=8)

    graph_twin = graph.twinx()
    line2 = graph_twin.plot(value2["_time"], value2["_value"], linewidth=linewidth2, color="blue", label=label2)
    graph_twin.set_ylabel(label2, fontsize=8)

    # Set legend
    labels = [line.get_label() for line in (line1 + line2)]
    graph.legend(
        line1 + line2,
        labels,
        fontsize=10,
        loc="upper right",
        frameon=True,
        framealpha=1,
        edgecolor="black",
    )

    # Set grid
    graph.minorticks_on()
    graph.grid(which="major", linestyle="-", linewidth="0.8", color="black", alpha=0.3)
    graph.grid(which="minor", linestyle=":", linewidth="0.5", color="black", alpha=0.2)

    return graph

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
    # acc_z = remove_anomalies(lines[lines["entity_id"] == "fridge_black_accel_z"])
    # gyro_x = remove_anomalies(lines[lines["entity_id"] == "fridge_black_gyro_x"])
    # gyro_y = remove_anomalies(lines[lines["entity_id"] == "fridge_black_gyro_y"])
    # gyro_z = remove_anomalies(lines[lines["entity_id"] == "fridge_black_gyro_z"])
    # temp_sen55 = remove_anomalies(lines[lines["entity_id"] == "airq_black_temperature_sen55"])
    # temp_cpu = remove_anomalies(lines[lines["entity_id"] == "fridge_black_internal_temperature"])

    acc_y = remove_anomalies(lines[lines["entity_id"] == "fridge_black_accel_y"])
    temp_avg = remove_anomalies(lines[lines["entity_id"] == "airq_black_temperature"])
    temp_probe = remove_anomalies(lines[lines["entity_id"] == "fridge_black_probe_temperature"])

    fig, (temp_acc, probe_acc, avg_prob) = plt.subplots(nrows=3, ncols=1, figsize=(14, 20), sharex=True)

    make_graph(temp_acc, temp_avg, "Ext Temp", 1, acc_y, "Acc Y", 0.3)
    make_graph(probe_acc, temp_probe, "Fridge Temp", 0.7, acc_y, "Acc Y", 0.3)
    make_graph(avg_prob, temp_avg, "Ext Temp", 1, temp_probe, "Probe Temp", 0.5)

    temp_acc.set_title("External Temperature vs Acc Y", fontsize=16)
    probe_acc.set_title("Probe Temperature vs Acc Y", fontsize=16)
    avg_prob.set_title("External vs Probe Temperature", fontsize=16)
    avg_prob.set_xlabel("Time")
    plt.show()

if __name__ == "__main__":
    main()
