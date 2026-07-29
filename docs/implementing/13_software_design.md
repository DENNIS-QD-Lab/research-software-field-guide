# Software design: keeping code clean and easy to follow

There is one goal behind everything in this doc: **keep the code easy to follow.** When a script grows into a tangle you feel the cost directly. To change one line you have to hold the whole file in your head, and every edit risks breaking something three functions away. Good design is what keeps code clean and clear as it grows.

This doc is about design *within* a codebase, at the level of functions and modules. Organizing the repository as a whole is a separate topic, covered later (`15_experiments_and_shipping.md`).

## Decomposition: one function, one job

The most useful move you can make is to split a function that does several things into small functions that each do one. Your project's coding-standards file (here, `../../CLAUDE.md`) states the rule ("keep functions short; if a function is doing more than one thing, split it"). Here is why it matters, concretely. This function does four jobs at once:

```python
def process_spectrum(path):
    data = np.loadtxt(path)
    wavelengths = data[:, 0]
    intensities = data[:, 1]
    intensities = intensities / intensities.max()
    peak_index = 0
    best = intensities[0]
    for i in range(len(intensities)):
        if intensities[i] > best:
            best = intensities[i]
            peak_index = i
    with open(path.replace(".txt", "_peak.txt"), "w") as f:
        f.write(f"{wavelengths[peak_index]}\n")
    return wavelengths[peak_index]
```

It reads a file, normalizes, finds a peak, and writes a result. You cannot reuse the normalization without also writing a file, you cannot test the peak-finding without a file on disk, and to follow any one step you have to read all of them. Split it so each piece does one thing:

```python
def load_spectrum(path: str) -> tuple[np.ndarray, np.ndarray]:
    """Read a two-column spectrum file into (wavelengths, intensities)."""
    data = np.loadtxt(path)
    return data[:, 0], data[:, 1]


def normalize(intensities: np.ndarray) -> np.ndarray:
    """Scale intensities so the largest is 1.0."""
    return intensities / intensities.max()


def peak_wavelength(wavelengths: np.ndarray, intensities: np.ndarray) -> float:
    """Return the wavelength at the maximum intensity."""
    return float(wavelengths[np.argmax(intensities)])
```

Then a thin function orchestrates them, and it reads like a summary of what happens:

```python
def report_peak(spectrum_path: str, output_path: str) -> float:
    wavelengths, intensities = load_spectrum(spectrum_path)
    peak = peak_wavelength(wavelengths, normalize(intensities))
    _save_value(peak, output_path)
    return peak
```

Every piece is now clear on its own, `normalize` and `peak_wavelength` are pure functions you can test without touching the disk (`12_testing_with_pytest.md`), and the hand-written max loop collapsed into `np.argmax` along the way. This is not busywork: it is what makes the code changeable later.

## Cohesion and single responsibility

Two words name the idea. **Cohesion** is how much the parts of a function or module belong together. **Single responsibility** is the target: each function does one job, each module covers one area. A quick smell test is the word "and." If describing a function honestly needs an "and" ("it loads the data *and* normalizes it *and* saves it"), it is doing too much. Small single-purpose functions are the ideal: a function that takes a couple of inputs and returns a single number, with no side effects, is trivial to unit-test. In the SWIR_HDR exemplar the weighting functions (one small step of the imaging math) are exactly this shape — each takes a pixel value and a range and returns one weight, nothing else — which is why they were straightforward to test.

## When a function, when a module, when a class

- **A function** is the default unit. Reach for one whenever you can name a job.
- **A module** (a `.py` file) groups related functions, such as all the radiance math in one file. Name it for what it contains, a noun phrase like `ratio_analysis.py` (`../../CLAUDE.md`).
- **A class** earns its keep only when data and the behavior that acts on it genuinely travel together, or when you need several independent instances each carrying their own state. Most research code does not need classes; functions and modules cover the large majority of cases. Reach for a class when passing the same cluster of values into function after function starts to feel awkward, not before.

## Two tools you will grow into

These are pointers, not lessons. Learn them when you hit the situation they solve.

- **Dataclasses** group related values that always travel together into one named object. If you find yourself passing the same cluster of calibration values (say `gain, offset, dark_level, exposure_times`) into function after function, a small `@dataclass` holding them turns four arguments into one and gives the bundle a name. That is the moment to look them up.
- **Abstract base classes** define a shared interface that several variants must all provide, so the rest of the code can treat them interchangeably. If you have multiple data sources, or multiple interchangeable methods that must expose the same call, an ABC pins down the shape they share. One paragraph is all it deserves here; do not turn a two-source problem into a class hierarchy.

## Design and tests reinforce each other

The two habits feed each other. Decomposing code into small, single-purpose functions is what makes it testable, and having tests is what gives you the confidence to decompose without fear of silently changing a result. That loop, refactor freely because the tests will catch a mistake, is the practical payoff of both docs together. When you later restructure a package into a library plus experiments (`15_experiments_and_shipping.md`), the tests from `12_testing_with_pytest.md` are exactly what prove the restructure changed the shape without changing the behavior.
