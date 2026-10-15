"""
eviction_efficiency_box.py — edit-and-rerun figure generator for the
eviction_efficiency_box figure (KV lease occupancy box plots: hook ON vs.
OFF, each pre-attack vs. post-attack, with mean markers and a fold-increase
annotation over the OFF pair).

This does NOT read from prototype/results/ or touch any live component.
It reads only eviction_efficiency_box_data.json (sitting next to this
script) so you can freely tweak figure size / font size / colors below
and rerun in seconds, without needing the prototype's venv or GPU.

Usage:
    python eviction_efficiency_box.py
    (or: prototype/.venv/bin/python prototype_figures/eviction_efficiency_box.py)

Output:
    eviction_efficiency_box.png   (next to this script — same filename as
    the figure used everywhere else; never renamed, PNG only, no PDF)
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

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

BOX_COLORS         = ["#a9c6ec", "#7fb3e6", "#f0b8a8", "#e8785f"]
MEAN_MARKER_COLORS = ["#1a3a6b", "#1a3a6b", "#8a2e1c", "#8a2e1c"]
BRACKET_COLOR       = "#8a2e1c"

BOX_WIDTH         = 0.55
MEAN_MARKER_SIZE  = 11
XTICK_ROTATION    = 0    # labels are now short ("Pre"/"Post") since the
                          # ON/OFF distinction moved into the legend, so
                          # no rotation is needed to avoid collisions

GRID_ON           = True
GRID_ALPHA        = 0.30

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
DATA_PATH = os.path.join(HERE, "eviction_efficiency_box_data.json")
OUT_PNG = os.path.join(HERE, "eviction_efficiency_box.png")


def main():
    with open(DATA_PATH) as f:
        d = json.load(f)

    groups = ["Pre", "Post", "Pre", "Post"]
    data = [d["on_pre"], d["on_post"], d["off_pre"], d["off_post"]]
    means = [float(np.mean(g)) for g in data]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH_IN, FIGURE_HEIGHT_IN),
                            constrained_layout=True)
    xs = np.arange(1, 5)
    bp = ax.boxplot(data, positions=xs, patch_artist=True, widths=BOX_WIDTH,
                     medianprops={"color": "black", "linewidth": 1.4},
                     whiskerprops={"color": "black", "linewidth": 1.1},
                     capprops={"color": "black", "linewidth": 1.1},
                     flierprops={"marker": "o", "markersize": 3, "alpha": 0.35},
                     boxprops={"linewidth": 1.1})
    for patch, color in zip(bp["boxes"], BOX_COLORS):
        patch.set_facecolor(color)
        patch.set_edgecolor("black")

    for x, m, c in zip(xs, means, MEAN_MARKER_COLORS):
        ax.plot(x, m, marker="D", markersize=MEAN_MARKER_SIZE, color=c, zorder=5)

    fold_off = means[3] / means[2] if means[2] else float("nan")
    top = max(max(g) for g in data)
    bracket_y = top * 1.08
    ax.plot([3, 3, 4, 4], [top * 1.02, bracket_y, bracket_y, top * 1.02],
            color=BRACKET_COLOR, linewidth=1.0, linestyle="--")
    ax.annotate(f"{fold_off:.2f}× mean", (3.5, bracket_y),
                xytext=(0, 4), textcoords="offset points",
                ha="center", fontweight="bold", color=BRACKET_COLOR)

    ax.set_xticks(xs, groups, rotation=XTICK_ROTATION,
                  ha="right" if XTICK_ROTATION else "center")
    ax.set_ylabel("KV Blocks Held")
    ax.set_ylim(0, top * 1.25)

    legend_elems = [
        Patch(facecolor=BOX_COLORS[1], edgecolor="black",
              label="Eviction Hook ON"),
        Patch(facecolor=BOX_COLORS[3], edgecolor="black",
              label="Eviction Hook OFF"),
        plt.Line2D([0], [0], marker="s", markersize=12, color="none",
                   markerfacecolor="none", markeredgecolor="black",
                   markeredgewidth=1.1, label="Interquartile Range (Median)"),
        plt.Line2D([0], [0], marker="D", markersize=8, color="none",
                   markerfacecolor="#1a3a6b", label="Mean"),
    ]
    ax.legend(handles=legend_elems, loc="upper left", framealpha=0.9)

    fig.savefig(OUT_PNG, bbox_inches="tight", dpi=SAVE_DPI)
    plt.close(fig)
    print(f"Saved -> {OUT_PNG}")
    print(f"ON:  pre_mean={means[0]:.2f} post_mean={means[1]:.2f}")
    print(f"OFF: pre_mean={means[2]:.2f} post_mean={means[3]:.2f} fold={fold_off:.2f}x")


if __name__ == "__main__":
    main()
