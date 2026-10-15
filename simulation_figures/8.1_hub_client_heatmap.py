"""
8.1_hub_client_heatmap.py — edit-and-rerun figure generator for the
8.1_hub_client_heatmap figure (mean throughput heatmap over hub count x
concurrent client count, with per-cell value labels).

This does NOT read from simulation/results/ or touch any live component.
It reads only 8.1_hub_client_heatmap_data.json (sitting next to this
script) so you can freely tweak figure size / font size / colors below
and rerun in seconds, without needing the simulator.

Usage:
    python 8.1_hub_client_heatmap.py
    (or: prototype/.venv/bin/python simulation_figures/8.1_hub_client_heatmap.py)

Output:
    8.1_hub_client_heatmap.png   (next to this script — same filename as
    the figure used everywhere else; never renamed, PNG only, no PDF)
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

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
CELL_LABEL_FONT_SIZE = 14    # per-cell numeric value text
CELL_LABEL_COLOR     = "black"  # set to None to auto-switch white/black by
                                 # cell brightness instead of a fixed color
COLORBAR_LABEL_SIZE  = 18
COLORBAR_TICK_SIZE   = 16

BOLD_EVERYTHING   = True     # axis labels, tick labels

# Material Design "blue" shade ramp (50 -> 900), light to dark, used to
# build a custom sequential colormap instead of matplotlib's default
# viridis (which reads as clashing/odd next to the rest of this paper's
# blue-centric palette).
BLUE_SHADES = [
    "#E3F2FD",  # blue 50
    "#BBDEFB",  # blue 100
    "#90CAF9",  # blue 200
    "#64B5F6",  # blue 300
    "#42A5F5",  # blue 400
    "#2196F3",  # blue (500)
    "#1E88E5",  # blue 600
    "#1976D2",  # blue 700
    "#1565C0",  # blue 800
    "#0D47A1",  # blue 900
]

COLOR_SCALE       = "log"    # "log" or "linear" — the throughput values
                              # span 49 to ~3579 (roughly 70x), so a linear
                              # color scale crushes every low-throughput
                              # cell (small hub/client counts) into the
                              # same palest 1-2 shades. "log" spreads that
                              # low end out so those cells get visibly
                              # distinct, progressively deeper colors too.

GRID_ON           = False    # heatmaps read better without a background grid

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
    "figure.dpi":         200,
    "savefig.dpi":        SAVE_DPI,
    "savefig.bbox":       "tight",
    "axes.grid":          GRID_ON,
})

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "8.1_hub_client_heatmap_data.json")
OUT_PNG = os.path.join(HERE, "8.1_hub_client_heatmap.png")


def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    hub_values = data["hub_values"]
    client_values = data["client_values"]
    matrix_tps = data["matrix_tps"]

    m = np.zeros((len(client_values), len(hub_values)))
    for ci, c in enumerate(client_values):
        for hi, h in enumerate(hub_values):
            m[ci, hi] = matrix_tps[str(c)][str(h)]

    cmap = LinearSegmentedColormap.from_list("blue_shades", BLUE_SHADES)
    norm = matplotlib.colors.LogNorm() if COLOR_SCALE == "log" else None

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH_IN, FIGURE_HEIGHT_IN),
                            constrained_layout=True)
    im = ax.imshow(m, origin="lower", cmap=cmap, norm=norm, aspect="auto")
    ax.set_xticks(range(len(hub_values)))
    ax.set_xticklabels(hub_values)
    ax.set_yticks(range(len(client_values)))
    ax.set_yticklabels(client_values)
    ax.set_xlabel("Number of Hubs")
    ax.set_ylabel("Concurrent Clients")


    for ci in range(len(client_values)):
        for hi in range(len(hub_values)):
            v = m[ci, hi]
            label = f"{round(v/1000)}k" if v >= 1000 else f"{v:.0f}"
            color = CELL_LABEL_COLOR
            if color is None:
                normed = norm(v) if norm is not None else v / m.max()
                color = "white" if normed < 0.6 else "black"
            ax.text(hi, ci, label, ha="center", va="center",
                     color=color, fontsize=CELL_LABEL_FONT_SIZE, fontweight="bold")

    cbar = fig.colorbar(im, ax=ax, fraction=0.08, pad=0.06, location="bottom")
    cbar.set_label("Mean throughput (tokens/s)", fontsize=COLORBAR_LABEL_SIZE,
                    fontweight="bold" if BOLD_EVERYTHING else "normal")
    cbar.ax.tick_params(labelsize=COLORBAR_TICK_SIZE)

    fig.savefig(OUT_PNG, bbox_inches="tight", dpi=SAVE_DPI)
    plt.close(fig)
    print(f"Saved -> {OUT_PNG}")


if __name__ == "__main__":
    main()
