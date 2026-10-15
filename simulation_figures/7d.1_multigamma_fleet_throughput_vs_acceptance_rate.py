"""
7d.1_multigamma_fleet_throughput_vs_acceptance_rate.py — edit-and-rerun
figure generator for the 7d.1_multigamma_fleet_throughput_vs_acceptance_rate
figure (throughput vs. synthetically swept acceptance rate, one line per
gamma, 50-hub fleet; solid up to each gamma's realized acceptance ceiling,
dashed beyond it).

This does NOT read from simulation/results/ or prototype/results/, or
touch any live component. It reads only
7d.1_multigamma_fleet_throughput_vs_acceptance_rate_data.json (sitting
next to this script) so you can freely tweak figure size / font size /
colors below and rerun in seconds, without needing the simulator or GPU.

Usage:
    python 7d.1_multigamma_fleet_throughput_vs_acceptance_rate.py
    (or: prototype/.venv/bin/python simulation_figures/7d.1_multigamma_fleet_throughput_vs_acceptance_rate.py)

Output:
    7d.1_multigamma_fleet_throughput_vs_acceptance_rate.png   (next to
    this script — same filename as the figure used everywhere else;
    never renamed, PNG only, no PDF)
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
LEGEND_FONT_SIZE  = 16       # legend entries (5 gamma lines)

BOLD_EVERYTHING   = True     # axis labels, tick labels, legend text

GAMMA_COLORS = {
    "1": "#0072B2",
    "3": "#D55E00",
    "5": "#009E73",
    "7": "#CC79A7",
    "9": "#E69F00",
}
GAMMA_MARKERS = {"1": "o", "3": "s", "5": "^", "7": "D", "9": "v"}

BEYOND_ALPHA      = 0.45   # opacity of the extrapolated (dashed) segment
CEILING_LINE_ALPHA = 0.5

GRID_ON           = True
GRID_ALPHA        = 0.4

LABEL_STYLE            = "inline"   # "legend" (boxed legend, original
                                     # style) or "inline" (gamma label
                                     # placed directly at the end of each
                                     # curve, no legend box at all — saves
                                     # the horizontal space a 5-entry
                                     # legend needs)
LEGEND_LOC             = "upper left"
LEGEND_BBOX_TO_ANCHOR  = (0.5, -0.30)
LEGEND_NCOL            = 3
INLINE_LABEL_FONT_SIZE = 16
INLINE_LABEL_X_OFFSET  = 0.015   # fraction of x-range to nudge the label
                                  # right of the curve's last point

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
DATA_PATH = os.path.join(HERE, "7d.1_multigamma_fleet_throughput_vs_acceptance_rate_data.json")
OUT_PNG = os.path.join(HERE, "7d.1_multigamma_fleet_throughput_vs_acceptance_rate.png")


def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    series = data["series"]
    ceilings = data["realized_acceptance_ceilings"]

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH_IN, FIGURE_HEIGHT_IN),
                            constrained_layout=True)

    all_xs = [p["acceptance_rate"] for pts in series.values() for p in pts]
    x_range = max(all_xs) - min(all_xs)
    inline_targets = []  # (x, y, color, gamma) for the last point of each curve

    for gamma in sorted(series.keys(), key=int):
        points = sorted(series[gamma], key=lambda r: r["acceptance_rate"])
        xs = [p["acceptance_rate"] for p in points]
        ys = [p["throughput_tps"] for p in points]
        color = GAMMA_COLORS.get(gamma, "#444444")
        marker = GAMMA_MARKERS.get(gamma, "o")
        ceiling = ceilings[gamma]

        achievable = [(x, y) for x, y in zip(xs, ys) if x <= ceiling]
        beyond = [(x, y) for x, y in zip(xs, ys) if x > ceiling]
        if achievable and beyond:
            x0, y0 = achievable[-1]
            x1, y1 = beyond[0]
            t = (ceiling - x0) / (x1 - x0)
            y_cross = y0 * (y1 / y0) ** t
            achievable = achievable + [(ceiling, y_cross)]
            beyond = [(ceiling, y_cross)] + beyond

        show_legend_label = (LABEL_STYLE == "legend")
        if achievable:
            ax.plot([p[0] for p in achievable], [p[1] for p in achievable],
                     marker=marker, color=color, linestyle="-",
                     label=f"$\\gamma$={gamma}" if show_legend_label else None)
        if beyond:
            ax.plot([p[0] for p in beyond], [p[1] for p in beyond],
                     marker=marker, color=color, linestyle="--",
                     alpha=BEYOND_ALPHA, markerfacecolor="none",
                     label=(f"$\\gamma$={gamma}" if (show_legend_label and not achievable) else None))
        ax.axvline(ceiling, color=color, alpha=CEILING_LINE_ALPHA,
                   linewidth=1.2, linestyle=":", zorder=0)

        last_x, last_y = (beyond or achievable)[-1]
        inline_targets.append((last_x, last_y, color, gamma))

    ax.set_xlabel("Token Acceptance Rate")
    ax.set_ylabel("Throughput (tokens/s)")
    ax.set_yscale("log")
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0%}"))

    k_formatter = plt.FuncFormatter(lambda v, _: f"{v/1000:g}k" if v >= 1000 else f"{v:g}")
    # Log scale's default major locator only places ticks at powers of 10
    # (..., 100, 1000, 10000, ...); the in-between labels (2k, 3k, ...) seen
    # on this data's actual range come from minor ticks, so both major AND
    # minor formatters need to be set. matplotlib auto-extends the y-limits
    # slightly below the lowest data point (~859), which pulled in the
    # 100s decade's own minor ticks (800, 900) alongside the 1000s
    # decade's (2k, 3k, ...). Hide only the 100s-decade minor ticks
    # (values below 1000) without touching the axis limits themselves, so
    # the gamma=1 curve's lowest point (~859) still stays fully visible.
    ax.yaxis.set_major_formatter(k_formatter)
    ax.yaxis.set_minor_formatter(plt.FuncFormatter(
        lambda v, pos: (f"{v/1000:g}k" if v >= 1000 else "")))

    if LABEL_STYLE == "inline":
        x_pad = x_range * INLINE_LABEL_X_OFFSET
        for last_x, last_y, color, gamma in inline_targets:
            ax.text(last_x + x_pad, last_y, f"$\\gamma$={gamma}",
                     color=color, va="center", ha="left",
                     fontsize=INLINE_LABEL_FONT_SIZE, fontweight="bold")
        # Give the inline labels room on the right without changing the
        # actual data range shown.
        xlo, xhi = ax.get_xlim()
        ax.set_xlim(xlo, xhi + x_range * 0.22)
    else:
        ax.legend(loc=LEGEND_LOC, bbox_to_anchor=LEGEND_BBOX_TO_ANCHOR,
                  ncol=LEGEND_NCOL, frameon=True)

    fig.savefig(OUT_PNG, bbox_inches="tight", dpi=SAVE_DPI)
    plt.close(fig)
    print(f"Saved -> {OUT_PNG}")


if __name__ == "__main__":
    main()
