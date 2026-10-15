"""
8.1_throughput_vs_arrival_rate_by_hubcount.py — edit-and-rerun figure
generator for the 8.1_throughput_vs_arrival_rate_by_hubcount figure
(system throughput vs. request arrival rate, one line per fleet size,
log-x, with 95% CI bands).

This does NOT read from simulation/results/ or touch any live component.
It reads only 8.1_throughput_vs_arrival_rate_by_hubcount_data.json
(sitting next to this script) so you can freely tweak figure size / font
size / colors below and rerun in seconds, without needing the simulator.

Usage:
    python 8.1_throughput_vs_arrival_rate_by_hubcount.py
    (or: prototype/.venv/bin/python simulation_figures/8.1_throughput_vs_arrival_rate_by_hubcount.py)

Output:
    8.1_throughput_vs_arrival_rate_by_hubcount.png   (next to this script
    — same filename as the figure used everywhere else; never renamed,
    PNG only, no PDF)
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

SERIES_STYLE = {
    "hubs4":  {"color": "#0072B2", "marker": "o"},
    "hubs8":  {"color": "#E69F00", "marker": "s"},
    "hubs16": {"color": "#D55E00", "marker": "^"},
}
CI_BAND_ALPHA     = 0.15
LINE_WIDTH        = 2.2
MARKER_SIZE       = 8

GRID_ON           = True
GRID_ALPHA        = 0.4

LEGEND_LOC             = "upper left"
LEGEND_BBOX_TO_ANCHOR  = (0.02, 0.83)

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
DATA_PATH = os.path.join(HERE, "8.1_throughput_vs_arrival_rate_by_hubcount_data.json")
OUT_PNG = os.path.join(HERE, "8.1_throughput_vs_arrival_rate_by_hubcount.png")


def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH_IN, FIGURE_HEIGHT_IN),
                            constrained_layout=True)

    for key in ("hubs4", "hubs8", "hubs16"):
        series = data[key]
        style = SERIES_STYLE[key]
        xs = series["arrival_rate"]
        ys = series["throughput_tps"]
        ax.plot(xs, ys, marker=style["marker"], color=style["color"],
                 label=series["label"])
        lo = series.get("throughput_tps_ci_lo")
        hi = series.get("throughput_tps_ci_hi")
        if lo and hi:
            ax.fill_between(xs, lo, hi, color=style["color"],
                             alpha=CI_BAND_ALPHA, linewidth=0)

    ax.set_xscale("log")
    ax.set_xlabel("Arrival Rate (req/sec)")
    ax.set_ylabel("Throughput (tokens/sec)")
    ax.set_ylim(bottom=0)
    ax.legend(loc=LEGEND_LOC, bbox_to_anchor=LEGEND_BBOX_TO_ANCHOR)

    fig.savefig(OUT_PNG, bbox_inches="tight", dpi=SAVE_DPI)
    plt.close(fig)
    print(f"Saved -> {OUT_PNG}")


if __name__ == "__main__":
    main()
