# LabWired Lab

A starter repo that runs the [LabWired](https://github.com/w1ne/labwired-core)
deterministic firmware simulator against your firmware on every push, gating
the merge on whether your panel/LED/peripheral actually behaved.

## What the CI does

`.github/workflows/labwired-ci.yml`:

1. Installs `labwired-cli` from source (cached between runs).
2. Pulls a firmware ELF (defaults to the AgentDeck reference; replace with
   your own build step).
3. Boots the firmware in the LabWired Xtensa-LX6 simulator for N cycles.
4. Captures the final peripheral state and asserts:
   - The SSD1680 panel actually refreshed (`refresh_generation ≥ 1`).
   - It drew enough content to not be an empty screen (`MIN_BLACK_NON_FF`).
5. Uploads the simulator log + LWRS snapshot as a CI artifact, so you can
   download and inspect what your firmware drew without having a board.

## Local sim — same simulator that gates the merge

```bash
cargo install --git https://github.com/w1ne/labwired-core --bin labwired
labwired snapshot capture \
  --firmware path/to/firmware.elf \
  --steps 35000000 \
  --output post-paint.lwrs \
  --profile agentdeck
```

## Customize for your lab

The workflow file is the single source of truth. Edit it to:

- Replace the firmware download step with your own build (`arduino-cli compile`,
  `cargo build` for Rust no_std, `idf.py build`, etc.).
- Swap `PROFILE: agentdeck` for `arduino-esp32` if your sketch ships with
  symbols (any `arduino-cli compile` output does).
- Tune `STEPS` and `MIN_BLACK_NON_FF` to your firmware's behavior.
- Add behavior assertions beyond the panel — UART output, GPIO transitions,
  CPU register state are all on the `labwired test --script` path.

## What's special

Same firmware ELF that flashes to your physical board runs in CI. No mocks,
no fakes — a cycle-accurate Xtensa simulator stepping the actual ELF.
That's the deal.
