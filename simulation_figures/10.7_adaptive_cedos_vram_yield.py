"""
10.7_adaptive_cedos_vram_yield.py — edit-and-rerun figure generator for
the 10.7_adaptive_cedos_vram_yield figure (attacker-held VRAM vs. payment
timing margin: fixed 500ms vs. fixed 55ms vs. adaptive margin, log-x
reversed, with a secondary axis showing % of fleet VRAM captured).

This does NOT read from simulation/results/ or touch any live component.
It reads only 10.7_adaptive_cedos_vram_yield_data.json (sitting next to
this script) so you can freely tweak figure size / font size / colors
below and rerun in seconds, without needing the simulator.

Usage:
    python 10.7_adaptive_cedos_vram_yield.py
    (or: prototype/.venv/bin/python simulation_figures/10.7_adaptive_cedos_vram_yield.py)

Output:
    10.7_adaptive_cedos_vram_yield.png   (next to this script — same
    filename as the figure used everywhere else; never renamed, PNG
    only, no PDF)
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

VARIANT_STYLE = {
    "fixed_dt":    {"label": "$\\Delta t$ = 500 ms", "color": "#D55E00", "marker": "s", "linestyle": "--"},
    "fixed_dt_55": {"label": "$\\Delta t$ = 55 ms",  "color": "#888888", "marker": "^", "linestyle": ":"},
    "adaptive_dt": {"label": "$\\Delta t$ = Adaptive",       "color": "#0072B2", "marker": "o", "linestyle": "-"},
}
CI_BAND_ALPHA     = 0.15
LINE_WIDTH        = 2.2

GRID_ON           = True
GRID_ALPHA        = 0.4



LEGEND_LOC             = "lower left"
LEGEND_BBOX_TO_ANCHOR  = None


XTICK_ROTATION         = 90

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
    "axes.linewidth":     1.5,
})

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "10.7_adaptive_cedos_vram_yield_data.json")
OUT_PNG = os.path.join(HERE, "10.7_adaptive_cedos_vram_yield.png")


def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    fleet_block_s = data["n_hubs"] * data["hub_vram_blocks"] * data["sim_duration_sec"]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH_IN, FIGURE_HEIGHT_IN),
                            constrained_layout=True)

    pooled_mean = {}
    all_slacks = set()
    for name in ("fixed_dt", "fixed_dt_55", "adaptive_dt"):
        vd = data[name]
        style = VARIANT_STYLE[name]
        xs = vd["adversary_slack_ms"]
        ys = vd["evicted_vram_block_s"]
        pooled_mean[name] = sum(ys) / len(ys)
        all_slacks.update(xs)
        ax.plot(xs, ys, marker=style["marker"], color=style["color"],
                 linestyle=style["linestyle"], label=style["label"])
        lo = vd.get("evicted_vram_block_s_ci_lo")
        hi = vd.get("evicted_vram_block_s_ci_hi")
        if lo and hi:
            ax.fill_between(xs, lo, hi, color=style["color"],
                             alpha=CI_BAND_ALPHA, linewidth=0)

    ax.set_xscale("log")
    ax.invert_xaxis()
    all_slacks = sorted(all_slacks, reverse=True)
    ax.set_xticks(all_slacks)
    ax.set_xticklabels([f"{v:g}" for v in all_slacks], rotation=XTICK_ROTATION, ha="center")
    ax.xaxis.set_minor_locator(plt.NullLocator())
    ax.set_xlabel("Payment Margin (ms)")
    ax.set_ylabel("Attacker VRAM")


    if fleet_block_s > 0:
        ax2 = ax.secondary_yaxis(
            "right", functions=(lambda y: y / fleet_block_s * 100,
                                 lambda p: p / 100 * fleet_block_s))
        ax2.set_ylabel("% of VRAM")


    if all(k in pooled_mean for k in ("adaptive_dt", "fixed_dt_55", "fixed_dt")):
        pct_vs_floor = pooled_mean["adaptive_dt"] / pooled_mean["fixed_dt_55"] * 100
        pct_vs_naive = pooled_mean["adaptive_dt"] / pooled_mean["fixed_dt"] * 100
        print(f"Adaptive is ~{pct_vs_floor:.0f}% of fixed-55ms floor, "
              f"~{pct_vs_naive:.0f}% of fixed-500ms naive baseline.")

    ax.legend(loc=LEGEND_LOC, bbox_to_anchor=LEGEND_BBOX_TO_ANCHOR, ncol=1)




    fig.savefig(OUT_PNG, bbox_inches="tight", dpi=SAVE_DPI)
    plt.close(fig)
    print(f"Saved -> {OUT_PNG}")


if __name__ == "__main__":
    main()
