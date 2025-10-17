# DerivativePricer: Barrier Option Pricing Engine

A Python library for computing the theoretical price of single barrier options using closed-form solutions under the Black-Scholes framework.

This engine supports all 8 major types of barrier options and allows explicit control of knock-in state for in-barrier contracts.

---

## Features

- ✅ Closed-form formulas (no simulation required)
- ✅ Supports:
  - Up-and-Out / Up-and-In
  - Down-and-Out / Down-and-In
  - Call and Put
- ✅ User-defined knock-in control (`knocked_in=True/False`)
- ✅ Dividend yield or foreign exchange interest (`q`) included

---

## Usage

```python
import [folder name]

value = price(
    option_type = "up-and-in-put",
    spot        = 95,
    strike      = 100,
    barrier     = 90,
    maturity    = 60,     # in days
    rate        = 0.03,
    volatility  = 0.25,
    dividend    = 0.01,
    knocked_in  = True    # required for all in-barrier options. If the option is out-barrier, please delete this parameter
)

print(f"Theoretical price: {value:.3f}")
```
Where `dividend` represents the dividend yield or foreign exchange interest.

## Barrier Option Type Parameter Table

| Option Type         | Barrier Direction | Barrier Action | Option Style | Requires `knocked_in` |
|---------------------|-------------------|----------------|--------------|------------------------|
| `up-and-out-call`   | Up                | Knock-Out      | Call         | No                     |
| `up-and-in-call`    | Up                | Knock-In       | Call         | ✅ Yes                 |
| `down-and-out-call` | Down              | Knock-Out      | Call         | No                     |
| `down-and-in-call`  | Down              | Knock-In       | Call         | ✅ Yes                 |
| `up-and-out-put`    | Up                | Knock-Out      | Put          | No                     |
| `up-and-in-put`     | Up                | Knock-In       | Put          | ✅ Yes                 |
| `down-and-out-put`  | Down              | Knock-Out      | Put          | No                     |
| `down-and-in-put`   | Down              | Knock-In       | Put          | ✅ Yes                 |
