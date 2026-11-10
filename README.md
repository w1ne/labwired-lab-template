# LabWired Lab

A small firmware repository with a working simulation test. It includes firmware
source, a prebuilt ELF, a board manifest, and two behavior assertions. A second
test deliberately expects the wrong UART text so CI also checks that the gate
can fail.

## Run locally

Install the released CLI, then run the same tests as CI:

```sh
curl -fsSL https://labwired.com/install.sh | LABWIRED_VERSION=v0.25.0 sh
python3 scripts/check-gate.py
```

The positive test must pass both assertions and return exit code 0. The negative
control must fail its UART assertion and return exit code 1. Results, UART logs,
and JUnit XML are written under `out/positive` and `out/negative`.

No firmware compiler is needed to run the committed ELF. Python 3 and the
`labwired` executable must be on `PATH`; set `LABWIRED_CLI` to use another binary.

## What is simulated

`firmware/demo.elf` is the program in `firmware/src/main.c`. It sends a greeting
through a generic memory-mapped UART and then loops. The manifest describes a
generic ARM Cortex-M target. This fixture checks the simulation and CI path;
it does not establish timing or peripheral compatibility with a specific board.

To rebuild the ELF, install `arm-none-eabi-gcc` and run `make -C firmware`.
Commit the rebuilt ELF when the source changes, or add the build to your workflow.

## Use your firmware

1. Replace `firmware/demo.elf` with your compiled ELF.
2. Update `firmware/system.yaml` and its chip descriptor for your hardware.
3. Update `tests/firmware-regression.yaml` with the behavior you expect.
4. Run `python3 scripts/check-gate.py`. Keep at least one `uart_contains`
   assertion so the negative control can confirm a failed assertion is rejected.

The workflow runs on every branch, including the repository's `master` default.
This repository uses a self-hosted Linux X64 runner. If you generate a copy and
use GitHub-hosted runners, change `runs-on` to `ubuntu-latest`. Fork pull requests
are not executed on this repository's self-hosted runners.

## Make the test a required merge check

Run the workflow once. In the rule for your default branch, enable
**Require status checks to pass before merging** and select `simulator-gate`.
Copying a template or adding a workflow does not create that rule automatically.

For richer hardware examples, use the current
[LabWired examples](https://github.com/w1ne/labwired-core/tree/main/examples).
Each example defines its own firmware, manifest, and supported behavior.
