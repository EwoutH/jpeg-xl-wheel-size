"""Render the preliminary comment's baseline-relative size measurements."""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, PercentFormatter

# Snapshot used in PR7848-COMMENT.md. Percentages are rounded to one decimal;
# source reports: runs 38309369474 and 38309406995. These are download bytes,
# not installed size or decoding speed. Intel macOS is not in this snapshot.
data = [
    ("Linux x86_64", 6.971, [29.8, 10.1, 6.6, 5.5]),
    ("Linux aarch64", 6.409, [24.8, 8.2, 5.7, 4.8]),
    ("macOS arm64", 4.565, [29.1, 9.4, 7.0, 5.9]),
    ("Windows AMD64", 6.793, [8.5, 8.5, 6.9, 6.9]),
]
labels = ["PR: full libjxl", "Decoder only", "+ MinSizeRel", "+ LTO"]
colors = ["#CD6A32", "#537DA0", "#39958F", "#17665F"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "svg.fonttype": "none", "axes.titleweight": "bold"})
fig, axes = plt.subplots(2, 2, figsize=(12, 7.8))
fig.subplots_adjust(left=.15, right=.97, top=.76, bottom=.18, wspace=.57, hspace=.85)
fig.text(.035, .945, "JPEG XL adds ~25–30% on Unix; optimization brings it to ~5–6%",
         fontsize=17, weight="bold", color="#172B3A")
fig.text(.035, .895, "Added wheel download size over the same-commit no-jxl baseline",
         fontsize=13, color="#344958")
fig.text(.035, .855, "CPython 3.13 · libjxl 0.11.2 · Shared scale across all four platforms",
         fontsize=11, color="#526675")
for ax, (platform, baseline, growth) in zip(axes.flat, data):
    ax.barh(range(4), growth, color=colors, height=.64, zorder=3)
    ax.set_yticks(range(4), labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 33)
    ax.xaxis.set_major_locator(MultipleLocator(10))
    ax.xaxis.set_major_formatter(PercentFormatter(xmax=100, decimals=0))
    ax.grid(axis="x", color="#DFE5E9", linewidth=.8, zorder=0)
    ax.set_axisbelow(True)
    ax.tick_params(axis="both", length=0, pad=7, labelsize=10)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.axvline(0, color="#B2BFC7", linewidth=1)
    ax.set_title(platform, loc="left", pad=28, fontsize=13)
    ax.text(0, 1.075, f"no-jxl wheel: {baseline:.3f} MiB", transform=ax.transAxes,
            fontsize=10, color="#526675")
    for i, value in enumerate(growth):
        ax.text(value + .65, i, f"+{value:.1f}%", va="center", fontsize=10,
                weight="bold", color="#172B3A")
fig.text(.035, .09, "0% = no added download cost. Each step includes the preceding changes; SIMD stays enabled.",
         fontsize=10, color="#344958")
fig.text(.035, .055, "Size only: Windows size optimization slows some decoding samples. See the comment for tests and tradeoffs.",
         fontsize=10, color="#344958")
fig.text(.035, .02, "Source: EwoutH/jpeg-xl-wheel-size · Pillow d00ba3a · Preliminary results; Intel macOS pending",
         fontsize=9, color="#627582")
out = Path(__file__).resolve().parents[1] / "figures"
out.mkdir(exist_ok=True)
for extension in ("png", "svg"):
    fig.savefig(out / f"jpeg-xl-overhead.{extension}", dpi=200, facecolor="white")
plt.close(fig)
