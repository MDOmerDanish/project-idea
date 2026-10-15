"""
2.2b_batching_speedup.py — edit-and-rerun figure generator for Figure 2.2b
(SPECIE throughput per gamma vs. naive autoregressive decoding).

This does NOT read from prototype/results/ or touch any live component.
It reads only 2.2b_batching_speedup_data.json (sitting next to this script)
so you can freely tweak figure size / font size / colors below and rerun
in seconds, without needing the prototype's venv or GPU.

Usage:
    python 2.2b_batching_speedup.py
    (or: prototype/.venv/bin/python prototype_figures/2.2b_batching_speedup.py)

Output:
    2.2b_batching_speedup.png  (next to this script — same filename as the
    figure used everywhere else; never renamed, PNG only, no PDF)
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
AXIS_LABEL_SIZE   = 22       # x/y axis label text (e.g. "Throughput (tokens/s)")
TICK_LABEL_SIZE   = 20       # the numbers along each axis
LEGEND_FONT_SIZE  = 18       # legend entries

BOLD_EVERYTHING   = True     # axis labels, tick labels, legend text

LINE_WIDTH        = 2.2      # the dashed AR baseline line
MARKER_SIZE       = 8        # unused here (no markers in a bar chart), kept
                              # for parity with the other figure scripts
BAR_WIDTH         = 0.6
BAR_ALPHA         = 0.55

BLUE = "#0072B2"   # SPECIE bars (Okabe-Ito colorblind-safe palette)
GREY = "#8A8A8A"   # naive-AR reference line

GRID_ON           = True
GRID_ALPHA        = 0.35

LEGEND_LOC             = "upper center"
LEGEND_BBOX_TO_ANCHOR  = (0.5, 1.18)   # push legend above the axes; increase
                                        # the 2nd number to push it further up

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
    "legend.framealpha":  0.9,
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
DATA_PATH = os.path.join(HERE, "2.2b_batching_speedup_data.json")


def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    gammas = data["gammas"]
    gpu_tps = [data["specie_throughput_tokps"][str(g)] for g in gammas]
    ar_tps = data["naive_ar_throughput_tokps"]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH_IN, FIGURE_HEIGHT_IN),
                            constrained_layout=True)

    ax.bar(gammas, gpu_tps, color=BLUE, alpha=BAR_ALPHA, width=BAR_WIDTH,
           zorder=2, label="SPECIE")

    ax.axhline(ar_tps, color=GREY, linestyle="--", linewidth=LINE_WIDTH,
               zorder=1, label=f"Naive autoregressive decoding ({ar_tps:.2f} tok/s)")

    ax.set_xlabel(r"$\gamma$ (Speculative Batch Size)",
                  fontweight="bold" if BOLD_EVERYTHING else "normal")
    ax.set_ylabel("Throughput (tokens/s)",
                  fontweight="bold" if BOLD_EVERYTHING else "normal")
    ax.set_xticks(gammas)
    ax.set_ylim(0, max(gpu_tps) * 1.1)

    if BOLD_EVERYTHING:
        for label in ax.get_xticklabels() + ax.get_yticklabels():
            label.set_fontweight("bold")

    ax.legend(loc=LEGEND_LOC, bbox_to_anchor=LEGEND_BBOX_TO_ANCHOR, ncol=1)

    out_png = os.path.join(HERE, "2.2b_batching_speedup.png")
    fig.savefig(out_png, bbox_inches="tight", dpi=SAVE_DPI)
    plt.close(fig)
    print(f"Saved -> {out_png}")


if __name__ == "__main__":
    main()
