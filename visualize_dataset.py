"""
Visualize the electronics prognostics dataset (MOSFET / IGBT / Capacitor aging data).

Dataset root (edit if you moved the folder):
    C:\\Users\\shahm\\Downloads\\Dataset

Install dependencies:
    pip install matplotlib scipy h5py numpy

Run:
    python visualize_dataset.py mosfet
    python visualize_dataset.py igbt
    python visualize_dataset.py capacitor
    python visualize_dataset.py all
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import scipy.io as sio

# ---------------------------------------------------------------------------
# Path to your dataset (from the earlier upload)
# ---------------------------------------------------------------------------
DATASET_ROOT = Path(r"C:\Users\shahm\Downloads\Dataset")

MOSFET_DIR = (
    DATASET_ROOT
    / "13.+MOSFET+Thermal+Overstress+Aging"
    / "13. MOSFET Thermal Overstress Aging"
    / "MOSFET_Thermal_Overstress_Aging_v0"
    / "MOSFET_Thermal_Overstress_Aging_v0"
)
IGBT_DIR = (
    DATASET_ROOT
    / "8.+IGBT+Accelerated+Aging"
    / "8. IGBT Accelerated Aging"
    / "IGBTAgingData_04022009"
    / "IGBTAgingData_04022009"
    / "Data"
)
CAPACITOR_DIR = (
    DATASET_ROOT / "12.+Capacitor+Electrical+Stress" / "12. Capacitor Electrical Stress"
)


# ---------------------------------------------------------------------------
# MOSFET Thermal Overstress Aging
#   .mat -> measurement.steadyState = list of samples, each with
#           timeEpoch and timeDomain: {supplyVoltage, packageTemperature,
#           drainSourceVoltage, drainCurrent, flangeTemperature}
#   .mat -> measurement.transient = list of samples, each with
#           timeDomain: {dt, gateSignalVoltage, gateSourceVoltage,
#           drainSourceVoltage, drainCurrent} (1000-point waveforms)
# ---------------------------------------------------------------------------
def plot_mosfet(mat_path: Path):
    m = sio.loadmat(mat_path, simplify_cells=True)
    meas = m["measurement"]

    steady = meas["steadyState"]
    t0 = steady[0]["timeEpoch"]
    time_hr = np.array([(s["timeEpoch"] - t0) * 24 for s in steady])  # days -> hours
    drain_current = np.array([s["timeDomain"]["drainCurrent"] for s in steady])
    package_temp = np.array([s["timeDomain"]["packageTemperature"] for s in steady])
    flange_temp = np.array([s["timeDomain"]["flangeTemperature"] for s in steady])
    vds = np.array([s["timeDomain"]["drainSourceVoltage"] for s in steady])

    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    fig.suptitle(f"MOSFET Steady-State Aging Trend — {mat_path.name}")

    axes[0, 0].plot(time_hr, drain_current, lw=0.7)
    axes[0, 0].set_title("Drain current")
    axes[0, 0].set_xlabel("Time (h)")
    axes[0, 0].set_ylabel("A")

    axes[0, 1].plot(time_hr, package_temp, lw=0.7, color="tab:red")
    axes[0, 1].plot(time_hr, flange_temp, lw=0.7, color="tab:orange", label="flange")
    axes[0, 1].set_title("Package / flange temperature")
    axes[0, 1].set_xlabel("Time (h)")
    axes[0, 1].set_ylabel("deg C")
    axes[0, 1].legend()

    axes[1, 0].plot(time_hr, vds, lw=0.7, color="tab:green")
    axes[1, 0].set_title("Drain-source voltage")
    axes[1, 0].set_xlabel("Time (h)")
    axes[1, 0].set_ylabel("V")

    # one transient switching waveform, for context
    tr = meas["transient"][len(meas["transient"]) // 2]["timeDomain"]
    t_us = np.arange(len(tr["drainCurrent"])) * tr["dt"] * 1e6
    axes[1, 1].plot(t_us, tr["drainCurrent"], lw=0.7)
    axes[1, 1].set_title("Sample transient switching waveform")
    axes[1, 1].set_xlabel("Time (us)")
    axes[1, 1].set_ylabel("Drain current (A)")

    fig.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# IGBT Accelerated Aging
#   .mat -> flat arrays: TIME, COLLECTOR_VOLTAGE, COLLECTOR_CURRENT,
#           GATE_VOLTAGE, GATE_CURRENT, HEAT_SINK_TEMP, PACKAGE_TEMP
#   Breakdown.csv / LeakageIV.csv / Turn On.csv -> two columns (V, I), no header
# ---------------------------------------------------------------------------
def plot_igbt(mat_path: Path):
    m = sio.loadmat(mat_path, simplify_cells=True)

    time = m["TIME"]
    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    fig.suptitle(f"IGBT Thermal Overstress Aging — {mat_path.name}")

    axes[0, 0].plot(time, m["COLLECTOR_CURRENT"], lw=0.4)
    axes[0, 0].set_title("Collector current")
    axes[0, 0].set_xlabel("Time (s)")
    axes[0, 0].set_ylabel("A")

    axes[0, 1].plot(time, m["COLLECTOR_VOLTAGE"], lw=0.4, color="tab:green")
    axes[0, 1].set_title("Collector-emitter voltage")
    axes[0, 1].set_xlabel("Time (s)")
    axes[0, 1].set_ylabel("V")

    axes[1, 0].plot(time, m["PACKAGE_TEMP"], lw=0.4, color="tab:red", label="package")
    axes[1, 0].plot(time, m["HEAT_SINK_TEMP"], lw=0.4, color="tab:orange", label="heat sink")
    axes[1, 0].set_title("Temperature")
    axes[1, 0].set_xlabel("Time (s)")
    axes[1, 0].set_ylabel("deg C")
    axes[1, 0].legend()

    axes[1, 1].plot(time, m["GATE_VOLTAGE"], lw=0.4, color="tab:purple")
    axes[1, 1].set_title("Gate voltage")
    axes[1, 1].set_xlabel("Time (s)")
    axes[1, 1].set_ylabel("V")

    fig.tight_layout()
    plt.show()


def plot_igbt_csv(csv_path: Path):
    data = np.loadtxt(csv_path, delimiter=",")
    voltage, current = data[:, 0], data[:, 1]

    plt.figure(figsize=(7, 5))
    plt.semilogy(voltage, np.abs(current) + 1e-15)
    plt.title(f"IGBT SMU sweep — {csv_path.parent.name}/{csv_path.name}")
    plt.xlabel("Voltage (V)")
    plt.ylabel("|Current| (A, log scale)")
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------------
# Capacitor Electrical Stress (ES##.mat, MATLAB v7.3 -> HDF5, needs h5py)
#   /ES##/Transient_Data/ES##C{1..7}/VL, VO -> (75826, 400) float64
#     rows = time samples within one capture, columns = repeated captures
#     over the life of the test (aging progression)
# ---------------------------------------------------------------------------
def plot_capacitor(mat_path: Path, channel: str = "ES10C1"):
    import h5py

    device = mat_path.stem  # e.g. "ES10"
    with h5py.File(mat_path, "r") as hf:
        grp = hf[device]["Transient_Data"][channel]
        vo = grp["VO"]  # output voltage, (samples, captures)
        vl = grp["VL"]  # line voltage, (samples, captures)

        n_samples, n_captures = vo.shape
        # pick a handful of captures spread across the test lifetime
        capture_idxs = np.linspace(0, n_captures - 1, 5, dtype=int)

        fig, axes = plt.subplots(1, 2, figsize=(11, 5))
        fig.suptitle(f"Capacitor Electrical Stress — {device} / {channel}")

        cmap = plt.cm.viridis(np.linspace(0, 1, len(capture_idxs)))
        for c_idx, color in zip(capture_idxs, cmap):
            axes[0].plot(vo[:, c_idx], color=color, lw=0.6, label=f"capture {c_idx}")
        axes[0].set_title("Output voltage waveform (aging progression)")
        axes[0].set_xlabel("Sample")
        axes[0].set_ylabel("VO (V)")
        axes[0].legend(fontsize=7)

        # peak output voltage across the whole test = simple degradation trend
        peak_vo = np.max(vo[:, :], axis=0)
        axes[1].plot(peak_vo, lw=0.8, color="tab:red")
        axes[1].set_title("Peak VO per capture (degradation trend)")
        axes[1].set_xlabel("Capture index (time progresses)")
        axes[1].set_ylabel("Peak VO (V)")

        fig.tight_layout()
        plt.show()


# ---------------------------------------------------------------------------
def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"

    if which in ("mosfet", "all"):
        sample = next(MOSFET_DIR.glob("Test_10_run_*.mat"))
        plot_mosfet(sample)

    if which in ("igbt", "all"):
        dc_dir = IGBT_DIR / "Thermal Overstress Aging with DC at gate"
        sample = next(dc_dir.glob("*.mat"))
        plot_igbt(sample)

        csv_sample = next(IGBT_DIR.rglob("Breakdown.csv"))
        plot_igbt_csv(csv_sample)

    if which in ("capacitor", "all"):
        plot_capacitor(CAPACITOR_DIR / "ES10.mat", channel="ES10C1")


if __name__ == "__main__":
    main()
