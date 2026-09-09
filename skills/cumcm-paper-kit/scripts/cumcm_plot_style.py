#!/usr/bin/env python3
"""Reusable Matplotlib style helpers for CUMCM paper figures."""

from __future__ import annotations

import argparse
import math
from pathlib import Path
from typing import Iterable


PALETTE = ("#1F4E79", "#C55A11", "#548235", "#7030A0", "#7F6000", "#5B9BD5")
LINESTYLES = ("-", "--", "-.", ":")
MARKERS = ("o", "s", "^", "D", "v", "P")


def cm_to_inch(value: float) -> float:
    return value / 2.54


def apply_cumcm_style(font_path: str | Path | None = None) -> str:
    import matplotlib as mpl
    from matplotlib import font_manager

    selected = "Source Han Serif CN"
    if font_path:
        path = Path(font_path).expanduser().resolve()
        font_manager.fontManager.addfont(str(path))
        selected = font_manager.FontProperties(fname=str(path)).get_name()

    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": [
                selected,
                "Source Han Serif SC",
                "Songti SC",
                "SimSun",
                "Times New Roman",
                "DejaVu Serif",
            ],
            "mathtext.fontset": "stix",
            "axes.unicode_minus": False,
            "font.size": 9.5,
            "axes.labelsize": 9.5,
            "legend.fontsize": 8.5,
            "xtick.labelsize": 8.5,
            "ytick.labelsize": 8.5,
            "axes.linewidth": 0.8,
            "lines.linewidth": 1.5,
            "lines.markersize": 4.5,
            "grid.color": "#D9D9D9",
            "grid.linewidth": 0.6,
            "grid.alpha": 0.7,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.facecolor": "white",
        }
    )
    return selected


def new_figure(width_cm: float = 14.5, aspect: float = 0.62):
    import matplotlib.pyplot as plt

    width = cm_to_inch(width_cm)
    return plt.subplots(figsize=(width, width * aspect), constrained_layout=True)


def style_axes(ax, *, grid_axis: str | None = "y") -> None:
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    if grid_axis:
        ax.grid(True, axis=grid_axis)
        ax.set_axisbelow(True)


def save_figure(fig, outputs: Iterable[str | Path]) -> None:
    for output in outputs:
        path = Path(output).expanduser().resolve()
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path)


def create_demo(output: Path, font_path: Path | None) -> None:
    try:
        apply_cumcm_style(font_path)
        fig, ax = new_figure()
    except ImportError:
        if output.suffix.lower() != ".svg":
            raise RuntimeError("Matplotlib is unavailable; request an .svg demo or install matplotlib")
        create_svg_demo(output)
        return
    xs = list(range(1, 13))
    observed = [0.45 + 0.035 * x + 0.08 * math.sin(x / 1.7) for x in xs]
    predicted = [0.47 + 0.033 * x + 0.055 * math.sin((x + 0.4) / 1.8) for x in xs]
    ax.plot(xs, observed, color=PALETTE[0], marker=MARKERS[0], label="观测值")
    ax.plot(xs, predicted, color=PALETTE[1], linestyle=LINESTYLES[1], marker=MARKERS[1], label="预测值")
    ax.set_xlabel("样本序号")
    ax.set_ylabel("归一化指标")
    ax.set_xlim(1, 12)
    style_axes(ax)
    ax.legend(frameon=False, ncol=2)
    save_figure(fig, [output])


def create_svg_demo(output: Path) -> None:
    """Write a dependency-free SVG preview when Matplotlib is unavailable."""
    width, height = 760, 430
    left, right, top, bottom = 78, 28, 28, 62
    plot_w, plot_h = width - left - right, height - top - bottom
    xs = list(range(1, 13))
    series = (
        ("观测值", [0.45 + 0.035 * x + 0.08 * math.sin(x / 1.7) for x in xs], PALETTE[0]),
        ("预测值", [0.47 + 0.033 * x + 0.055 * math.sin((x + 0.4) / 1.8) for x in xs], PALETTE[1]),
    )
    ymin = min(min(values) for _, values, _ in series) - 0.04
    ymax = max(max(values) for _, values, _ in series) + 0.04

    def point(index: int, value: float) -> tuple[float, float]:
        x = left + index * plot_w / (len(xs) - 1)
        y = top + (ymax - value) * plot_h / (ymax - ymin)
        return x, y

    family = "Source Han Serif CN, Source Han Serif SC, Songti SC, SimSun, serif"
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        f'<g font-family="{family}" font-size="15" fill="#222">',
    ]
    for tick in range(6):
        value = ymin + tick * (ymax - ymin) / 5
        y = point(0, value)[1]
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{width-right}" y2="{y:.1f}" stroke="#D9D9D9" stroke-width="1"/>')
        parts.append(f'<text x="{left-12}" y="{y+5:.1f}" text-anchor="end">{value:.2f}</text>')
    parts.extend(
        [
            f'<line x1="{left}" y1="{top}" x2="{left}" y2="{height-bottom}" stroke="#222"/>',
            f'<line x1="{left}" y1="{height-bottom}" x2="{width-right}" y2="{height-bottom}" stroke="#222"/>',
        ]
    )
    for index, value in enumerate(xs):
        x, _ = point(index, ymin)
        parts.append(f'<text x="{x:.1f}" y="{height-bottom+26}" text-anchor="middle">{value}</text>')
    for label, values, color in series:
        coords = " ".join(f"{point(i, value)[0]:.1f},{point(i, value)[1]:.1f}" for i, value in enumerate(values))
        dash = ' stroke-dasharray="8 5"' if label == "预测值" else ""
        parts.append(f'<polyline points="{coords}" fill="none" stroke="{color}" stroke-width="2.4"{dash}/>')
        for i, value in enumerate(values):
            x, y = point(i, value)
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.3" fill="white" stroke="{color}" stroke-width="2"/>')
    parts.extend(
        [
            f'<text x="{left+plot_w/2:.1f}" y="{height-10}" text-anchor="middle">样本序号</text>',
            f'<text x="20" y="{top+plot_h/2:.1f}" text-anchor="middle" transform="rotate(-90 20 {top+plot_h/2:.1f})">归一化指标</text>',
            f'<line x1="{width-215}" y1="24" x2="{width-180}" y2="24" stroke="{PALETTE[0]}" stroke-width="2.4"/>',
            f'<text x="{width-170}" y="29">观测值</text>',
            f'<line x1="{width-105}" y1="24" x2="{width-70}" y2="24" stroke="{PALETTE[1]}" stroke-width="2.4" stroke-dasharray="8 5"/>',
            f'<text x="{width-60}" y="29">预测值</text>',
            "</g></svg>",
        ]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(parts) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="CUMCM figure-style helper with an SVG fallback")
    parser.add_argument("--demo", type=Path, help="Write a synthetic style preview")
    parser.add_argument("--font", type=Path, help="Path to a Chinese serif font")
    args = parser.parse_args()
    if not args.demo:
        parser.print_help()
        return 0
    create_demo(args.demo, args.font)
    print(args.demo.expanduser().resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
