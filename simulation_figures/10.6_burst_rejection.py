"""
10.6_burst_rejection.py — edit-and-rerun figure generator for the
10.6_burst_rejection figure (burst-region rejection rate time-series
through a regional burst window, one line per routing strategy, with
95% CI bands and a shaded burst window).

This does NOT read from simulation/results/ or touch any live component.
It reads only 10.6_burst_rejection_data.json (sitting next to this
script) so you can freely tweak figure size / font size / colors below
and rerun in seconds, without needing the simulator.

Usage:
    python 10.6_burst_rejection.py
    (or: prototype/.venv/bin/python simulation_figures/10.6_burst_rejection.py)

Output:
    10.6_burst_rejection.png   (next to this script — same filename as
    the figure used everywhere else; never renamed, PNG only, no PDF)
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

VARIANT_COLORS = {
    "nearest":       "#0072B2",
    "load_balanced": "#009E73",
    "centralized":   "#D55E00",
}


VARIANT_LEGEND_LABELS = {
    "nearest":       "SPECIE(Nearest)",
    "load_balanced": "SPECIE(Balanced)",
    "centralized":   "Centralized",
}


BURST_WINDOW_LABEL = "10\u00d7 Arrival Burst"

BURST_WINDOW_COLOR = "red"
BURST_WINDOW_ALPHA = 0.08

CI_BAND_ALPHA     = 0.15
LINE_WIDTH        = 2.2

GRID_ON           = True
GRID_ALPHA        = 0.4

LEGEND_LOC        = "upper left"
YLIM_HEADROOM_MULT = 1.35   # extra headroom above the data max so the
                             # top-left legend never overlaps a rising curve

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
DATA_PATH = os.path.join(HERE, "10.6_burst_rejection_data.json")
OUT_PNG = os.path.join(HERE, "10.6_burst_rejection.png")


def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    burst_window = data["burst_window_s"]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH_IN, FIGURE_HEIGHT_IN),
                            constrained_layout=True)

    for variant in ("nearest", "load_balanced", "centralized"):
        vd = data[variant]
        ts = vd["timestamps_s"]
        ys = vd["rejection_rate"]
        color = VARIANT_COLORS[variant]
        ls = "--" if variant == "centralized" else "-"
        ax.plot(ts, ys, color=color, linestyle=ls,
                 label=VARIANT_LEGEND_LABELS[variant])
        lo = vd.get("rejection_rate_ci_lo")
        hi = vd.get("rejection_rate_ci_hi")
        if lo and hi:
            ax.fill_between(ts, lo, hi, color=color, alpha=CI_BAND_ALPHA, linewidth=0)

    ax.axvspan(*burst_window, alpha=BURST_WINDOW_ALPHA, color=BURST_WINDOW_COLOR,
               label=BURST_WINDOW_LABEL)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))
    ax.set_xlabel("Simulation Time (s)")
    ax.set_ylabel("Rejection Rate")

    ylo, yhi = ax.get_ylim()
    ax.set_ylim(ylo, ylo + (yhi - ylo) * YLIM_HEADROOM_MULT)
    ax.legend(loc=LEGEND_LOC, framealpha=1.0)

    fig.savefig(OUT_PNG, bbox_inches="tight", dpi=SAVE_DPI)
    plt.close(fig)
    print(f"Saved -> {OUT_PNG}")


if __name__ == "__main__":
    main()
