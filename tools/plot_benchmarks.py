import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def load_data():
    root_dir = Path(__file__).resolve().parents[2]

    python_csv = root_dir / "port-scanner" / "results" / "benchmarks.csv"
    go_csv = root_dir / "port-scanner-go" / "results" / "benchmarks.csv"

    print("Loading from:")
    print("Python:", python_csv)
    print("Go:", go_csv)

    py_df = pd.read_csv(python_csv)
    go_df = pd.read_csv(go_csv)

    df = pd.concat([py_df, go_df], ignore_index=True)

    # Normalize column names
    df.columns = df.columns.str.strip().str.lower()

    # Normalize language
    df["lang"] = df["lang"].astype(str).str.strip().str.lower()

    # Safe numeric conversion
    df["workers"] = pd.to_numeric(df["workers"], errors="coerce")
    df["timeout_s"] = pd.to_numeric(df["timeout_s"], errors="coerce")
    df["total_time_s"] = pd.to_numeric(df["total_time_s"], errors="coerce")

    df = df.dropna(subset=["workers", "timeout_s", "total_time_s"])

    df["workers"] = df["workers"].astype(int)
    df["timeout_s"] = df["timeout_s"].astype(int)

    print("\nLanguage counts after merge:")
    print(df["lang"].value_counts())

    return df


def plot_time_vs_workers(df, target, output_dir):
    target_df = df[df["target"] == target]

    for timeout in sorted(target_df["timeout_s"].unique()):
        subset = target_df[target_df["timeout_s"] == timeout]

        plt.figure(figsize=(10, 6), dpi=130)

        for i, lang in enumerate(sorted(subset["lang"].unique())):
            lang_data = subset[subset["lang"] == lang].sort_values("workers")

            # Slight visual offset to prevent perfect overlap
            x_values = lang_data["workers"] + (i * 2)

            plt.plot(
                x_values,
                lang_data["total_time_s"],
                marker="o",
                linewidth=2.5,
                markersize=7,
                label=lang.capitalize()
            )

        plt.xlabel("Number of Workers", fontsize=12)
        plt.ylabel("Total Scan Time (seconds)", fontsize=12)
        plt.title(f"{target} | Timeout={timeout}s | Time vs Workers", fontsize=14)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)

        plt.savefig(output_dir / f"{target}_timeout_{timeout}_time_vs_workers.png", bbox_inches="tight")
        plt.close()


def plot_time_vs_timeout(df, target, output_dir):
    target_df = df[df["target"] == target]

    plt.figure(figsize=(10, 6), dpi=130)

    for lang in sorted(target_df["lang"].unique()):
        lang_data = target_df[target_df["lang"] == lang]
        grouped = lang_data.groupby("timeout_s")["total_time_s"].mean().reset_index()

        plt.plot(
            grouped["timeout_s"],
            grouped["total_time_s"],
            marker="o",
            linewidth=2.5,
            markersize=7,
            label=lang.capitalize()
        )

    plt.xlabel("Timeout (seconds)", fontsize=12)
    plt.ylabel("Average Total Scan Time (seconds)", fontsize=12)
    plt.title(f"{target} | Time vs Timeout", fontsize=14)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)

    plt.savefig(output_dir / f"{target}_time_vs_timeout.png", bbox_inches="tight")
    plt.close()


def plot_relative_performance(df, target, output_dir):
    target_df = df[df["target"] == target]

    if not {"python", "go"}.issubset(set(target_df["lang"].unique())):
        return

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

    plt.figure(figsize=(10, 6), dpi=130)

    plt.plot(
        merged["workers"],
        merged["performance_ratio"],
        marker="o",
        linewidth=2.5,
        markersize=7
    )

    plt.axhline(y=1.0, linestyle="--", linewidth=1.5)
    plt.ylim(0.95, 1.05)  # Zoom for clarity

    plt.xlabel("Number of Workers", fontsize=12)
    plt.ylabel("Python / Go Execution Time Ratio", fontsize=12)
    plt.title(f"{target} | Relative Performance (Ratio > 1 ⇒ Go Faster)", fontsize=14)
    plt.grid(True, alpha=0.3)

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