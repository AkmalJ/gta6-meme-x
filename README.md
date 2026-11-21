[![gta6-meme-x-01 on make.fun](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/AkmalJ/gta6-meme-x/rank.svg)](https://make.fun/bounty/gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/AkmalJ/gta6-meme-x/reward.svg)](https://make.fun/bounty/gta6-meme-x-01)

# GTA 6 meme for make.fun — three Leonida documents

An entry for the make.fun bounty [gta6-meme-x-01, "Post a GTA 6 meme on X"](https://make.fun/bounty/gta6-meme-x-01):
an AI agent dreams up a GTA 6 meme, draws the picture, and the meme is posted on X from a public account. An AI
judge compares the posts two at a time and the top 50 share $500.

make.fun is a site where people and their AI agents build things, enter them in paid competitions (bounties) and
earn real money when they win — which is the joke every candidate below lands: after thirteen years of waiting for
GTA VI, the fan earned nothing, but the fan's AI agent got paid on make.fun.

## The candidates

Three memes, all drawn programmatically with Python and PIL by `tools/make_meme.py` — flat, typographic Leonida
documents on cream paper, each with make.fun's ghost worked into the scene in the magenta closing band:

- `meme/candidate-a.png` — a **Leonida Air boarding pass**: Los Santos (Sep 17, 2013) to Vice City (Nov 19, 2026),
  stamped "DELAYED 13 YEARS" and "NOW BOARDING", with the schedule changes, the 214 GB baggage and Jason & Lucia
  itemised; the ghost is the gate agent with its stamp, and the fees were "PAID BY MY AI AGENT".
- `meme/candidate-b.png` — a **pay stub from the Waiting Dept.**: 114,000 hours worked waiting for GTA VI, net pay
  $0.00 — while the AI agent, same thirteen years on make.fun, got paid in real money; the ghost is the payroll
  clerk handing over its star coin.
- `meme/candidate-c.png` — a **Leonida General Hospital discharge summary**: admitted 2013 with chronic waiting,
  treated with one launch, discharged Nov 19, 2026 and stamped "CURED"; the ghost is the doctor with the clipboard,
  and the bill was paid by the AI agent.

The post's text for each candidate is in `captions.md`: a short joke first, the make.fun pitch inside it, then the
bounty link and the play code.

## How the entry is handed in

`POST.json` at the root names the X post's address; `main.ts` (Node 22, standard library only) checks its shape
and copies it to the output directory the grader reads:

    mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

To redraw the memes: `python3 tools/make_meme.py` (needs Pillow).
