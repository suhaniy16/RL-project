import tkinter as tk
from tkinter import ttk
from brain import StudyAI
from logic import run_simulation

# ── DESIGN SYSTEM ────────────────────────────────────────────────────────────
UI = {
    # Warm off-white / parchment palette
    "bg":           "#F5F0E8",      # warm parchment base
    "surface":      "#FDFAF4",      # card surface, soft cream
    "surface2":     "#EDE8DC",      # subtle inset / sidebar bg
    "border":       "#DDD8CC",      # gentle divider
    "border_dark":  "#C8C0B0",      # slightly stronger border

    # Terracotta + slate accent system
    "accent":       "#C0654A",      # terracotta / rust – main CTA
    "accent_light": "#E8927A",      # lighter hover tint
    "accent_muted": "#F0DDD7",      # very soft tint background
    "green":        "#4A8C6A",      # positive / growth indicator
    "green_muted":  "#D6EAE0",      # soft green background

    # Typography
    "text_h1":      "#1E1A14",      # near-black headings
    "text_body":    "#5A5248",      # warm mid-tone body
    "text_muted":   "#9C9488",      # placeholder / label text

    # Fonts – warm humanist choices
    "font_logo":    ("Georgia", 17, "bold"),
    "font_sub":     ("Georgia", 9, "italic"),
    "font_h2":      ("Georgia", 11, "bold"),
    "font_label":   ("Helvetica", 8),
    "font_label_b": ("Helvetica", 8, "bold"),
    "font_body":    ("Helvetica", 10),
    "font_body_b":  ("Helvetica", 10, "bold"),
    "font_number":  ("Georgia", 20, "bold"),
    "font_pct":     ("Georgia", 13, "bold"),
    "font_small":   ("Helvetica", 7),
}

SUBJECT_ICONS = {
    "Python":        "⌨",
    "Java":          "☕",
    "DSA":           "⎇",
    "Aptitude":      "⊞",
    "Communication": "❋",
}

class Synapse(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Synapse — Study Planner")
        self.geometry("1060x740")
        self.configure(bg=UI["bg"])
        self.resizable(True, True)

        self.diffs = {
            "Python": 0.9, "Java": 0.8, "DSA": 0.9,
            "Aptitude": 0.5, "Communication": 0.3
        }
        self.subjs = list(self.diffs.keys())
        self.ai = StudyAI(self.subjs)
        self.ai.load()

        self.vars = {s: tk.IntVar(value=40) for s in self.subjs}
        self._setup()

    def _setup(self):
        # ── Top nav bar ──────────────────────────────────────────────────────
        nav = tk.Frame(self, bg=UI["surface"], pady=0)
        nav.pack(fill="x")

        # Thin accent stripe at very top
        tk.Frame(nav, bg=UI["accent"], height=3).pack(fill="x")

        nav_inner = tk.Frame(nav, bg=UI["surface"], padx=48, pady=18)
        nav_inner.pack(fill="x")

        # Logo
        logo_frame = tk.Frame(nav_inner, bg=UI["surface"])
        logo_frame.pack(side="left")
        tk.Label(logo_frame, text="Synapse", font=UI["font_logo"],
                 bg=UI["surface"], fg=UI["text_h1"]).pack(side="left")
        
        # Nav tagline right
        tk.Label(nav_inner, text="Personalised · AI-Powered · Actionable",
                 font=UI["font_small"], bg=UI["surface"], fg=UI["text_muted"]).pack(side="right")

        # Thin border below nav
        tk.Frame(self, bg=UI["border"], height=1).pack(fill="x")

        # ── Main layout ──────────────────────────────────────────────────────
        main = tk.Frame(self, bg=UI["bg"])
        main.pack(fill="both", expand=True)
        main.columnconfigure(0, weight=0)   # sidebar fixed
        main.columnconfigure(1, weight=1)   # content expands
        main.rowconfigure(0, weight=1)

        # ── Sidebar ──────────────────────────────────────────────────────────
        aside = tk.Frame(main, bg=UI["surface2"])
        aside.grid(row=0, column=0, sticky="nsew")
        main.columnconfigure(0, minsize=300, weight=0)

        aside_inner = tk.Frame(aside, bg=UI["surface2"], padx=30, pady=32)
        aside_inner.pack(fill="both", expand=True)

        tk.Label(aside_inner, text="Skill Matrix",
                 font=UI["font_h2"], bg=UI["surface2"], fg=UI["text_h1"]).pack(anchor="w")
        tk.Label(aside_inner, text="Rate your current confidence",
                 font=UI["font_label"], bg=UI["surface2"], fg=UI["text_muted"]).pack(anchor="w", pady=(2, 20))

        # Skill sliders
        for s in self.subjs:
            card = tk.Frame(aside_inner, bg=UI["surface"],
                            highlightthickness=1, highlightbackground=UI["border"])
            card.pack(fill="x", pady=6)

            card_inner = tk.Frame(card, bg=UI["surface"], padx=14, pady=12)
            card_inner.pack(fill="x")

            # Header row
            head = tk.Frame(card_inner, bg=UI["surface"])
            head.pack(fill="x")

            icon = SUBJECT_ICONS.get(s, "•")
            tk.Label(head, text=f"{icon}  {s}",
                     font=UI["font_body_b"], bg=UI["surface"], fg=UI["text_h1"]).pack(side="left")

            v_lbl = tk.Label(head, text=f"{self.vars[s].get()}%",
                             font=UI["font_pct"], bg=UI["surface"], fg=UI["accent"])
            v_lbl.pack(side="right")

            # Custom rounded-feel trough via ttk style
            style_name = f"{s}.Horizontal.TScale"

            slider = tk.Scale(
                card_inner, from_=0, to=100, orient="horizontal",
                variable=self.vars[s],
                bg=UI["surface"], fg=UI["text_body"],
                highlightthickness=0,
                troughcolor=UI["border"],
                activebackground=UI["accent_light"],
                showvalue=False, width=5, sliderlength=18,
                command=lambda v, l=v_lbl: l.config(text=f"{int(float(v))}%")
            )
            slider.pack(fill="x", pady=(8, 0))

            # Confidence hint
            hint_frame = tk.Frame(card_inner, bg=UI["surface"])
            hint_frame.pack(fill="x", pady=(4, 0))
            for label, pos in [("Beginner", "left"), ("Expert", "right")]:
                tk.Label(hint_frame, text=label, font=UI["font_small"],
                         bg=UI["surface"], fg=UI["text_muted"]).pack(side=pos)

        # Spacer
        tk.Frame(aside_inner, bg=UI["surface2"], height=10).pack()

        # CTA button
        btn_frame = tk.Frame(aside_inner, bg=UI["surface2"])
        btn_frame.pack(fill="x", pady=(16, 0))

        self.btn = tk.Button(
            btn_frame, text="Generate My Roadmap →",
            font=UI["font_body_b"],
            bg=UI["accent"], fg="#FDFAF4",
            relief="flat", pady=14, padx=20,
            cursor="hand2", activebackground=UI["accent_light"],
            activeforeground="#FDFAF4",
            command=self.sync
        )
        self.btn.pack(fill="x")

        tk.Label(aside_inner, text="Results update instantly each time",
                 font=UI["font_small"], bg=UI["surface2"], fg=UI["text_muted"]).pack(pady=(8, 0))

        # Vertical divider
        tk.Frame(main, bg=UI["border"], width=1).grid(row=0, column=0, sticky="nse")

        # ── Roadmap panel ────────────────────────────────────────────────────
        right = tk.Frame(main, bg=UI["bg"])
        right.grid(row=0, column=1, sticky="nsew")

        # Panel header
        panel_head = tk.Frame(right, bg=UI["bg"], padx=44, pady=28)
        panel_head.pack(fill="x")

        tk.Label(panel_head, text="Your Study Roadmap",
                 font=("Georgia", 15, "bold"), bg=UI["bg"], fg=UI["text_h1"]).pack(side="left")

        self.badge = tk.Label(panel_head, text="",
                              font=UI["font_label_b"], bg=UI["green_muted"], fg=UI["green"],
                              padx=10, pady=4)
        self.badge.pack(side="right", pady=(4, 0))

        tk.Frame(right, bg=UI["border"], height=1).pack(fill="x", padx=44)

        # Scrollable content area (using canvas for scroll support)
        self.content_frame = tk.Frame(right, bg=UI["bg"])
        self.content_frame.pack(fill="both", expand=True, padx=44, pady=20)

        # Empty state
        self.hint_frame = tk.Frame(self.content_frame, bg=UI["bg"])
        self.hint_frame.pack(expand=True, fill="both")

        empty_box = tk.Frame(self.hint_frame, bg=UI["surface"],
                             highlightthickness=1, highlightbackground=UI["border"],
                             padx=40, pady=50)
        empty_box.place(relx=0.5, rely=0.45, anchor="center")

        tk.Label(empty_box, text="✦", font=("Georgia", 28),
                 bg=UI["surface"], fg=UI["border"]).pack()
        tk.Label(empty_box, text="No roadmap yet",
                 font=("Georgia", 13, "bold"), bg=UI["surface"], fg=UI["text_body"]).pack(pady=(12, 4))
        tk.Label(empty_box, text="Adjust your skill levels on the left\nand click Generate to begin.",
                 font=UI["font_body"], bg=UI["surface"], fg=UI["text_muted"],
                 justify="center").pack()

    def sync(self):
        # Clear content
        for w in self.content_frame.winfo_children():
            w.destroy()

        scores = {s: self.vars[s].get() / 100.0 for s in self.subjs}
        plan = run_simulation(self.ai, self.subjs, self.diffs, scores, explore=False)

        total_gain = sum(step["gain"] for step in plan)
        self.badge.config(text=f"  Est. total growth  +{total_gain:.0%}  ")

        for i, step in enumerate(plan):
            self._render_step(i, step, len(plan), scores)

    # ── Subject-specific plan content ────────────────────────────────────────
    PLANS = {
        "Python": {
            "beginner":     ["Learn variables, loops, and functions", "Complete 10 beginner exercises on HackerRank", "Build a simple calculator or to-do CLI app"],
            "intermediate": ["Study OOP: classes, inheritance, decorators", "Practice file I/O and exception handling", "Build a REST API with Flask or FastAPI"],
            "advanced":     ["Deep-dive into generators, asyncio, and metaclasses", "Optimise with profiling tools (cProfile, line_profiler)", "Contribute to an open-source Python project"],
        },
        "Java": {
            "beginner":     ["Understand JVM basics, types, and control flow", "Practice OOP: classes, interfaces, and inheritance", "Build a simple bank account simulator"],
            "intermediate": ["Study Collections, Generics, and Streams API", "Learn exception handling and multithreading basics", "Build a CRUD app with Spring Boot"],
            "advanced":     ["Master concurrency: locks, executors, CompletableFuture", "Explore JVM internals and memory management", "Design a microservice with Spring Boot + Docker"],
        },
        "DSA": {
            "beginner":     ["Revise arrays, strings, and basic recursion", "Solve 5 easy LeetCode problems daily", "Understand time/space complexity (Big-O)"],
            "intermediate": ["Study linked lists, stacks, queues, and trees", "Solve medium LeetCode problems on sliding window & BFS/DFS", "Practice sorting algorithms from scratch"],
            "advanced":     ["Master dynamic programming patterns", "Study graphs: Dijkstra, Floyd-Warshall, topological sort", "Mock interview: 2 hard problems per week timed"],
        },
        "Aptitude": {
            "beginner":     ["Review percentages, ratios, and averages", "Attempt 20 questions daily from IndiaBix", "Focus on speed: use shortcuts for multiplication"],
            "intermediate": ["Practice time & work, pipes & cisterns, profit & loss", "Attempt sectional mock tests (30 min per topic)", "Analyse mistakes and revisit weak areas weekly"],
            "advanced":     ["Solve full-length aptitude papers (TCS, Infosys pattern)", "Work on data interpretation and logical reasoning", "Target sub-60 sec per question consistently"],
        },
        "Communication": {
            "beginner":     ["Read aloud for 10 minutes daily to build fluency", "Record yourself speaking and review for filler words", "Practice introducing yourself clearly in 60 seconds"],
            "intermediate": ["Join a group discussion or debate practice session", "Write one structured email or summary per day", "Watch TED Talks and note structure & delivery techniques"],
            "advanced":     ["Present a 5-minute talk on a technical topic weekly", "Practise mock GDs and HR interview rounds", "Get feedback from peers and iterate on weak points"],
        },
    }

    def _get_plan_tier(self, score):
        if score < 0.4:   return "beginner"
        if score < 0.7:   return "intermediate"
        return "advanced"

    def _render_step(self, i, step, total, scores):
        subj  = step["subj"]
        score = scores[subj]
        tier  = self._get_plan_tier(score)
        tasks = self.PLANS.get(subj, {}).get(tier, ["Study core concepts", "Practice problems", "Review and revise"])

        # Outer card
        card = tk.Frame(self.content_frame, bg=UI["surface"],
                        highlightthickness=1, highlightbackground=UI["border"])
        card.pack(fill="x", pady=6)

        # ── Header row ───────────────────────────────────────────────────────
        header = tk.Frame(card, bg=UI["surface"], padx=24, pady=16)
        header.pack(fill="x")

        # Step badge
        num_badge = tk.Frame(header, bg=UI["accent_muted"], width=40, height=40)
        num_badge.pack(side="left")
        num_badge.pack_propagate(False)
        tk.Label(num_badge, text=str(i + 1), font=("Georgia", 13, "bold"),
                 bg=UI["accent_muted"], fg=UI["accent"]).place(relx=0.5, rely=0.5, anchor="center")

        # Subject name + tier label
        info = tk.Frame(header, bg=UI["surface"])
        info.pack(side="left", padx=(14, 0))

        icon = SUBJECT_ICONS.get(subj, "•")
        tk.Label(info, text=f"{icon}  {subj}",
                 font=("Georgia", 12, "bold"), bg=UI["surface"], fg=UI["text_h1"]).pack(anchor="w")

        tier_colors = {
            "beginner":     (UI["accent_muted"],  UI["accent"]),
            "intermediate": ("#FFF3DC",            "#B07D20"),
            "advanced":     (UI["green_muted"],    UI["green"]),
        }
        tc_bg, tc_fg = tier_colors[tier]
        tk.Label(info, text=f"  {tier.capitalize()} level  ",
                 font=UI["font_small"], bg=tc_bg, fg=tc_fg).pack(anchor="w", pady=(3, 0))

        # Growth pill (right side)
        gain_frame = tk.Frame(header, bg=UI["green_muted"],
                              highlightthickness=1, highlightbackground="#B8DCCB")
        gain_frame.pack(side="right")
        gain_inner = tk.Frame(gain_frame, bg=UI["green_muted"], padx=14, pady=8)
        gain_inner.pack()
        tk.Label(gain_inner, text=f"+{step['gain']:.1%}",
                 font=("Georgia", 13, "bold"), bg=UI["green_muted"], fg=UI["green"]).pack()
        tk.Label(gain_inner, text="est. growth",
                 font=UI["font_small"], bg=UI["green_muted"], fg=UI["green"]).pack()

        # ── Divider ──────────────────────────────────────────────────────────
        tk.Frame(card, bg=UI["border"], height=1).pack(fill="x", padx=24)

        # ── Task list ────────────────────────────────────────────────────────
        tasks_frame = tk.Frame(card, bg=UI["surface"], padx=24, pady=14)
        tasks_frame.pack(fill="x")

        tk.Label(tasks_frame, text="Recommended actions",
                 font=UI["font_label_b"], bg=UI["surface"], fg=UI["text_muted"]).pack(anchor="w", pady=(0, 8))

        for t, task in enumerate(tasks):
            row = tk.Frame(tasks_frame, bg=UI["surface"])
            row.pack(fill="x", pady=3)
            tk.Label(row, text=f"{t+1}.", font=UI["font_label_b"],
                     bg=UI["surface"], fg=UI["accent"], width=2).pack(side="left")
            tk.Label(row, text=task, font=UI["font_body"],
                     bg=UI["surface"], fg=UI["text_body"], anchor="w").pack(side="left", padx=(6, 0))

        # ── Progress bar ─────────────────────────────────────────────────────
        bar_frame = tk.Frame(card, bg=UI["surface"], padx=24, pady=(4, 14))
        bar_frame.pack(fill="x")

        bar_bg = tk.Frame(bar_frame, bg=UI["border"], height=4)
        bar_bg.pack(fill="x")

        fill_width = min(1.0, step["gain"] * 5)

        def draw_bar(event, bg=bar_bg, fw=fill_width):
            w = bg.winfo_width()
            bar_fill = tk.Frame(bg, bg=UI["green"], height=4, width=int(w * fw))
            bar_fill.place(x=0, y=0)

        bar_bg.bind("<Configure>", draw_bar)


if __name__ == "__main__":
    Synapse().mainloop()