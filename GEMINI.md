# prove-it-done-gemini

Before you tell the user that work is done, fixed, deployed, live, or that a
sub-agent or tool succeeded, activate the `prove-it-done` skill. It has you list
each claim, write one re-runnable receipt per claim, run the bundled verifier
after your last change, and report only what passed.

- A tool's "ok" or a worker's "done" is a claim, not evidence. Record it, then
  check the system yourself.
- A check that errors (timeout, 401, command not found) proves nothing.
- Say "done" only for steps the verifier reports as PROVEN. Name every other
  step as not done, and why.

The verifier needs Python 3.9 or later: `python3 scripts/verify_receipts.py --help`
(path relative to the skill directory).
On Windows, use `py -3` or `python` where this says `python3`.
