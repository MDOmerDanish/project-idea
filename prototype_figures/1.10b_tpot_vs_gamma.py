"""
1.10b_tpot_vs_gamma.py — edit-and-rerun figure generator for the
1.10b_tpot_vs_gamma figure (TPOT mean/P50/P95 vs. gamma, with acceptance
rate on a secondary axis).

This does NOT read from prototype/results/ or touch any live component.
It reads only 1.10b_tpot_vs_gamma_data.json (sitting next to this script)
so you can freely tweak figure size / font size / colors below and rerun
in seconds, without needing the prototype's venv or GPU.

Usage:
    python 1.10b_tpot_vs_gamma.py
    (or: prototype/.venv/bin/python prototype_figures/1.10b_tpot_vs_gamma.py)

Output:
    1.10b_tpot_vs_gamma.png   (next to this script — same filename as the
    figure used everywhere else; never renamed, PNG only, no PDF)
"""
import json
import os

import numpy as np
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

METRIC_COLOR      = "#c9662f"   # TPOT lines
ACCEPT_COLOR      = "#7B3294"   # acceptance-rate line (secondary axis)

STAT_STYLE = {
    "mean": {"linestyle": "-",  "marker": "o"},
    "p50":  {"linestyle": "--", "marker": "s"},
    "p95":  {"linestyle": ":",  "marker": "^"},
}
LINE_WIDTH        = 2.2
MARKER_SIZE       = 9

GRID_ON           = True
GRID_ALPHA        = 0.30

LEGEND_LOC             = "center right"
LEGEND_BBOX_TO_ANCHOR  = (0.98, 0.62)   # sits in the empty gap between the
                                         # P95 dotted curve (above) and the
                                         # mean/P50 curves (below), clear of
                                         # every line instead of overlapping
                                         # the top-left corner

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
    "axes.linewidth":     1.5,
})

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "1.10b_tpot_vs_gamma_data.json")
OUT_PNG = os.path.join(HERE, "1.10b_tpot_vs_gamma.png")


def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    gammas = data["gammas"]
    xs = np.arange(len(gammas))
    tpot = {g: data["tpot_ms"][str(g)] for g in gammas}
    accept_rate = [data["acceptance_rate"][str(g)] for g in gammas]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH_IN, FIGURE_HEIGHT_IN),
                            constrained_layout=True)

    lines = []
    for stat_key, stat_label in (("mean", "Mean"), ("p50", "P50"), ("p95", "P95")):
        style = STAT_STYLE[stat_key]
        ys = [tpot[g][stat_key] for g in gammas]
        p, = ax.plot(xs, ys, color=METRIC_COLOR, linestyle=style["linestyle"],
                     marker=style["marker"], label=f" {stat_label}")
        lines.append(p)

    ax.set_xticks(xs, [str(g) for g in gammas])
    ax.set_xlabel(r"$\gamma$ (Speculative Batch Size)")
    ax.set_ylabel("TPOT (ms)")

    ax2 = ax.twinx()
    p_accept, = ax2.plot(xs, accept_rate, color=ACCEPT_COLOR, linestyle="-.",
                         marker="D", label="Acceptance Rate")
    ax2.set_ylabel("Acceptance Rate", color="black")
    ax2.tick_params(axis="y", labelcolor="black")
    ax2.set_ylim(0.0, 1.0)
    ax2.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: f"{y:.0%}"))
    ax2.grid(False)
    lines.append(p_accept)

    ax.legend(lines, [l.get_label() for l in lines], loc=LEGEND_LOC,
              bbox_to_anchor=LEGEND_BBOX_TO_ANCHOR, ncol=1, frameon=False)

    fig.savefig(OUT_PNG, bbox_inches="tight", dpi=SAVE_DPI)
    plt.close(fig)
    print(f"Saved -> {OUT_PNG}")


if __name__ == "__main__":
    main()
