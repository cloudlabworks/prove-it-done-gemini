# prove-it-done-gemini

Receipt-gated completion for [Gemini CLI](https://github.com/google-gemini/gemini-cli).
Before the agent tells you work is done, fixed, deployed or live, it lists each claim,
writes one re-runnable receipt per claim, and runs a bundled verifier against the real
system. Only steps the verifier reports as PROVEN get called done.

This is a Gemini CLI packaging of the
[`prove-it-done`](https://github.com/issaquahd/prove-it-done) skill. **The skill repo is
the source of truth**: `skills/prove-it-done/` here is a copy, kept in sync with it. Report
skill behaviour issues there; report packaging issues (manifest, command, context file) here.

## Install

```
gemini extensions install https://github.com/cloudlabworks/prove-it-done-gemini
```

Requires Python 3.9 or later for the verifier (standard library only, no packages). On
Windows, use `py -3` or `python` where this says `python3`; for example:

```
py -3 skills/prove-it-done/scripts/verify_receipts.py --help
```

## What's in it

| Path | What it does |
|---|---|
| `gemini-extension.json` | Extension manifest (`prove-it-done-gemini`). |
| `GEMINI.md` | Context file: activate the skill before saying "done". |
| `commands/prove/check.toml` | The `/prove:check` command. |
| `skills/prove-it-done/` | The skill, its verifier (`scripts/verify_receipts.py`), references and examples. |

## `/prove:check`

Run it after a piece of work, optionally with a note about what to cover:

```
/prove:check the staging deploy and the config change
```

It activates the `prove-it-done` skill for the work just completed in the session. The agent
lists every claim it made, writes a receipt for each (a command to re-run and what the
output must show), runs the verifier after the last change, and finishes with only what
the verifier reports as PROVEN. Anything unproven is named as not done, with the reason.

Rules the skill enforces:

- A tool's "ok" or a worker's "done" is a claim, not evidence.
- A check that errors (timeout, 401, command not found) proves nothing.
- A receipt that already passes before the change is not evidence. With `| baseline=HEAD`
  the verifier re-runs a code receipt against the pre-change tree and marks it VACUOUS if it
  passes there too; `--require-baseline` makes that a failure.
- "Done" is said only for PROVEN steps.

## Keeping the copy in sync

The bundled skill is checked against the upstream repository with:

```bash
python3 scripts/check_skill_sync.py ../prove-it-done
```

It prints one line per difference and exits 1 if the copy has drifted (2 on a usage error).

## Notes

- No MCP server and no shell hooks: the command is prompt-only, and the verifier is run by the skill.
- `/prove:check` has been parse-checked and the extension validated with
  `gemini extensions validate`; the command's behaviour with a live model has not been tested yet.

## Maintainer

Cloud Lab Works. Licence: MIT (see `LICENSE`; the bundled skill carries its own copy of the
licence in `skills/prove-it-done/LICENSE`).
