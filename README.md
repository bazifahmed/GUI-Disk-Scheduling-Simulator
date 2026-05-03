# 🖥️ Disk Scheduling Simulator

A visual desktop application built with Python and Tkinter that simulates and compares classic disk scheduling algorithms in real time.

> **Project by Bazif & Sawaira** — Operating Systems Course

---

## Features

- **5 Algorithms** simulated simultaneously: FCFS, SCAN, C-SCAN, LOOK, C-LOOK
- **Animated trajectory graph** showing head movement across the disk
- **Auto-detects the best algorithm** (lowest seek time) and highlights it
- **Comparison table** sorted by seek time — best to worst at a glance
- **Popup detail view** for any non-best algorithm with step-by-step movement breakdown
- **Quick presets** (Classic, Dense, Scattered) for instant testing
- **Adjustable animation speed** (Slow / Normal / Fast)
- Dark-themed, clean UI with color-coded algorithm results

---

## Algorithms Implemented

| Algorithm | Description |
|-----------|-------------|
| **FCFS** | First Come First Serve — services requests in arrival order |
| **SCAN** | Elevator algorithm — sweeps to disk end then reverses |
| **C-SCAN** | Circular SCAN — sweeps one direction, jumps back to start |
| **LOOK** | Like SCAN but only goes as far as the last request |
| **C-LOOK** | Like C-SCAN but only goes as far as the last request |

---

## Requirements

- Python 3.x
- Tkinter (included in standard Python installations)

No external libraries required.

---

## How to Run

```bash
python os_project.py
```

---

## Usage

1. Set the **initial head position** (0–400) via the input or slider
2. Enter a **request sequence** as comma or space-separated values
3. Choose an **animation speed**
4. Click **▶ RUN SIMULATION**
5. The app will animate the best algorithm's trajectory and display a **comparison table** of all algorithms ranked by seek time

---

## Project Structure

```
os_project.py   # Single-file application — algorithms + UI
README.md
```
