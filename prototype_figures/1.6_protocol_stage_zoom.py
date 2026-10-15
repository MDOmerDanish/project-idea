"""
1.6_protocol_stage_zoom.py — edit-and-rerun figure generator for the
1.6_protocol_stage_zoom figure (log-scale grouped bars of the six
payment-channel protocol steps, one group per gamma).

This does NOT read from prototype/results/ or touch any live component.
It reads only 1.6_protocol_stage_zoom_data.json (sitting next to this
script) so you can freely tweak figure size / font size / colors below
and rerun in seconds, without needing the prototype's venv or GPU.

Usage:
    python 1.6_protocol_stage_zoom.py
    (or: prototype/.venv/bin/python prototype_figures/1.6_protocol_stage_zoom.py)

Output:
    1.6_protocol_stage_zoom.png   (next to this script — same filename as
    the figure used everywhere else; never renamed, PNG only, no PDF)
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker

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
LEGEND_FONT_SIZE  = 16       # legend entries (6 entries, kept a bit smaller
                              # than the axis text so a 2-column legend fits)

BOLD_EVERYTHING   = True     # axis labels, tick labels, legend text

BAR_WIDTH         = 0.8
STEP_COLORS = ["#1f4e9c", "#3d85d8", "#c0392b", "#e57373", "#7f7f7f", "#b5b5b5"]

# Legend text for each protocol step, keyed by the data file's internal
# field name (stage_keys in the JSON) -- edit the label strings here to
# change what the legend shows, without touching the data file at all.
STAGE_LABELS = {
    "t_commit_s":   "Commit Signing",
    "t_wrap_s":     "Key Wrapping",
    "t_validate_s": "Validation",
    "t_pay_build_s":"Payment Build",
    "t_settle_s":   "Settlement",
    "t_decrypt_s":  "Key Verify/Decrypt",
}

GRID_ON           = True
GRID_ALPHA        = 0.30

LEGEND_LOC             = "upper center"
LEGEND_BBOX_TO_ANCHOR  = (0.5, 1.00)   # pushed above the axes; increase the
                                        # 2nd number to push it further up
LEGEND_NCOL            = 2

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
    "axes.linewidth":     1.5,
})

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(HERE, "1.6_protocol_stage_zoom_data.json")
OUT_PNG = os.path.join(HERE, "1.6_protocol_stage_zoom.png")


def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    gammas = data["gammas"]
    stage_keys = data["stage_keys"]
    stage_order = [(key, STAGE_LABELS[key]) for key in stage_keys]
    stage_means = {int(g): v for g, v in data["stage_means_ms"].items()}

    n_steps = len(stage_order)
    pitch = n_steps + 1.5

    fig, ax = plt.subplots(figsize=(FIGURE_WIDTH_IN, FIGURE_HEIGHT_IN),
                            constrained_layout=True)

    top = 0.0
    for si, ((key, lbl), color) in enumerate(zip(stage_order, STEP_COLORS)):
        xs = [gi * pitch + si for gi in range(len(gammas))]
        means = [stage_means[g][key] for g in gammas]
        ax.bar(xs, means, BAR_WIDTH, color=color, label=lbl,
               edgecolor="white", linewidth=1.0)
        top = max(top, max(means))

    ax.set_xticks([gi * pitch + (n_steps - 1) / 2 for gi in range(len(gammas))],
                  [str(g) for g in gammas])
    ax.set_xlabel(r"Speculative Batch Size ($\gamma$)")
    ax.set_yscale("log")
    ax.yaxis.set_minor_formatter(matplotlib.ticker.NullFormatter())
    ax.set_ylabel("Latency (ms)")
    ax.set_ylim(top=top * 6)

    ax.legend(loc=LEGEND_LOC, bbox_to_anchor=LEGEND_BBOX_TO_ANCHOR,
              ncol=LEGEND_NCOL, framealpha=0.9)

    fig.savefig(OUT_PNG, bbox_inches="tight", dpi=SAVE_DPI)
    plt.close(fig)
    print(f"Saved -> {OUT_PNG}")


if __name__ == "__main__":
    main()
