# AlgoBench

AlgoBench is a lightweight benchmarking and empirical Big-O complexity estimation CLI tool. It stress-tests algorithms with doubling input sizes to observe real-world runtime behavior and estimate asymptotic complexity without relying solely on static theoretical analysis.

## Methodology: The Doubling Hypothesis

AlgoBench uses the empirical doubling method to analyze asymptotic behavior:

1. **Worst-Case Synthesis:** Generates input data of size `N` designed to force complete traversal (e.g., strictly unique elements for duplicate-detection algorithms to prevent early returns).
2. **High-Resolution Timing:** Measures wall-clock execution time `T(N)` in milliseconds using `time.perf_counter()`.
3. **Growth Ratio Analysis:** Doubles the input size (`N -> 2N`) at each step and calculates the empirical growth ratio:

```text
Ratio = T(2N) / T(N)
```

The ratio maps directly to the complexity exponent: if `T(N) ~ N^k`, then `Ratio ≈ 2^k`, so `k = log2(Ratio)`.

| Expected Ratio | Exponent (k) | Empirical Big-O Estimate |
| :--- | :--- | :--- |
| ≈ 1.0x | 0 | O(1) or O(log N) |
| ≈ 2.0x | 1 | O(N) or O(N log N) |
| ≈ 4.0x | 2 | O(N²) |
| ≈ 8.0x | 3 | O(N³) |

## Current Benchmark Output (v0.1 - MVP)

```text
Function fast_fonk started.

N = 1000, Time: 0.049 ms | Baseline
N = 2000, Time: 0.125 ms | Ratio: 2.55x
N = 4000, Time: 0.191 ms | Ratio: 1.52x
N = 8000, Time: 0.692 ms | Ratio: 3.62x
N = 16000, Time: 0.970 ms | Ratio: 1.40x

>> Estimated Complexity: O(N) or O(N log N)

Function slow_fonk started.

N = 1000, Time: 21.560 ms | Baseline
N = 2000, Time: 88.457 ms | Ratio: 4.10x
N = 4000, Time: 360.184 ms | Ratio: 4.07x
N = 8000, Time: 1009.510 ms | Ratio: 2.80x
N = 16000, Time: 3975.127 ms | Ratio: 3.94x

>> Estimated Complexity: O(N^2)
```

> **Note on Measurement Noise:** The v0.1 MVP output above contains visible ratio fluctuations in both benchmarks.
> - `fast_fonk` (`2.55x`, `3.62x`): execution times under `1.0 ms` are highly sensitive to OS scheduler interrupts, CPU cache misses, and Python Garbage Collection.
> - `slow_fonk` (`2.80x` at `N = 8000`): even with second-scale runtimes, a single measurement per size is vulnerable to GC pauses, CPU frequency scaling, and background processes. Neighboring ratios (`4.07x`, `3.94x`) show the underlying O(N²) trend is intact.
>
> Because each size is currently measured only once, a single disturbed run skews the ratio. Addressing this noise is the primary focus of Phase 2 and Phase 3.

## Getting Started

### Prerequisites
* Python 3.10+

### Running Locally
```bash
python3 src/core_bench.py
```

## Architecture & Development Roadmap

- [x] **Phase 1: Core MVP Engine** — Doubling hypothesis runner, worst-case generator, and baseline ratio estimator.
- [ ] **Phase 2: Noise Reduction & Precision Timing** — CPU cache warmup runs, Garbage Collector (`gc`) isolation during measurement, and multi-run `min()` aggregation.
- [ ] **Phase 3: Statistical Curve Fitting (Log-Log OLS)** — Replacing single-step heuristics with Ordinary Least Squares linear regression on `log(N)` vs. `log(T)` to extract the complexity exponent `k` (the slope of the fitted line).
- [ ] **Phase 4: Multi-Language Subprocess Engine** — Automated compilation (`g++ -O2`) and execution pipeline to benchmark C++ implementations alongside Python.
- [ ] **Phase 5: CLI Interface & Reporting** — Command-line argument parsing (`argparse`) and formatted terminal tables.