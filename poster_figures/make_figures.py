"""Regenerates the six poster plots at 5.5 x 3.09 in; axis text 28 pt, legends/annotations smaller.

Values are read off the original plots (approximate to plot resolution).
Run: PYTHONPATH=<matplotlib dir> python3 make_figures.py
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.colors import LogNorm, LinearSegmentedColormap
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, NullFormatter

FS = 28
W, H = 5.5, 3.09
LEG = 12  # legend / in-plot annotation size (axes text stays FS)
OUT = os.path.dirname(os.path.abspath(__file__))

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Liberation Serif", "Nimbus Roman", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": FS,
    "font.weight": "bold",
    "axes.labelweight": "bold",
    "axes.labelsize": FS,
    "xtick.labelsize": FS,
    "ytick.labelsize": FS,
    "legend.fontsize": FS,
    "axes.linewidth": 1.8,
    "xtick.major.width": 2,
    "ytick.major.width": 2,
    "xtick.major.size": 5,
    "ytick.major.size": 5,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

GAMMAS = [1, 3, 5, 7, 9]
G = "\u03b3"


def new_fig(l=1.5, b=0.95, w=3.9, h=2.02):
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([l / W, b / H, w / W, h / H])
    return fig, ax


def in_legend(ax, handles=None, labels=None, ncol=2, loc="upper left"):
    kw = dict(fontsize=LEG, ncol=ncol, loc=loc, frameon=True, framealpha=0.9,
              edgecolor="none", handlelength=1.2, handletextpad=0.4,
              labelspacing=0.2, columnspacing=0.8, borderpad=0.25,
              borderaxespad=0.1)
    if handles is None:
        ax.legend(**kw)
    else:
        ax.legend(handles, labels, **kw)


def grid(ax):
    ax.grid(True, which="major", ls="--", lw=0.7, alpha=0.35)
    ax.set_axisbelow(True)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + ".png"), dpi=300)
    fig.savefig(os.path.join(OUT, name + ".pdf"))
    plt.close(fig)


def fig1():
    names = ["Commit Signing", "Key Wrapping", "Validation",
             "Payment Build", "Settlement", "Key Verify/Decrypt"]
    colors = ["#1f4e9c", "#3d85d8", "#c0392b", "#e57373", "#808080", "#b5b5b5"]
    data = np.array([
        [0.110, 0.169, 0.153, 0.0517, 0.152, 0.0192],
        [0.103, 0.173, 0.174, 0.0582, 0.172, 0.0203],
        [0.101, 0.160, 0.165, 0.0531, 0.168, 0.0194],
        [0.101, 0.169, 0.181, 0.0577, 0.182, 0.0225],
        [0.094, 0.238, 0.303, 0.0970, 0.318, 0.0330],
    ])
    fig, ax = new_fig(l=1.6, w=3.7)
    w, pitch = 0.094, 0.134
    x = np.arange(5)
    for j, (n, c) in enumerate(zip(names, colors)):
        ax.bar(x + (j - 2.5) * pitch, data[:, j], w, color=c, label=n)
    ax.set_yscale("log")
    ax.set_ylim(0.017, 6)
    ax.set_xlim(-0.55, 4.55)
    ax.set_xticks(x, [str(g) for g in GAMMAS])
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.set_yticks([0.1, 1])
    ax.set_ylabel("Time (ms)")
    ax.set_xlabel(f"Batch Size ({G})")
    grid(ax)
    in_legend(ax, ncol=2)
    save(fig, "fig1_latency_by_component")


def fig2():
    draft = [13.7, 34.2, 52.1, 71.5, 87.7]
    verif = [104.0, 113.7, 119.3, 143.9, 145.5]
    pay = [0.68, 0.67, 0.73, 0.74, 0.65]
    tok = [70.8, 57.3, 58.7, 63.4, 66.0]
    c_d, c_v, c_p, c_t = "#4c72b0", "#c96630", "#129688", "#b04e70"
    fig, ax = new_fig(l=1.85, w=3.45)
    x = np.arange(5)
    w = 0.147
    kw = dict(width=w, edgecolor="white", linewidth=1.0)
    ax.bar(x - 2 * w, draft, color=c_d, **kw)
    ax.bar(x - w, verif, color=c_v, **kw)
    ax.bar(x, pay, color=c_p, **kw)
    ax.bar(x + w, draft, color=c_d, **kw)
    ax.bar(x + w, verif, bottom=draft, color=c_v, **kw)
    ax.bar(x + w, pay, bottom=np.add(draft, verif), color=c_p, **kw)
    ax.bar(x + 2 * w, tok, color=c_t, **kw)
    for xi, p in zip(x, pay):
        ax.text(xi, 4, f"{p:.2f}", rotation=90, color=c_p, ha="center",
                va="bottom", fontsize=LEG - 1, fontweight="bold",
                path_effects=[pe.withStroke(linewidth=2.5, foreground="white")],
                zorder=5)
    ax.set_xticks(x, [str(g) for g in GAMMAS])
    ax.set_xlim(-0.55, 4.55)
    ax.set_ylim(0, 340)
    ax.set_yticks([0, 100, 200, 300])
    ax.set_ylabel("Time (ms)")
    ax.set_xlabel(f"Batch Size ({G})")
    grid(ax)
    handles = [Patch(color=c_d), Patch(color=c_v), Patch(color=c_p), Patch(color=c_t)]
    in_legend(ax, handles, ["Drafting/round", "Verification/round",
                            "Payment/round", "Per Accepted Token"], ncol=2)
    save(fig, "fig2_round_latency")


def fig3():
    cols = {1: "#0072B2", 3: "#D55E00", 5: "#009E73", 7: "#CC79A7", 9: "#E69F00"}
    mk = {1: "o", 3: "s", 5: "^", 7: "D", 9: "v"}
    solid = {
        1: [(19.3, 860), (39.8, 1010), (60.1, 1150), (68.3, 1210)],
        3: [(19.3, 1140), (39.6, 1570), (54.0, 1870)],
        5: [(19.3, 1420), (37.2, 2040)],
        7: [(19.2, 1700), (25.2, 1980), (29.0, 2200), (33.0, 2360)],
        9: [(18.7, 1910), (19.9, 2000), (23.9, 2240), (26.7, 2420)],
    }
    openp = {
        1: [(80.5, 1300)],
        3: [(60.0, 2010), (80.3, 2460)],
        5: [(39.5, 2130), (59.8, 2870), (80.0, 3600)],
        7: [(39.5, 2700), (59.8, 3730), (78.5, 4690)],
        9: [(38.8, 3240), (59.8, 4590), (75.8, 5620)],
    }
    fig, ax = new_fig(w=3.9)
    for g in GAMMAS:
        c = cols[g]
        s, o = np.array(solid[g]), np.array(openp[g])
        ax.axvline(s[-1, 0], color=c, ls=":", lw=1.5, alpha=0.6)
        ax.plot(s[:, 0], s[:, 1], "-", color=c, lw=2.2, marker=mk[g], ms=7, zorder=3)
        link = np.vstack([s[-1], o])
        ax.plot(link[:, 0], link[:, 1], "--", color=c, lw=2.2, alpha=0.45)
        ax.plot(o[:, 0], o[:, 1], ls="none", marker=mk[g], ms=7, mfc="none",
                mec=c, mew=1.5, alpha=0.5)
        ax.text(o[-1, 0] + 2, o[-1, 1], f"{G}={g}", color=c, fontsize=LEG + 3,
                fontweight="bold", va="center", ha="left")
    ax.set_yscale("log")
    ax.set_ylim(780, 6300)
    ax.set_xlim(15, 100)
    ax.yaxis.set_major_locator(FixedLocator([1000, 2000, 4000]))
    ax.set_yticklabels(["1k", "2k", "4k"])
    ax.yaxis.set_minor_formatter(NullFormatter())
    ax.set_xticks([20, 40, 60, 80])
    ax.set_ylabel("Tokens/s")
    ax.set_xlabel("Acceptance Rate (%)")
    grid(ax)
    save(fig, "fig3_throughput_vs_acceptance")


def fig4():
    clients = [10, 50, 100, 200, 400, 800]
    hubs = [1, 2, 4, 8, 16, 32]
    v = np.array([
        [49, 49, 49, 49, 49, 49],
        [155, 239, 240, 239, 239, 240],
        [155, 306, 450, 451, 450, 450],
        [155, 307, 585, 911, 912, 911],
        [155, 306, 586, 1000, 2000, 2000],
        [155, 307, 587, 1000, 2000, 4000],
    ], dtype=float)
    cmap = LinearSegmentedColormap.from_list(
        "bl", ["#e3f2fd", "#90caf9", "#2196f3", "#1565c0", "#0d47a1"])
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([1.5 / W, 0.95 / H, 3.15 / W, 2.02 / H])
    norm = LogNorm(vmin=49, vmax=4000)
    im = ax.imshow(v, cmap=cmap, norm=norm, aspect="auto", origin="lower")
    for i in range(6):
        for j in range(6):
            val = v[i, j]
            t = f"{val / 1000:.0f}k" if val >= 1000 else f"{val:.0f}"
            ax.text(j, i, t, ha="center", va="center", fontsize=LEG - 1,
                    fontweight="bold")
    ax.set_xticks(range(6), [str(h) for h in hubs])
    ax.set_yticks(range(6), [str(c) for c in clients])
    ax.set_xlabel("Hubs")
    ax.set_ylabel("Clients")
    for sp in ax.spines.values():
        sp.set_visible(True)
    cax = fig.add_axes([4.8 / W, 0.95 / H, 0.17 / W, 1.62 / H])
    cb = fig.colorbar(im, cax=cax)
    cb.ax.set_title("tokens/s", fontsize=LEG, fontweight="bold", pad=5, loc="left")
    cb.outline.set_linewidth(1.2)
    cb.ax.tick_params(labelsize=LEG + 3)
    save(fig, "fig4_hubs_clients_heatmap")


T = np.arange(5, 200, 10)
NEAR_C, BAL_C, CEN_C = "#0072B2", "#009E73", "#D55E00"


def burst_fig(series, ylabel, name, ylim, yticks, yticklabels, l=1.7, w=3.55):
    fig, ax = new_fig(l=l, w=w)
    ax.axvspan(100, 150, color="#ffcccc", alpha=0.5, lw=0)
    for y, band, c, ls in series:
        y, band = np.array(y, float), np.array(band, float)
        ax.fill_between(T, y - band, y + band, color=c, alpha=0.15, lw=0)
        ax.plot(T, y, color=c, ls=ls, lw=2.5)
    ax.set_xlim(-4, 205)
    ax.set_ylim(*ylim)
    ax.set_xticks([0, 50, 100, 150, 200])
    ax.set_yticks(yticks, yticklabels)
    ax.set_xlabel("Simulation Time (s)")
    ax.set_ylabel(ylabel)
    grid(ax)
    handles = [Line2D([], [], color=NEAR_C, lw=2.5), Line2D([], [], color=BAL_C, lw=2.5),
               Line2D([], [], color=CEN_C, lw=2.5, ls="--"),
               Patch(facecolor="#ffcccc", edgecolor="#ffcccc", alpha=0.7)]
    in_legend(ax, handles, ["SPECIE(Nearest)", "SPECIE(Balanced)",
                            "Centralized", "10\u00d7 Arrival Burst"], ncol=2)
    save(fig, name)


def fig5():
    near = [0, 0, 1235, 1225, 1245, 1230, 1250, 1250, 1250, 1255,
            1880, 1930, 1945, 1940, 1940, 1385, 1230, 1265, 1245, 1240]
    bal = [0, 0, 1240, 1250, 1245, 1260, 1260, 1255, 1275, 1215,
           2330, 2810, 2850, 2860, 2900, 1750, 1250, 1245, 1250, 1255]
    cen = [0, 0, 505, 500, 497, 505, 500, 497, 505, 500,
           640, 690, 710, 710, 710, 545, 505, 510, 505, 500]
    burst = np.isin(T, np.arange(105, 150, 10))
    nb = np.where(burst, 60, 20)
    bb = np.where(burst, 35, 15)
    cb = np.full(len(T), 12)
    burst_fig([(cen, cb, CEN_C, "--"), (near, nb, NEAR_C, "-"), (bal, bb, BAL_C, "-")],
              "Tokens/s", "fig5_throughput_burst", (-100, 4800),
              [0, 2000, 4000], ["0", "2000", "4000"])


def fig6():
    cen = [0, 0, 61, 60, 60.5, 60.5, 61, 61, 60, 62,
           80, 75.5, 75.3, 74.3, 75.5, 42.5, 57.5, 57, 60, 61]
    near = [0] * 10 + [51, 48.5, 50.5, 51.3, 50, 0.5, 0, 0, 0, 0]
    burst = np.isin(T, np.arange(105, 150, 10))
    nb = np.where(burst, 4.5, 0.0)
    cb = np.where(T > 20, 3.0, 0.0)
    burst_fig([(cen, cb, CEN_C, "--"), (near, nb, NEAR_C, "-"),
               (np.zeros(20), np.zeros(20), BAL_C, "-")],
              "Rejection", "fig6_rejection_burst", (-5, 135),
              [0, 50, 100], ["0%", "50%", "100%"], l=1.85, w=3.4)


if __name__ == "__main__":
    for f in (fig1, fig2, fig3, fig4, fig5, fig6):
        f()
    print("done")
