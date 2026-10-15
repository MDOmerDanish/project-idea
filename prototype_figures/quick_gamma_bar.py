"""
quick_gamma_bar.py — edit-and-rerun figure generator for the quick_gamma_bar
figure (latency component breakdown per gamma: draft, verification,
protocol, stacked total, and amortized per-token latency).

This does NOT read from prototype/results/ or touch any live component.
It reads only quick_gamma_bar_data.json (sitting next to this script) so
you can freely tweak figure size / font size / colors below and rerun in
seconds, without needing the prototype's venv or GPU.

Usage:
    python quick_gamma_bar.py
    (or: prototype/.venv/bin/python prototype_figures/quick_gamma_bar.py)

Output:
    quick_gamma_bar.png   (next to this script — same filename as the
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
AXIS_LABEL_SIZE   = 22       # x/y axis label text (e.g. "Latency (ms)")
TICK_LABEL_SIZE   = 20       # the numbers along each axis
LEGEND_FONT_SIZE  = 16       # legend entries (4 entries, so kept a bit
                              # smaller than the axis text to help it fit)

BOLD_EVERYTHING   = True     # axis labels, tick labels, legend text

BAR_GROUP_WIDTH   = 0.15     # width of each individual bar within a gamma group
BAR_EDGE_LINEWIDTH = 0.6

STAGE_COLORS = {
    "draft":     "#4c72b0",
    "verify":    "#c9662f",
    "protocol":  "#0e9488",
    "per_token": "#b04c72",
}

PAYMENT_LABEL_FONT_SIZE = 11   # the "0.68" etc. text drawn above the
                                # payment bars, since those bars are only
                                # ~0.6-0.8ms tall and invisible against a
                                # ~230ms axis otherwise
PAYMENT_LABEL_DECIMALS  = 2

GRID_ON           = True
GRID_ALPHA        = 0.30

LEGEND_LOC             = "upper left"
LEGEND_BBOX_TO_ANCHOR  = (0.0, 1.00)   # pushes the legend above the axes
                                        # entirely, clear of the tall
                                        # verification bars it used to
                                        # overlap when placed inside the
                                        # plot area; increase the 2nd
                                        # number to push it further up

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
DATA_PATH = os.path.join(HERE, "quick_gamma_bar_data.json")
OUT_PNG = os.path.join(HERE, "quick_gamma_bar.png")


def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    gammas = data["gammas"]
    results = {int(g): v for g, v in data["results"].items()}

    xs = np.arange(len(gammas))
    width = BAR_GROUP_WIDTH

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH_IN, FIGURE_HEIGHT_IN),
                            constrained_layout=True)

    draft_vals = [results[g]["draft_ms"] for g in gammas]
    verify_vals = [results[g]["verify_ms"] for g in gammas]
    protocol_vals = [results[g]["protocol_ms"] for g in gammas]
    per_token_vals = [results[g]["per_token_ms"] for g in gammas]

    ax.bar(xs - 1.5 * width, draft_vals, width,
           label="Drafting/round", color=STAGE_COLORS["draft"],
           edgecolor="white", linewidth=BAR_EDGE_LINEWIDTH)
    ax.bar(xs - 0.5 * width, verify_vals, width,
           label="Verification/round", color=STAGE_COLORS["verify"],
           edgecolor="white", linewidth=BAR_EDGE_LINEWIDTH)
    payment_bars = ax.bar(xs + 0.5 * width, protocol_vals, width,
           label="Payment/round", color=STAGE_COLORS["protocol"],
           edgecolor="white", linewidth=BAR_EDGE_LINEWIDTH)
    for rect, v in zip(payment_bars, protocol_vals):
        ax.annotate(f"{v:.{PAYMENT_LABEL_DECIMALS}f}",
                    (rect.get_x() + rect.get_width() / 2, v),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", rotation=90,
                    fontsize=PAYMENT_LABEL_FONT_SIZE,
                    color=STAGE_COLORS["protocol"])

    # Total = stacked draft+verify+protocol, no separate legend entries for
    # the stack segments (they're already labeled by the standalone bars).
    total_x = xs + 1.5 * width
    ax.bar(total_x, draft_vals, width, color=STAGE_COLORS["draft"],
           edgecolor="white", linewidth=BAR_EDGE_LINEWIDTH)
    ax.bar(total_x, verify_vals, width, bottom=draft_vals,
           color=STAGE_COLORS["verify"], edgecolor="white", linewidth=BAR_EDGE_LINEWIDTH)
    ax.bar(total_x, protocol_vals, width,
           bottom=np.array(draft_vals) + np.array(verify_vals),
           color=STAGE_COLORS["protocol"], edgecolor="white", linewidth=BAR_EDGE_LINEWIDTH)

    ax.bar(xs + 2.5 * width, per_token_vals, width,
           label="Per Accepted Token",
           color=STAGE_COLORS["per_token"], edgecolor="white", linewidth=BAR_EDGE_LINEWIDTH)

    ax.set_xticks(xs, [str(g) for g in gammas])
    ax.set_xlabel(r"Speculative Batch Size ($\gamma$)")
    ax.set_ylabel("Latency (ms)")
    ax.legend(loc=LEGEND_LOC, bbox_to_anchor=LEGEND_BBOX_TO_ANCHOR, ncol=1)

    fig.savefig(OUT_PNG, bbox_inches="tight", dpi=SAVE_DPI)
    plt.close(fig)
    print(f"Saved -> {OUT_PNG}")


if __name__ == "__main__":
    main()
