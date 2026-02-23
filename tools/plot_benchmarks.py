import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def load_data():
    # Current repo base directory
    base_dir = Path(__file__).resolve().parents[1]

    # Parent directory (CyberSec_work)
    parent_dir = base_dir.parent

    # Local CSV (current repo)
    local_csv = base_dir / "results" / "benchmarks.csv"

    # Sibling repos
    python_csv = parent_dir / "port-scanner" / "results" / "benchmarks.csv"
    go_csv = parent_dir / "port-scanner-go" / "results" / "benchmarks.csv"

    dataframes = []

    # Always load current repo CSV if exists
    if local_csv.exists():
        dataframes.append(pd.read_csv(local_csv))

    # Load python repo CSV if exists
    if python_csv.exists() and python_csv != local_csv:
        dataframes.append(pd.read_csv(python_csv))

    # Load go repo CSV if exists
    if go_csv.exists() and go_csv != local_csv:
        dataframes.append(pd.read_csv(go_csv))

    if not dataframes:
        raise FileNotFoundError("No benchmark CSV files found.")

    df = pd.concat(dataframes, ignore_index=True)

    # Convert safely
    df["workers"] = pd.to_numeric(df["workers"], errors="coerce")
    df["timeout_s"] = pd.to_numeric(df["timeout_s"], errors="coerce")
    df["total_time_s"] = pd.to_numeric(df["total_time_s"], errors="coerce")

    # Drop corrupted rows
    df = df.dropna(subset=["workers", "timeout_s", "total_time_s"])

    # Cast cleanly
    df["workers"] = df["workers"].astype(int)
    df["timeout_s"] = df["timeout_s"].astype(int)

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

        plt.savefig(output_dir / f"{target}_timeout_{timeout}_time_vs_workers.png", bbox_inches="tight")
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

    plt.savefig(output_dir / f"{target}_time_vs_timeout.png", bbox_inches="tight")
    plt.close()


def plot_relative_performance(df, target, output_dir):
    target_df = df[df["target"] == target]

    if not {"python", "go"}.issubset(set(target_df["lang"].unique())):
        return  # Only plot if both exist

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

    plt.savefig(output_dir / f"{target}_relative_performance.png", bbox_inches="tight")
    plt.close()


def main():
    df = load_data()

    output_dir = Path(__file__).resolve().parents[1] / "plots"
    output_dir.mkdir(exist_ok=True)

    for target in df["target"].unique():
        plot_time_vs_workers(df, target, output_dir)
        plot_time_vs_timeout(df, target, output_dir)
        plot_relative_performance(df, target, output_dir)

    print("Benchmark plots generated successfully.")


if __name__ == "__main__":
    main()