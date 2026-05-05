import tkinter as tk
from tkinter import ttk, messagebox, font
import math
import time
import threading

# ─────────────────────────────────────────────
#  ALGORITHMS
# ─────────────────────────────────────────────

def fcfs(requests, head):
    order = [head] + requests
    seek = sum(abs(order[i] - order[i-1]) for i in range(1, len(order)))
    return order, seek

def scan(requests, head, disk_max=400):
    left  = sorted([r for r in requests if r <= head], reverse=True)
    right = sorted([r for r in requests if r >  head])
    order = [head] + right + ([disk_max] if right else []) + left
    # remove disk_max if it wasn't in requests
    seq   = [head] + right
    if right or not left:
        seq.append(disk_max)
    seq  += left
    seek  = sum(abs(seq[i] - seq[i-1]) for i in range(1, len(seq)))
    return seq, seek

def cscan(requests, head, disk_max=400):
    right = sorted([r for r in requests if r >  head])
    left  = sorted([r for r in requests if r <= head])
    seq   = [head] + right
    if right or left:
        seq.append(disk_max)
        seq.append(0)
    seq  += left
    seek  = sum(abs(seq[i] - seq[i-1]) for i in range(1, len(seq)))
    return seq, seek

def look(requests, head):
    """LOOK: like SCAN but only goes as far as the last request (no disk-end touch)."""
    left  = sorted([r for r in requests if r <= head], reverse=True)
    right = sorted([r for r in requests if r >  head])
    seq   = [head] + right + left
    seek  = sum(abs(seq[i] - seq[i-1]) for i in range(1, len(seq)))
    return seq, seek

def clook(requests, head):
    """C-LOOK: services right side, jumps to lowest remaining, services upward."""
    right = sorted([r for r in requests if r >  head])
    left  = sorted([r for r in requests if r <= head])
    seq   = [head] + right + left
    seek  = sum(abs(seq[i] - seq[i-1]) for i in range(1, len(seq)))
    return seq, seek

def best_algorithm(requests, head):
    results = {
        "FCFS":   fcfs(requests,  head),
        "SCAN":   scan(requests,  head),
        "C-SCAN": cscan(requests, head),
        "LOOK":   look(requests,  head),
        "C-LOOK": clook(requests, head),
    }
    best = min(results, key=lambda k: results[k][1])
    return best, results


# ─────────────────────────────────────────────
#  COLOUR PALETTE  (minimal, cool, clean)
# ─────────────────────────────────────────────
BG       = "#0d0d0f"
SURFACE  = "#16161a"
CARD     = "#1c1c22"
BORDER   = "#2a2a35"
ACCENT   = "#7c6af7"      # violet
ACCENT2  = "#4ecdc4"      # teal
ACCENT3  = "#f7c948"      # amber
TEXT     = "#e8e8f0"
SUBTEXT  = "#8888aa"
SUCCESS  = "#5dde8a"
DANGER   = "#f76a6a"
WHITE    = "#ffffff"


# ─────────────────────────────────────────────
#  MAIN APP
# ─────────────────────────────────────────────
class DiskSchedulerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Disk Scheduling Simulator")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.minsize(900, 680)

        # center window
        w, h = 1100, 760
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry(f"{w}x{h}+{(sw-w)//2}+{(sh-h)//2}")

        self._define_fonts()
        self._build_ui()

    # ── fonts ──────────────────────────────────
    def _define_fonts(self):
        self.f_title  = ("Courier New", 20, "bold")
        self.f_head   = ("Courier New", 13, "bold")
        self.f_body   = ("Consolas",    11)
        self.f_small  = ("Consolas",    10)
        self.f_label  = ("Consolas",    10, "bold")
        self.f_result = ("Courier New", 14, "bold")
        self.f_badge  = ("Consolas",    9,  "bold")

    # ── root layout ────────────────────────────
    def _build_ui(self):
        # header bar
        hdr = tk.Frame(self, bg=SURFACE, height=56)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="⬡  DISK SCHEDULING SIMULATOR",
                 font=self.f_title, bg=SURFACE, fg=ACCENT).pack(side="left", padx=24, pady=12)
        tk.Label(hdr, text="Operating Systems • Visual Tool",
                 font=self.f_small, bg=SURFACE, fg=SUBTEXT).pack(side="right", padx=24)

        # separator
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")

        # two-column body
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, padx=18, pady=18)
        body.columnconfigure(0, weight=0, minsize=310)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self._build_left_panel(body)
        self._build_right_panel(body)

        # footer
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x")
        tk.Label(self, text="Project done by Bazif & Sawaira",
                 font=self.f_label, bg=SURFACE, fg=ACCENT2,
                 pady=8).pack(fill="x")

    # ── LEFT PANEL ─────────────────────────────
    def _build_left_panel(self, parent):
        pane = tk.Frame(parent, bg=CARD, bd=0,
                        highlightbackground=BORDER, highlightthickness=1)
        pane.grid(row=0, column=0, sticky="nsew", padx=(0,14))

        def section(label):
            tk.Label(pane, text=label, font=self.f_label,
                     bg=CARD, fg=ACCENT2, anchor="w").pack(fill="x", padx=18, pady=(14,2))
            tk.Frame(pane, bg=BORDER, height=1).pack(fill="x", padx=18)

        # ── disk head
        section("INITIAL HEAD POSITION")
        hf = tk.Frame(pane, bg=CARD)
        hf.pack(fill="x", padx=18, pady=6)
        self.head_var = tk.StringVar(value="53")
        head_entry = tk.Entry(hf, textvariable=self.head_var, width=8,
                              font=self.f_head, bg=SURFACE, fg=ACCENT,
                              insertbackground=ACCENT, bd=0,
                              highlightbackground=BORDER, highlightthickness=1,
                              relief="flat")
        head_entry.pack(side="left")
        tk.Label(hf, text="  (0 – 400)", font=self.f_small,
                 bg=CARD, fg=SUBTEXT).pack(side="left")

        # live slider
        self.head_slider = tk.Scale(pane, from_=0, to=400, orient="horizontal",
                                    variable=self.head_var,
                                    bg=CARD, fg=SUBTEXT, troughcolor=BORDER,
                                    activebackground=ACCENT, highlightthickness=0,
                                    sliderrelief="flat", bd=0, showvalue=False,
                                    length=260)
        self.head_slider.pack(padx=18, pady=(0,6))

        # ── request sequence
        section("REQUEST SEQUENCE  (0 – 400)")
        self.req_text = tk.Text(pane, height=5, width=34,
                                font=self.f_body, bg=SURFACE, fg=TEXT,
                                insertbackground=TEXT, bd=0, relief="flat",
                                highlightbackground=BORDER, highlightthickness=1,
                                wrap="word")
        self.req_text.insert("1.0", "98, 183, 37, 122, 14, 124, 65, 67")
        self.req_text.pack(padx=18, pady=8)
        tk.Label(pane, text="Comma or space separated",
                 font=self.f_small, bg=CARD, fg=SUBTEXT).pack()

        # preset buttons
        section("QUICK PRESETS")
        presets = [
            ("Classic",   "98, 183, 37, 122, 14, 124, 65, 67"),
            ("Dense",     "10, 22, 35, 40, 55, 70, 85, 95, 102, 118"),
            ("Scattered", "320, 5, 199, 88, 342, 17, 267, 390, 44, 150"),
        ]
        pf = tk.Frame(pane, bg=CARD)
        pf.pack(padx=18, pady=8, fill="x")
        for name, vals in presets:
            b = tk.Button(pf, text=name, font=self.f_small,
                          bg=BORDER, fg=TEXT, activebackground=ACCENT,
                          activeforeground=WHITE, bd=0, padx=10, pady=4,
                          cursor="hand2",
                          command=lambda v=vals: self._apply_preset(v))
            b.pack(side="left", padx=3)

        # animation speed
        section("ANIMATION SPEED")
        sf = tk.Frame(pane, bg=CARD)
        sf.pack(fill="x", padx=18, pady=6)
        self.speed_var = tk.IntVar(value=1)
        for lbl, val in [("Slow", 1), ("Normal", 2), ("Fast", 3)]:
            tk.Radiobutton(sf, text=lbl, variable=self.speed_var, value=val,
                           font=self.f_small, bg=CARD, fg=SUBTEXT,
                           selectcolor=ACCENT, activebackground=CARD,
                           cursor="hand2").pack(side="left", padx=6)

        # run button
        tk.Frame(pane, bg=CARD, height=10).pack()
        self.run_btn = tk.Button(pane, text="▶  RUN SIMULATION",
                                 font=self.f_head, bg=ACCENT, fg=WHITE,
                                 activebackground="#9d8fff", activeforeground=WHITE,
                                 bd=0, pady=10, cursor="hand2",
                                 command=self._run_simulation)
        self.run_btn.pack(fill="x", padx=18, pady=(0,6))

        self.clear_btn = tk.Button(pane, text="✕  CLEAR",
                                   font=self.f_small, bg=SURFACE, fg=SUBTEXT,
                                   activebackground=BORDER, activeforeground=TEXT,
                                   bd=0, pady=6, cursor="hand2",
                                   command=self._clear_all)
        self.clear_btn.pack(fill="x", padx=18, pady=(0,14))

    # ── RIGHT PANEL ────────────────────────────
    def _build_right_panel(self, parent):
        pane = tk.Frame(parent, bg=BG)
        pane.grid(row=0, column=1, sticky="nsew")
        pane.rowconfigure(1, weight=1)
        pane.columnconfigure(0, weight=1)

        # result card (top)
        self.result_frame = tk.Frame(pane, bg=CARD,
                                     highlightbackground=BORDER, highlightthickness=1)
        self.result_frame.grid(row=0, column=0, sticky="ew", pady=(0,12))
        self.result_label = tk.Label(self.result_frame,
                                     text="Run the simulation to see results.",
                                     font=self.f_body, bg=CARD, fg=SUBTEXT,
                                     pady=12, padx=18, anchor="w")
        self.result_label.pack(fill="x")

        # graph area (scrollable)
        graph_wrap = tk.Frame(pane, bg=CARD,
                              highlightbackground=BORDER, highlightthickness=1)
        graph_wrap.grid(row=1, column=0, sticky="nsew")
        graph_wrap.rowconfigure(0, weight=1)
        graph_wrap.columnconfigure(0, weight=1)

        # label
        self.graph_title = tk.Label(graph_wrap, text="TRAJECTORY GRAPH",
                                    font=self.f_label, bg=CARD, fg=ACCENT2,
                                    anchor="w", padx=14, pady=8)
        self.graph_title.pack(fill="x")
        tk.Frame(graph_wrap, bg=BORDER, height=1).pack(fill="x")

        # canvas + scrollbar
        scroll_frame = tk.Frame(graph_wrap, bg=CARD)
        scroll_frame.pack(fill="both", expand=True)
        self.h_scroll = tk.Scrollbar(scroll_frame, orient="horizontal",
                                     bg=SURFACE, troughcolor=BORDER)
        self.h_scroll.pack(side="bottom", fill="x")
        self.canvas = tk.Canvas(scroll_frame, bg=SURFACE, bd=0, highlightthickness=0,
                                xscrollcommand=self.h_scroll.set)
        self.canvas.pack(fill="both", expand=True)
        self.h_scroll.config(command=self.canvas.xview)

        # comparison + alt buttons at bottom
        self.bottom_frame = tk.Frame(pane, bg=BG)
        self.bottom_frame.grid(row=2, column=0, sticky="ew", pady=(10,0))

    # ── HELPERS ────────────────────────────────
    def _apply_preset(self, vals):
        self.req_text.delete("1.0", "end")
        self.req_text.insert("1.0", vals)

    def _clear_all(self):
        self.canvas.delete("all")
        self.result_label.config(text="Run the simulation to see results.", fg=SUBTEXT)
        self.graph_title.config(text="TRAJECTORY GRAPH")
        for w in self.bottom_frame.winfo_children():
            w.destroy()

    def _parse_inputs(self):
        try:
            head = int(self.head_var.get())
            if not (0 <= head <= 400):
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Head position must be an integer 0–400.")
            return None, None

        raw = self.req_text.get("1.0", "end").replace(",", " ").split()
        try:
            reqs = [int(x) for x in raw]
            if any(not (0 <= r <= 400) for r in reqs):
                raise ValueError
            if len(reqs) < 2:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error",
                                 "Enter at least 2 integers 0–400, comma/space separated.")
            return None, None
        return head, reqs

    # ── RUN ────────────────────────────────────
    def _run_simulation(self):
        head, reqs = self._parse_inputs()
        if head is None:
            return

        self._clear_all()
        best_name, all_results = best_algorithm(reqs, head)
        best_seq, best_seek   = all_results[best_name]

        # result banner
        color_map = {
            "FCFS":   ACCENT,
            "SCAN":   ACCENT2,
            "C-SCAN": ACCENT3,
            "LOOK":   "#f76a9a",   # pink
            "C-LOOK": "#5daaff",   # sky blue
        }
        bc = color_map[best_name]
        self.result_label.config(
            text=f"✔  Best Algorithm: {best_name}   |   Seek Time: {best_seek} cylinders"
                 f"   |   Requests: {len(reqs)}   |   Head: {head}",
            fg=bc)
        self.graph_title.config(text=f"TRAJECTORY  —  {best_name}")

        # animate graph
        speed_delay = {1: 120, 2: 50, 3: 14}[self.speed_var.get()]
        threading.Thread(target=self._animate_graph,
                         args=(best_seq, bc, speed_delay), daemon=True).start()

        # build comparison + alt buttons after tiny delay
        self.after(200, lambda: self._build_bottom(best_name, all_results, color_map))

    # ── GRAPH ANIMATION ────────────────────────
    def _animate_graph(self, sequence, color, delay_ms):
        self.canvas.delete("all")
        n      = len(sequence)
        margin = {"left": 60, "right": 40, "top": 30, "bottom": 50}
        step_w = 90
        total_w = margin["left"] + (n - 1) * step_w + margin["right"]

        self.canvas.config(scrollregion=(0, 0, total_w, 10))  # temp
        self.canvas.update()
        ch = self.canvas.winfo_height() or 340
        plot_h = ch - margin["top"] - margin["bottom"]

        def cy(val):
            return margin["top"] + plot_h - (val / 400) * plot_h

        total_w = max(total_w, self.canvas.winfo_width())
        self.canvas.config(scrollregion=(0, 0, total_w, ch))

        # grid lines
        for tick in range(0, 401, 50):
            y = cy(tick)
            self.canvas.create_line(margin["left"], y, total_w - margin["right"], y,
                                    fill=BORDER, dash=(4, 6))
            self.canvas.create_text(margin["left"] - 8, y, text=str(tick),
                                    font=self.f_small, fill=SUBTEXT, anchor="e")

        # x axis labels
        for i, val in enumerate(sequence):
            x = margin["left"] + i * step_w
            self.canvas.create_text(x, ch - margin["bottom"] + 14, text=str(val),
                                    font=self.f_small, fill=SUBTEXT)

        # animate step by step
        points = [(margin["left"] + i * step_w, cy(sequence[i]))
                  for i in range(n)]

        for i in range(1, n):
            x0, y0 = points[i-1]
            x1, y1 = points[i]
            # smooth interpolation: draw in sub-steps
            steps = max(8, int(abs(y1 - y0) / 6))
            for s in range(1, steps + 1):
                t  = s / steps
                xi = x0 + (x1 - x0) * t
                yi = y0 + (y1 - y0) * t
                self.canvas.create_line(x0 + (x1-x0)*(s-1)/steps,
                                        y0 + (y1-y0)*(s-1)/steps,
                                        xi, yi,
                                        fill=color, width=2.5, capstyle="round")
                self.canvas.update()
                time.sleep(delay_ms / 1000 / steps)
            # node circle
            r = 5
            self.canvas.create_oval(x1-r, y1-r, x1+r, y1+r,
                                    fill=color, outline=SURFACE, width=2)
            self.canvas.create_text(x1, y1 - 14, text=str(sequence[i]),
                                    font=self.f_small, fill=color)
            self.canvas.update()

        # draw head marker at start
        x0, y0 = points[0]
        r = 7
        self.canvas.create_oval(x0-r, y0-r, x0+r, y0+r,
                                 fill=WHITE, outline=color, width=2)
        self.canvas.create_text(x0, y0 - 16, text=f"HEAD\n{sequence[0]}",
                                 font=self.f_small, fill=WHITE, justify="center")
        self.canvas.update()

    # ── BOTTOM SECTION ─────────────────────────
    def _build_bottom(self, best_name, all_results, color_map):
        for w in self.bottom_frame.winfo_children():
            w.destroy()

        # comparison table
        table_frame = tk.Frame(self.bottom_frame, bg=CARD,
                               highlightbackground=BORDER, highlightthickness=1)
        table_frame.pack(fill="x", pady=(0, 10))

        tk.Label(table_frame, text="COMPARISON TABLE",
                 font=self.f_label, bg=CARD, fg=ACCENT2,
                 anchor="w", padx=14, pady=6).grid(row=0, column=0, columnspan=4, sticky="ew")
        tk.Frame(table_frame, bg=BORDER, height=1).grid(row=1, column=0, columnspan=4, sticky="ew")

        headers = ["Algorithm", "Seek Time", "Δ vs Best", ""]
        col_w   = [130, 130, 130, 160]
        for c, (h, cw) in enumerate(zip(headers, col_w)):
            tk.Label(table_frame, text=h, font=self.f_label,
                     bg=CARD, fg=SUBTEXT, width=cw//8,
                     anchor="center").grid(row=2, column=c, padx=6, pady=4)

        best_seek = all_results[best_name][1]
        sorted_results = sorted(all_results.items(), key=lambda x: x[1][1])
        for r_idx, (algo, (_, seek)) in enumerate(sorted_results, start=3):
            is_best = (algo == best_name)
            row_bg  = SURFACE if is_best else CARD
            fg_col  = color_map[algo] if is_best else SUBTEXT
            delta   = seek - best_seek

            tk.Label(table_frame, text=algo, font=self.f_body,
                     bg=row_bg, fg=fg_col,
                     anchor="center").grid(row=r_idx, column=0, padx=6, pady=3, sticky="ew")
            tk.Label(table_frame, text=f"{seek} cyl", font=self.f_body,
                     bg=row_bg, fg=fg_col,
                     anchor="center").grid(row=r_idx, column=1, padx=6, sticky="ew")
            tk.Label(table_frame, text=f"+{delta}" if delta else "BEST ✔",
                     font=self.f_body, bg=row_bg,
                     fg=DANGER if delta else SUCCESS,
                     anchor="center").grid(row=r_idx, column=2, padx=6, sticky="ew")

            if not is_best:
                btn = tk.Button(table_frame, text=f"View {algo} Seek Details",
                                font=self.f_small, bg=BORDER, fg=TEXT,
                                activebackground=color_map[algo], activeforeground=WHITE,
                                bd=0, padx=10, pady=3, cursor="hand2",
                                command=lambda a=algo, s=seek, seq=all_results[algo][0]:
                                    self._show_alt_popup(a, s, seq))
                btn.grid(row=r_idx, column=3, padx=10, pady=3)
            else:
                tk.Label(table_frame, text="(graph shown above)", font=self.f_small,
                         bg=row_bg, fg=SUBTEXT).grid(row=r_idx, column=3, padx=10)

    # ── ALT ALGORITHM POPUP ────────────────────
    def _show_alt_popup(self, algo, seek, sequence):
        pop = tk.Toplevel(self)
        pop.title(f"{algo} — Seek Details")
        pop.configure(bg=BG)
        pop.resizable(False, False)
        w, h = 480, 400
        sx, sy = self.winfo_screenwidth(), self.winfo_screenheight()
        pop.geometry(f"{w}x{h}+{(sx-w)//2}+{(sy-h)//2}")

        # header
        hdr = tk.Frame(pop, bg=SURFACE)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"⬡  {algo}  ALGORITHM", font=self.f_head,
                 bg=SURFACE, fg=ACCENT, pady=12, padx=18).pack(side="left")

        tk.Frame(pop, bg=BORDER, height=1).pack(fill="x")

        # seek badge
        badge = tk.Frame(pop, bg=CARD, pady=10)
        badge.pack(fill="x", padx=20, pady=12)
        tk.Label(badge, text=f"Total Seek Time", font=self.f_small,
                 bg=CARD, fg=SUBTEXT).pack()
        tk.Label(badge, text=f"{seek} cylinders", font=("Courier New", 22, "bold"),
                 bg=CARD, fg=ACCENT3).pack()

        # sequence display
        tk.Label(pop, text="HEAD MOVEMENT SEQUENCE", font=self.f_label,
                 bg=BG, fg=ACCENT2, anchor="w").pack(fill="x", padx=20)
        tk.Frame(pop, bg=BORDER, height=1).pack(fill="x", padx=20)

        seq_frame = tk.Frame(pop, bg=SURFACE)
        seq_frame.pack(fill="both", expand=True, padx=20, pady=10)

        sb = tk.Scrollbar(seq_frame)
        sb.pack(side="right", fill="y")
        txt = tk.Text(seq_frame, font=self.f_body, bg=SURFACE, fg=TEXT,
                      bd=0, highlightthickness=0, yscrollcommand=sb.set,
                      wrap="word")
        txt.pack(fill="both", expand=True)
        sb.config(command=txt.yview)

        # write step-by-step
        txt.insert("end", f"Sequence ({len(sequence)} positions):\n\n", "hdr")
        txt.tag_config("hdr", foreground=ACCENT, font=self.f_label)
        for i in range(len(sequence)):
            if i == 0:
                txt.insert("end", f"  Start  →  {sequence[i]}\n", "start")
                txt.tag_config("start", foreground=ACCENT2)
            else:
                dist = abs(sequence[i] - sequence[i-1])
                txt.insert("end", f"  Step {i:>2}  →  {sequence[i]:>4}   "
                                  f"(moved {dist} cylinders)\n")
        txt.config(state="disabled")

        tk.Button(pop, text="Close", font=self.f_small, bg=ACCENT, fg=WHITE,
                  activebackground="#9d8fff", bd=0, pady=6, cursor="hand2",
                  command=pop.destroy).pack(fill="x", padx=20, pady=(0,16))


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if __name__ == "__main__":
    app = DiskSchedulerApp()
    app.mainloop()