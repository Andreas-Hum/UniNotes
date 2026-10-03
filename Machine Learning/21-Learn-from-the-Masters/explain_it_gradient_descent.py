"""Explain-it video: gradient descent and the learning rate.

Render (from this folder):
    manim -pql explain_it_gradient_descent.py GradientDescent     # quick 480p preview
    manim -qh  explain_it_gradient_descent.py GradientDescent     # 1080p final
    manim -ql --format=gif explain_it_gradient_descent.py GradientDescent

Uses only Text (no LaTeX needed). Structure = the 5 beats from "Explain-it Videos.md":
hook → intuition → the rule → what can go wrong → recap.
"""
from manim import *

LOSS = lambda w: 0.5 * w ** 2 + 0.5          # a simple bowl, minimum at w = 0
SLOPE = lambda w: w


class GradientDescent(Scene):
    def construct(self):
        self.hook()
        axes, curve = self.intuition()
        self.the_rule(axes, curve)
        self.what_can_go_wrong()
        self.recap()

    # 1 ── Hook: the question the video answers ───────────────────────────
    def hook(self):
        q = Text("How does a neural network\nactually learn?", font_size=48, line_spacing=1.2)
        sub = Text("One idea: walk downhill.", font_size=32, color=YELLOW).next_to(q, DOWN, buff=0.6)
        self.play(Write(q), run_time=2)
        self.play(FadeIn(sub, shift=UP * 0.3))
        self.wait(1.5)
        self.play(FadeOut(q), FadeOut(sub))

    # 2 ── Intuition: loss is a landscape, we are a ball on it ────────────
    def intuition(self):
        axes = Axes(x_range=[-3, 3, 1], y_range=[0, 5, 1], x_length=8, y_length=4,
                    axis_config={"include_tip": False}).shift(UP * 0.2)
        xl = Text("weight w", font_size=24).next_to(axes.x_axis, DOWN, buff=0.2)
        yl = Text("loss", font_size=24).next_to(axes.y_axis, UP, buff=0.2)
        curve = axes.plot(LOSS, x_range=[-2.9, 2.9], color=BLUE)
        title = Text("The loss landscape", font_size=36).to_edge(UP)
        self.play(Write(title), Create(axes), FadeIn(xl), FadeIn(yl))
        self.play(Create(curve), run_time=1.5)

        w = ValueTracker(-2.5)
        ball = always_redraw(lambda: Dot(axes.c2p(w.get_value(), LOSS(w.get_value())), color=YELLOW, radius=0.12))
        note = Text("each point = one setting of the weights", font_size=26).to_edge(DOWN)
        self.play(FadeIn(ball), Write(note))
        self.play(w.animate.set_value(2.5), run_time=2.5, rate_func=there_and_back)
        low = Text("goal: the lowest point", font_size=26, color=GREEN).to_edge(DOWN)
        self.play(ReplacementTransform(note, low))
        goal = Dot(axes.c2p(0, LOSS(0)), color=GREEN)
        self.play(Indicate(goal, scale_factor=2))
        self.wait(1)
        self.play(FadeOut(ball), FadeOut(low), FadeOut(title), FadeOut(goal))
        self.axes_labels = VGroup(xl, yl)
        return axes, curve

    # 3 ── The rule: step against the slope ───────────────────────────────
    def the_rule(self, axes, curve):
        title = Text("Look at the slope, step the other way", font_size=34).to_edge(UP)
        self.play(Write(title))
        w = ValueTracker(-2.5)
        ball = always_redraw(lambda: Dot(axes.c2p(w.get_value(), LOSS(w.get_value())), color=YELLOW, radius=0.12))
        tangent = always_redraw(lambda: axes.get_secant_slope_group(
            w.get_value(), curve, dx=0.01, secant_line_length=2.5, secant_line_color=ORANGE).submobjects[-1])
        self.play(FadeIn(ball), Create(tangent))

        rule = Text("new w  =  w  −  learning rate × slope", font_size=30,
                    t2c={"learning rate": YELLOW, "slope": ORANGE}).to_edge(DOWN)
        self.play(Write(rule), run_time=2)
        lr = 0.35
        for _ in range(6):
            self.play(w.animate.set_value(w.get_value() - lr * SLOPE(w.get_value())), run_time=0.8)
        small = Text("steps shrink by themselves: the slope flattens near the bottom", font_size=24, color=GREEN)
        small.next_to(rule, UP, buff=0.25)
        self.play(FadeIn(small))
        self.wait(2)
        self.play(*map(FadeOut, [title, ball, tangent, rule, small, axes, curve, self.axes_labels]))

    # 4 ── What can go wrong: the learning rate ───────────────────────────
    def what_can_go_wrong(self):
        title = Text("The one knob that matters: the learning rate", font_size=32).to_edge(UP)
        self.play(Write(title))
        settings = [(0.05, "too small", RED), (0.6, "about right", GREEN), (2.05, "too large", RED)]
        panels, balls, trackers = VGroup(), [], []
        for lr, name, col in settings:
            ax = Axes(x_range=[-3, 3, 1], y_range=[0, 5, 1], x_length=3.6, y_length=2.6,
                      axis_config={"include_tip": False, "include_ticks": False})
            cv = ax.plot(LOSS, x_range=[-2.9, 2.9], color=BLUE)
            lab = Text(f"{name}\nlr = {lr}", font_size=22, color=col, line_spacing=1).next_to(ax, DOWN, buff=0.2)
            panels.add(VGroup(ax, cv, lab))
        panels.arrange(RIGHT, buff=0.5).shift(DOWN * 0.3)
        self.play(FadeIn(panels))
        for (lr, _, _), p in zip(settings, panels):
            t = ValueTracker(-2.2); ax = p[0]
            balls.append(always_redraw(lambda t=t, ax=ax: Dot(
                ax.c2p(np.clip(t.get_value(), -2.9, 2.9), min(LOSS(np.clip(t.get_value(), -2.9, 2.9)), 5)),
                color=YELLOW, radius=0.08)))
            trackers.append((t, lr))
        self.play(*map(FadeIn, balls))
        for _ in range(8):
            self.play(*[t.animate.set_value(t.get_value() - lr * SLOPE(t.get_value())) for t, lr in trackers], run_time=0.6)
        verdict = Text("crawls  ·  converges  ·  bounces out and diverges", font_size=26).to_edge(DOWN)
        self.play(Write(verdict))
        self.wait(2)
        self.play(*map(FadeOut, [title, panels, verdict, *balls]))

    # 5 ── Recap: what to remember ────────────────────────────────────────
    def recap(self):
        title = Text("Recap", font_size=40).to_edge(UP)
        points = VGroup(
            Text("1. Training = finding low points of the loss", font_size=28),
            Text("2. The slope (gradient) says which way is uphill", font_size=28),
            Text("3. Step against it, scaled by the learning rate", font_size=28),
            Text("4. Too small: slow.  Too large: diverges.", font_size=28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        self.play(Write(title))
        for p in points:
            self.play(FadeIn(p, shift=RIGHT * 0.3), run_time=0.8)
        nxt = Text("Next: with millions of weights, the slope becomes a gradient vector.",
                   font_size=24, color=YELLOW).to_edge(DOWN)
        self.play(FadeIn(nxt))
        self.wait(2.5)
