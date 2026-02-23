import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def load_available_data():
    base_dir = Path(__file__).resolve().parents[1]
    parent_dir = base_dir.parent

    current_csv = port-scanner/results/benchmarks.csv
    go_csv = port-scanner-go/results/benchmarks.csv

    dataframes = []

    if current_csv.exists():
        dataframes.append(pd.read_csv(current_csv))

    if go_csv.exists():
        dataframes.append(pd.read_csv(go_csv))

    if not dataframes:
        raise FileNotFoundError("No benchmark CSV files found.")

    df = pd.concat(dataframes, ignore_index=True)

    df["workers"] = df["workers"].astype(int)
    df["timeout_s"] = df["timeout_s"].astype(int)
    df["total_time_s"] = df["total_time_s"].astype(float)

    return df


def plot_time_vs_workers(df, target, output_dir):
    target_df = df[df["target"] == target]

    for timeout in sorted(target_df["timeout_s"].unique()):
        subset = target_df[target_df["timeout_s"] == timeout]

        plt.figure()

        for lang in subset["lang"].unique():
            lang_data = subset[subset["lang"] == lang].sort_values("workers")

            plt.plot(
                lang_data["workers"],
                lang_data["total_time_s"],
                marker="o",
                label=lang.capitalize()
            )

        plt.xlabel("Number of Workers")
        plt.ylabel("Total Scan Time (seconds)")
        plt.title(f"{target} | Timeout={timeout}s | Time vs Workers")
        plt.legend()
        plt.grid(True)

        filename = output_dir / f"{target}_timeout_{timeout}_time_vs_workers.png"
        plt.savefig(filename, bbox_inches="tight")
        plt.close()


def plot_time_vs_timeout(df, target, output_dir):
    target_df = df[df["target"] == target]

    plt.figure()

    for lang in target_df["lang"].unique():
        lang_data = target_df[target_df["lang"] == lang]
        grouped = lang_data.groupby("timeout_s")["total_time_s"].mean().reset_index()

        plt.plot(
            grouped["timeout_s"],
            grouped["total_time_s"],
            marker="o",
            label=lang.capitalize()
        )

    plt.xlabel("Timeout (seconds)")
    plt.ylabel("Average Total Scan Time (seconds)")
    plt.title(f"{target} | Time vs Timeout")
    plt.legend()
    plt.grid(True)

    filename = output_dir / f"{target}_time_vs_timeout.png"
    plt.savefig(filename, bbox_inches="tight")
    plt.close()


def plot_relative_performance(df, target, output_dir):
    target_df = df[df["target"] == target]

    if not {"python", "go"}.issubset(set(target_df["lang"].unique())):
        return  # comparative plot requires both languages

    python_df = target_df[target_df["lang"] == "python"]
    go_df = target_df[target_df["lang"] == "go"]

    merged = pd.merge(
        python_df,
        go_df,
        on=["workers", "timeout_s", "target"],
        suffixes=("_python", "_go")
    )

    merged["performance_ratio"] = (
        merged["total_time_s_python"] /
        merged["total_time_s_go"]
    )

    merged = merged.sort_values("workers")

    plt.figure()

    plt.plot(
        merged["workers"],
        merged["performance_ratio"],
        marker="o"
    )

    plt.axhline(y=1.0, linestyle="--")
    plt.xlabel("Number of Workers")
    plt.ylabel("Python / Go Execution Time Ratio")
    plt.title(f"{target} | Relative Performance (Ratio > 1 ⇒ Go Faster)")
    plt.grid(True)

    filename = output_dir / f"{target}_relative_performance.png"
    plt.savefig(filename, bbox_inches="tight")
    plt.close()


def main():
    df = load_available_data()

    output_dir = Path(__file__).resolve().parents[1] / "plots"
    output_dir.mkdir(exist_ok=True)

    for target in df["target"].unique():
        plot_time_vs_workers(df, target, output_dir)
        plot_time_vs_timeout(df, target, output_dir)
        plot_relative_performance(df, target, output_dir)

    print("Benchmark visualizations generated successfully.")


if __name__ == "__main__":
    main()