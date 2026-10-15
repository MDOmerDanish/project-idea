"""
2.1_gamma_config_tradeoff.py — edit-and-rerun figure generator for the
2.1_gamma_config_tradeoff figure (draft throughput vs. gamma, CPU vs. GPU,
TinyLlama-1.1B baseline vs. Llama-3.2-1B optimized config).

This does NOT read from prototype/results/ or touch any live component.
It reads only 2.1_gamma_config_tradeoff_data.json (sitting next to this
script) so you can freely tweak figure size / font size / colors below
and rerun in seconds, without needing the prototype's venv or GPU.

Usage:
    python 2.1_gamma_config_tradeoff.py
    (or: prototype/.venv/bin/python prototype_figures/2.1_gamma_config_tradeoff.py)

Output:
    2.1_gamma_config_tradeoff.png   (next to this script — same filename
    as the figure used everywhere else; never renamed, PNG only, no PDF)
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ============================================================
#  EVERYTHING YOU'D WANT TO TRY-AND-ERROR IS IN THIS ONE BLOCK
# ============================================================

FIGURE_WIDTH_IN   = 7.0     # inches
FIGURE_HEIGHT_IN  = 4.5     # inches

FONT_FAMILY       = "serif"
FONT_NAME         = "Nimbus Roman"   # Times-New-Roman-compatible font that
                                     # actually HAS a real bold face on this
                                     # machine (fc-list | grep -i "nimbus roman").
                                     # Plain "Times New Roman" only has a
                                     # regular weight installed here, so
                                     # bold text silently falls back to
                                     # regular if you use that name instead.

BASE_FONT_SIZE    = 20       # font.size (fallback for anything not listed below)
AXIS_LABEL_SIZE   = 22       # x/y axis label text
TICK_LABEL_SIZE   = 20       # the numbers along each axis
LEGEND_FONT_SIZE  = 16       # legend entries

BOLD_EVERYTHING   = True     # axis labels, tick labels, legend text

BLUE   = "#0072B2"   # CPU draft (edge-device baseline)
ORANGE = "#D55E00"   # GPU draft (local accelerator)

LINE_WIDTH        = 2.2
MARKER_SIZE       = 8
PEAK_MARKER_SIZE  = 130   # star marker on each series' peak

GRID_ON           = True
GRID_ALPHA        = 0.4

LEGEND_LOC             = "upper left"
LEGEND_BBOX_TO_ANCHOR  = (0.45,0.65)   # e.g. (0.5, -0.24) to pin below the axes
LEGEND_HANDLELENGTH    = 2.2



SAVE_DPI          = 300

# ============================================================
#  END OF TRY-AND-ERROR BLOCK — nothing below this line needs
#  editing to change how the figure looks
# ============================================================

plt.rcParams.update({
    "font.family":        FONT_FAMILY,
    "font.serif":         [FONT_NAME],
    "font.size":          BASE_FONT_SIZE,
    "font.weight":        "bold" if BOLD_EVERYTHING else "normal",
    "axes.titlesize":     BASE_FONT_SIZE,
    "axes.titleweight":   "bold" if BOLD_EVERYTHING else "normal",
    "axes.labelsize":     AXIS_LABEL_SIZE,
    "axes.labelweight":   "bold" if BOLD_EVERYTHING else "normal",
    "xtick.labelsize":    TICK_LABEL_SIZE,
    "ytick.labelsize":    TICK_LABEL_SIZE,
    "legend.fontsize":    LEGEND_FONT_SIZE,
    "legend.framealpha":  0.85,
    "lines.linewidth":    LINE_WIDTH,
    "lines.markersize":   MARKER_SIZE,
    "figure.dpi":         200,
    "savefig.dpi":        SAVE_DPI,
    "savefig.bbox":       "tight",
    "axes.grid":          GRID_ON,
    "grid.linestyle":     "--",
    "grid.alpha":         GRID_ALPHA,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.linewidth":     1.5,
})

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "2.1_gamma_config_tradeoff_data.json")
OUT_PNG = os.path.join(HERE, "2.1_gamma_config_tradeoff.png")


def plot_series(ax, gammas, tps, color, linestyle, marker, label):
    if not tps:
        return
    ax.plot(gammas, tps, marker=marker, color=color, linestyle=linestyle,
            alpha=(1.0 if linestyle == "-" else 0.55), label=label)
    peak_i = max(range(len(tps)), key=lambda i: tps[i])
    ax.scatter([gammas[peak_i]], [tps[peak_i]], color=color,
               s=PEAK_MARKER_SIZE, zorder=5, marker="*")


def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    gammas = data["gammas"]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH_IN, FIGURE_HEIGHT_IN),
                            constrained_layout=True)

    plot_series(ax, gammas, data["cpu_tinyllama_tokps"], BLUE, "--", "o",
                "CPU (TinyLlama-1.1B)")
    plot_series(ax, gammas, data["gpu_tinyllama_tokps"], ORANGE, "--", "s",
                "GPU (TinyLlama-1.1B)")
    plot_series(ax, gammas, data["cpu_llama32_tokps"], BLUE, "-", "o",
                "CPU (Llama-3.2-1B)")
    plot_series(ax, gammas, data["gpu_llama32_tokps"], ORANGE, "-", "s",
                "GPU (Llama-3.2-1B)")

    ax.set_xlabel(r"$\gamma$ (Speculative Batch Size)")
    ax.set_ylabel("Throughput (tokens/s)")
    ax.set_xticks(gammas)
    ax.legend(loc=LEGEND_LOC, bbox_to_anchor=LEGEND_BBOX_TO_ANCHOR, ncol=1,
              handlelength=LEGEND_HANDLELENGTH)

    fig.savefig(OUT_PNG, bbox_inches="tight", dpi=SAVE_DPI)
    plt.close(fig)
    print(f"Saved -> {OUT_PNG}")


if __name__ == "__main__":
    main()
