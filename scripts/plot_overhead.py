"""Render final baseline-relative measurements from the archived CI evidence."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, PercentFormatter

repo = Path(__file__).resolve().parents[1]
summary = json.loads((repo / "evidence/summary.json").read_text())
platforms = {"linux-x86_64": "Linux x86_64", "linux-aarch64": "Linux aarch64",
             "macos-x86_64": "macOS x86_64", "macos-arm64": "macOS arm64", "windows-amd64": "Windows AMD64"}
data = [(label, summary["platforms"][key]["no-jxl"]["bytes"] / 1048576,
         [summary["platforms"][key][v]["growth_percent"] for v in ("pr", "decoder", "minsize", "lto")])
        for key, label in platforms.items()]
labels = ["PR: full libjxl", "Decoder only", "+ MinSizeRel", "+ LTO"]
colors = ["#CD6A32", "#537DA0", "#39958F", "#17665F"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "svg.fonttype": "none", "axes.titleweight": "bold"})
fig, axes = plt.subplots(3, 2, figsize=(12, 10.5))
fig.subplots_adjust(left=.15, right=.97, top=.80, bottom=.14, wspace=.57, hspace=.85)
fig.text(.035, .955, "From 25–41% extra to 5–8% on Linux and macOS",
         fontsize=17, weight="bold", color="#172B3A")
fig.text(.035, .915, "Added wheel download size over the same-commit no-jxl baseline",
         fontsize=13, color="#344958")
fig.text(.035, .88, "30 wheels · CPython 3.13 · libjxl 0.11.2 · Shared scale across all five platforms",
         fontsize=11, color="#526675")
for ax, (platform, baseline, growth) in zip(axes.flat, data):
    ax.barh(range(4), growth, color=colors, height=.64, zorder=3)
    ax.set_yticks(range(4), labels)
    ax.invert_yaxis()
    ax.set_xlim(0, 46)
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
ax = axes.flat[-1]
ax.axis("off")
ax.text(-.18, .98, "Where the savings come from", transform=ax.transAxes,
        fontsize=13, weight="bold", color="#172B3A", va="top")
ax.text(-.18, .72, "Decoder-only removes 66–68% of the\nadded cost on Linux and macOS.\n\nAdding MinSizeRel + LTO removes 80–82%.\nWindows improves less: about 18%.",
        transform=ax.transAxes, fontsize=11, color="#344958", va="top", linespacing=1.5)
fig.text(.035, .085, "0% = no added download cost. Each step includes the preceding changes; SIMD stays enabled.",
         fontsize=10, color="#344958")
fig.text(.035, .052, "Tradeoffs: size flags cause tiny sample pixel changes on Linux x86_64 and slower decoding on Windows.",
         fontsize=10, color="#344958")
fig.text(.035, .02, "Source: EwoutH/jpeg-xl-wheel-size/evidence · Pillow d00ba3a · All builds and selected test jobs passed",
         fontsize=9, color="#627582")
out = Path(__file__).resolve().parents[1] / "figures"
out.mkdir(exist_ok=True)
for extension in ("png", "svg"):
    fig.savefig(out / f"jpeg-xl-overhead.{extension}", dpi=200, facecolor="white")
svg = out / "jpeg-xl-overhead.svg"
svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
plt.close(fig)
