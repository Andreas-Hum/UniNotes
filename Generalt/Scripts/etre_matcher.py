#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parametric ETRE-like matcher with PLOTS:
- Learns (per window) the best time-scale s* from a small grid and amplitude α* (closed-form).
- Matches the atom ⟨ f^δ ⟩[D, D] using robust tube membership with tolerance δ and coverage.
- Finds early pairs P · Σ*[g_min, g_max] · P (gap guard).
- PLOTS:
    (1) Time series with matched windows shaded; early-pair gaps hatched.
    (2) "What it learned": top-K matched windows aligned vs their learned template (α* f_{s*}),
        including f±δ tubes and the mean window curve.

Math/automata mapping (intuitively):
- Duration guard: fixed D (seconds) ⇒ window length n = round(D*fs).
- Value guard: |(w - mean(w)) - α*(f_s - mean(f_s))| ≤ δ for ≥ coverage fraction.
- Gap guard: if matches start at i and j, accept pair iff (t[j] - t[i]) ∈ [g_min, g_max].

Run:
    pip install numpy matplotlib
    python learned_patterns_plot.py
"""

import numpy as np
import matplotlib.pyplot as plt

from numpy.lib.stride_tricks import sliding_window_view


# ---------------------------
# Template / shape
# ---------------------------

def qrs_like_pulse(local_t, amp=1.0, width=0.015):
    """Simple spike-like function f0(t)."""
    g1 = amp * np.exp(-0.5 * (local_t / width) ** 2)
    g2 = -0.4 * amp * np.exp(-0.5 * ((local_t - 2 * width) / (1.4 * width)) ** 2)
    return g1 + g2


def build_template(fs, D, base_amp=0.9, time_scale=1.0, width=0.012):
    """
    Build f_s on [0, D] for a given time_scale s: center the pulse and stretch by s.
    """
    n = max(5, int(round(D * fs)))
    local = np.linspace(0, D, n, endpoint=False)
    centered = (local - D / 2.0) / max(time_scale, 1e-6)
    f = qrs_like_pulse(centered, amp=base_amp, width=width)
    return f  # length n


# ---------------------------
# Synthetic data
# ---------------------------

def make_signal(fs=500, T=10.0, seed=7):
    rng = np.random.default_rng(seed)
    t = np.arange(0.0, T, 1.0/fs)
    N = t.size

    base = 0.12*np.sin(2*np.pi*0.6*t) + 0.06*np.sin(2*np.pi*1.1*t + 0.7)
    noise = rng.normal(0.0, 0.05, size=N)
    x = base + noise

    # Inject a few spikes (two early pairs)
    centers = np.array([1.00, 1.55, 3.20, 5.00, 5.42, 7.40, 8.70])
    for c in centers:
        idx = np.argmin(np.abs(t - c))
        half = int(0.035 * fs)
        i0 = max(0, idx - half)
        i1 = min(N, idx + half)
        local_t = t[i0:i1] - t[idx]
        x[i0:i1] += qrs_like_pulse(local_t, amp=0.9, width=0.012)

    return t, x, centers


# ---------------------------
# Vectorized core helpers
# ---------------------------

def window_matrix(x, n):
    """Sliding window view (M, n) where rows are x[i:i+n]."""
    if n > len(x):
        return np.empty((0, n), dtype=float)
    return sliding_window_view(x, n)


def minimal_delta_per_window_for_f(W, f, coverage=0.9, fit_alpha=True):
    """
    For a single template f, compute per-window:
      α* (least squares) and δ* (minimal tube radius for given coverage).
    Returns (delta_star: (M,), alpha_star: (M,))
    """
    # Center windows
    Wc = W - W.mean(axis=1, keepdims=True)   # (M, n)

    # Center template
    f = np.asarray(f, dtype=float)
    f_c = f - f.mean()                        # (n,)
    denom = float(np.dot(f_c, f_c)) or 1e-12

    if fit_alpha:
        alphas = (Wc @ f_c) / denom          # (M,)
    else:
        alphas = np.ones(Wc.shape[0], dtype=float)

    # Residuals: |Wc - α f_c|
    R = np.abs(Wc - alphas[:, None] * f_c[None, :])

    p = float(np.clip(coverage, 0.0, 1.0))
    delta_star = np.quantile(R, p, axis=1)    # (M,)

    return delta_star, alphas


def learn_best_scale_and_alpha(W, fs, D, base_amp, scales, coverage=0.9, fit_alpha=True):
    """
    For each window (row of W), evaluate a small set of scales s∈scales and
    pick the s* that minimizes δ*. Return arrays of:
      best_delta: (M,), best_alpha: (M,), best_scale_idx: (M,), and the n (window length).
    """
    n = W.shape[1]
    S = len(scales)
    M = W.shape[0]

    if M == 0 or S == 0:
        return (np.array([]), np.array([]), np.array([]), n)

    delta_stack = np.zeros((S, M), dtype=float)
    alpha_stack = np.zeros((S, M), dtype=float)

    for si, s in enumerate(scales):
        f_s = build_template(fs, D, base_amp=base_amp, time_scale=s)
        dstar, astar = minimal_delta_per_window_for_f(W, f_s, coverage=coverage, fit_alpha=fit_alpha)
        delta_stack[si, :] = dstar
        alpha_stack[si, :] = astar

    best_si = np.argmin(delta_stack, axis=0)         # (M,)
    best_delta = delta_stack[best_si, np.arange(M)]  # (M,)
    best_alpha = alpha_stack[best_si, np.arange(M)]  # (M,)

    return best_delta, best_alpha, best_si, n


def nms_local_minima(values, radius):
    """
    Non-maximum suppression but for local MINIMA (we keep low δ*).
    Returns sorted indices kept.
    """
    if radius <= 0 or values.size == 0:
        return np.arange(values.size, dtype=int)

    M = values.size
    order = np.argsort(values)  # low to high
    taken = np.zeros(M, dtype=bool)
    kept = []

    for idx in order:
        if taken[idx]:
            continue
        kept.append(idx)
        lo = max(0, idx - radius)
        hi = min(M, idx + radius + 1)
        taken[lo:hi] = True

    kept.sort()
    return np.array(kept, dtype=int)


def early_pairs_from_indices(match_idx, fs, gap_min, gap_max):
    """Compute early pairs using two-pointer sweep."""
    if len(match_idx) == 0:
        return []
    t = match_idx / fs
    pairs = []
    j = 0
    for i in range(len(t)):
        while j < len(t) and t[j] - t[i] < gap_min:
            j += 1
        k = j
        while k < len(t) and t[k] - t[i] <= gap_max:
            pairs.append((match_idx[i], match_idx[k]))
            k += 1
    return pairs


# ---------------------------
# Plotting
# ---------------------------

def plot_time_series_with_matches(t, x, match_idx, n, fs, early_pairs, title):
    """Plot full time series; shade matched windows; hatch early-pair gaps."""
    plt.figure(figsize=(12, 5))
    plt.plot(t, x, lw=1.0, label="signal")

    D = n / fs
    for i in match_idx:
        if i + n <= len(x):
            plt.axvspan(t[i], t[i] + D, color='tab:green', alpha=0.15)

    for (i, j) in early_pairs:
        plt.axvspan(t[i], t[j], hatch='///', edgecolor='k', facecolor='none', alpha=0.25)

    plt.title(title)
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.legend(loc="upper right")
    plt.tight_layout()


def plot_learned_patterns(W, match_idx, t, x, fs, D, scales, best_si, best_alpha,
                          delta_thresh, top_k=8):
    """
    Show what it 'learned':
      - pick top-K matches with smallest δ*,
      - plot their windows aligned to [0, D],
      - overlay learned template α* f_{s*} and its ±δ tube (in data coords per window).
    """
    n = int(round(D * fs))
    if len(match_idx) == 0:
        return

    # Build an array of (match_idx, rank_by_delta) — we don't have δ* per match here,
    # so we approximate by their order (already thresholded and NMS'd). For a precise
    # ranking, pass best_delta per window alongside match_idx and sort by it.
    # Here we'll just take the first K for simplicity.
    chosen = match_idx[:top_k]

    local_t = np.linspace(0, D, n, endpoint=False)

    plt.figure(figsize=(12, 6))
    ax = plt.gca()
    ax.set_title(f"Learned patterns at top-{len(chosen)} matches (aligned to [0, D])")
    ax.set_xlabel("Local time within window [s]")
    ax.set_ylabel("Amplitude")

    # Also collect mean of windows (zero-mean) for a quick visual template "average"
    mean_windows = []

    for i in chosen:
        if i + n > len(x):
            continue
        win = x[i:i+n]
        mu = win.mean()
        mean_windows.append(win - mu)

        # the learned scale s* and α* for this window:
        si = best_si[i]  # best scale index from the learning stage (indexed by window row i)
        s_star = scales[si]
        alpha_star = best_alpha[i]

        # rebuild f_{s*} of length n
        f_s = build_template(fs, D, base_amp=0.9, time_scale=s_star)
        f_c = f_s - f_s.mean()

        # Overlay: the data window (centered) and learned template (centered)
        ax.plot(local_t, win - mu, lw=0.8, alpha=0.25, label="window" if i == chosen[0] else None)
        ax.plot(local_t, alpha_star * f_c, lw=1.5, alpha=0.9, label="learned α*f_s" if i == chosen[0] else None)

        # Tube ±δ around template, drawn in data coords (centered)
        ax.fill_between(local_t,
                        alpha_star * f_c - delta_thresh,
                        alpha_star * f_c + delta_thresh,
                        alpha=0.15,
                        label="tube ±δ" if i == chosen[0] else None)

    if mean_windows:
        mean_curve = np.mean(np.vstack(mean_windows), axis=0)
        ax.plot(local_t, mean_curve, lw=2.0, alpha=0.9, linestyle='--',
                label="mean(window) over top-K")

    ax.legend(loc="upper right")
    plt.tight_layout()


# ---------------------------
# Main
# ---------------------------

def main():
    # Sampling & data
    fs = 500
    T = 10.0
    t, x, truth = make_signal(fs=fs, T=T, seed=7)

    # ETRE atom params
    D = 0.060            # seconds (window length)  ← duration guard
    coverage = 0.90      # robust coverage (fraction inside tube)
    delta_thresh = 0.18  # tube radius δ threshold for accepting a window
    fit_alpha = True     # learn α* per window

    # Learnable time-scales (small grid)
    scales = [0.9, 1.0, 1.1]   # s* is chosen from these per window
    base_amp = 0.9

    # Early pair gap guard
    gap_min = 0.04
    gap_max = 0.65

    # Build window matrix
    n = int(round(D * fs))
    W = window_matrix(x, n)          # shape (M, n) where M = len(x)-n+1

    # Learn best s* and α* per window, and get δ* per window for that s*
    # NOTE: For plotting and match thresholding we need δ* for each window.
    # We'll compute δ* for the best s* by recomputing for that template.
    best_delta, best_alpha, best_si, _ = learn_best_scale_and_alpha(
        W, fs, D, base_amp, scales, coverage=coverage, fit_alpha=fit_alpha
    )

    # Optional non-max suppression to reduce overlaps (radius ~ n/4)
    nms_radius = n // 4
    candidate_idx = nms_local_minima(best_delta, radius=nms_radius)

    # Threshold: keep windows whose minimal δ* ≤ delta_thresh
    cand_sorted = candidate_idx[np.argsort(best_delta[candidate_idx])]
    deltas_sorted = best_delta[cand_sorted]
    k = int(np.searchsorted(deltas_sorted, delta_thresh, side='right'))
    match_idx = cand_sorted[:k]  # these are window STARTS (in samples)

    # Early pairs on matched starts
    pairs = early_pairs_from_indices(match_idx, fs, gap_min, gap_max)

    # ---- PLOTS ----
    plot_time_series_with_matches(
        t, x, match_idx, n, fs, pairs,
        title=f"Time series with learned matches (D={D:.3f}s, δ≤{delta_thresh}, coverage≥{coverage:.2f})"
    )

    # Show what it learned at the top-K matches (aligned windows)
    top_k = min(8, len(match_idx)) if len(match_idx) else 0
    if top_k > 0:
        plot_learned_patterns(
            W, match_idx, t, x, fs, D, scales, best_si, best_alpha,
            delta_thresh=delta_thresh, top_k=top_k
        )

    # Console summary
    print(f"Matches: {len(match_idx)}   Early pairs: {len(pairs)}")
    print("First few match starts (idx → time):")
    for i in match_idx[:10]:
        print(f"  {i:6d} → {i/fs:7.3f}s")
    print("\nInjected spike centers (truth):", np.round(truth, 3))

    plt.show()


if __name__ == "__main__":
    main()
