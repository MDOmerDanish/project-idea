"""
4.3_cheating_hub_economics.py — edit-and-rerun figure generator for the
4.3_cheating_hub_economics figure (total payment received: naive flat-fee
reference vs. honest Hub vs. cheating Hub).

This does NOT read from prototype/results/ or touch any live component.
It reads only 4.3_cheating_hub_economics_data.json (sitting next to this
script) so you can freely tweak figure size / font size / colors below
and rerun in seconds, without needing the prototype's venv or GPU.

Usage:
    python 4.3_cheating_hub_economics.py
    (or: prototype/.venv/bin/python prototype_figures/4.3_cheating_hub_economics.py)

Output:
    4.3_cheating_hub_economics.png   (next to this script — same filename
    as the figure used everywhere else; never renamed, PNG only, no PDF)
"""
import json
import math
import os

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
LEGEND_FONT_SIZE  = 15       # legend entries (3 entries, long labels)
BAR_LABEL_FONT_SIZE = 15     # the "$x.xx x 10^-n" / "Nx less" text above bars

BOLD_EVERYTHING   = True     # axis labels, tick labels, legend text

GREY       = "#8A8A8A"   # naive flat-fee reference (no verification)
BLUE       = "#0072B2"   # honest hub
VERMILLION = "#D55E00"   # cheating hub

BAR_WIDTH         = 0.55
BAR_ALPHA         = 0.9

GRID_ON           = True
GRID_ALPHA        = 0.4

LEGEND_LOC             = "upper right"
LEGEND_BBOX_TO_ANCHOR  = (.50, 1.00)   # pushed above the axes; increase the
                                        # 2nd number to push it further up

YLIM_HEADROOM_MULT = 1.85   # ylim_top = naive_fee * this
LABEL_OFFSET_MULT  = 0.03   # label_offset = ylim_top * this

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
DATA_PATH = os.path.join(HERE, "4.3_cheating_hub_economics_data.json")
OUT_PNG = os.path.join(HERE, "4.3_cheating_hub_economics.png")


def sci_label(v):
    """Format a small dollar amount as '$a.ab x 10^-n' using matplotlib
    mathtext superscript syntax (not Unicode superscript chars, which most
    text fonts including Nimbus Roman don't fully cover)."""
    if v == 0:
        return "$0"
    exp = math.floor(math.log10(abs(v)))
    mant = v / (10 ** exp)
    return f"\\${mant:.2f}$\\times$10$^{{{exp}}}$"


def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    price = data["price_per_token_usd"]
    honest = data["honest"]
    cheating = data["cheating"]

    honest_usd = honest["tokens_paid"] * price
    cheating_usd = cheating["tokens_paid"] * price
    naive_fee = honest["total_gamma_requested"] * price

    xs = [0, 1, 2]
    values = [naive_fee, honest_usd, cheating_usd]
    colors = [GREY, BLUE, VERMILLION]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH_IN, FIGURE_HEIGHT_IN),
                            constrained_layout=True)
    bars = ax.bar(xs, values, color=colors, alpha=BAR_ALPHA, width=BAR_WIDTH,
                   zorder=3)
    ax.set_xticks([])   # identity carried by the legend only

    ylim_top = naive_fee * YLIM_HEADROOM_MULT
    label_offset = ylim_top * LABEL_OFFSET_MULT

    for bar, v in zip(bars, values):
        label = sci_label(v)
        if v != naive_fee:
            label += f"\n{naive_fee / v:.1f}x less"
        ax.text(bar.get_x() + bar.get_width() / 2, v + label_offset, label,
                ha="center", fontsize=BAR_LABEL_FONT_SIZE, linespacing=1.3)

    legend_handles = [
        Patch(facecolor=GREY, alpha=BAR_ALPHA, label="Flat fee naive decoding"),
        Patch(facecolor=BLUE, alpha=BAR_ALPHA, label="SPECIE honest Hub"),
        Patch(facecolor=VERMILLION, alpha=BAR_ALPHA, label="SPECIE cheating Hub"),
    ]




    ax.legend(handles=legend_handles, loc=LEGEND_LOC,
              bbox_to_anchor=LEGEND_BBOX_TO_ANCHOR, frameon=True)


    ax.set_ylabel("Payment Received")

    ax.set_ylim(0, ylim_top)

    fig.savefig(OUT_PNG, bbox_inches="tight", dpi=SAVE_DPI)
    plt.close(fig)
    print(f"Saved -> {OUT_PNG}")


if __name__ == "__main__":
    main()
