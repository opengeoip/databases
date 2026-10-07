import csv
import sys
from datetime import date

WIDTH, HEIGHT = 800, 360
LEFT, RIGHT, TOP, BOTTOM = 56, 150, 24, 40
SERIES = [
    ("ipv4", "OpenGeoIP IPv4", "#4fd1c5", ""),
    ("ipv6", "OpenGeoIP IPv6", "#f6ad55", ""),
    ("dbip_ipv4", "DB-IP Lite IPv4", "#4fd1c5", "6 5"),
    ("dbip_ipv6", "DB-IP Lite IPv6", "#f6ad55", "6 5"),
]


def main(source, target):
    with open(source, newline="") as f:
        rows = [row for row in csv.DictReader(f)]
    days = [date.fromisoformat(row["date"]).toordinal() for row in rows]
    values = [float(row[key]) for row in rows for key, *_ in SERIES if row[key]]
    low = max(0, int(min(values)) - 1)
    high = min(100, int(max(values)) + 2)
    first, last = min(days), max(days)
    span = max(last - first, 1)

    def x(day):
        if first == last:
            return LEFT + (WIDTH - LEFT - RIGHT) / 2
        return LEFT + (day - first) / span * (WIDTH - LEFT - RIGHT)

    def y(value):
        return TOP + (high - value) / (high - low) * (HEIGHT - TOP - BOTTOM)

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" width="{WIDTH}" height="{HEIGHT}" font-family="sans-serif" font-size="12" fill="#8b949e">'
    ]
    step = max(1, (high - low) // 6)
    for value in range(low, high + 1, step):
        out.append(f'<line x1="{LEFT}" x2="{WIDTH - RIGHT}" y1="{y(value):.1f}" y2="{y(value):.1f}" stroke="#8b949e" stroke-opacity="0.25"/>')
        out.append(f'<text x="{LEFT - 8}" y="{y(value) + 4:.1f}" text-anchor="end">{value} %</text>')
    for row, day in [(rows[0], days[0]), (rows[-1], days[-1])]:
        out.append(f'<text x="{x(day):.1f}" y="{HEIGHT - BOTTOM + 20}" text-anchor="middle">{row["date"]}</text>')
    for index, (key, label, color, dash) in enumerate(SERIES):
        points = [(x(day), y(float(row[key]))) for row, day in zip(rows, days) if row[key]]
        if not points:
            continue
        dasharray = f' stroke-dasharray="{dash}"' if dash else ""
        path = " ".join(f"{px:.1f},{py:.1f}" for px, py in points)
        out.append(f'<polyline points="{path}" fill="none" stroke="{color}" stroke-width="2.5"{dasharray}/>')
        for px, py in points[-1:]:
            out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.5" fill="{color}"/>')
        legend = TOP + 10 + index * 22
        out.append(f'<line x1="{WIDTH - RIGHT + 16}" x2="{WIDTH - RIGHT + 40}" y1="{legend}" y2="{legend}" stroke="{color}" stroke-width="2.5"{dasharray}/>')
        out.append(f'<text x="{WIDTH - RIGHT + 46}" y="{legend + 4}">{label}</text>')
    out.append("</svg>")
    with open(target, "w") as f:
        f.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
