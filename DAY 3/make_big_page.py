"""Create the large HTML page used in the context-overflow experiment."""
rows = "\n".join(
    f"<tr><td>Student {number:04d}</td><td>Roll BA{number:04d}</td>"
    f"<td>Attendance {60 + number % 40}%</td>"
    "<td>Remarks: regular attendance recorded</td></tr>"
    for number in range(1, 3001))
html = f"<html><body><h1>Attendance Register</h1><table>{rows}</table></body></html>"
with open("big.html", "w", encoding="utf-8") as page:
    page.write(html)
print(f"big.html created: {len(html):,} characters")