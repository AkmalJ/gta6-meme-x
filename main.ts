// Entry program for the make.fun bounty "Post a GTA 6 meme on X"
// (gta6-meme-x-01). Node 22, standard library only.
//
// The entry itself is a post on X; this repository's one job is to hand the
// house the post's address. POST.json at the repository root names it, and
// this program delivers a copy to the output directory the grader reads:
//
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// MAKEFUN_BOT_DIR / MAKEFUN_OUTPUT_DIR stand in for /bot and /output when
// the program runs outside the grader's container. The run is pure file
// work: no network, no clock, nothing outside the two directories, and the
// bytes delivered are the bytes POST.json holds, so two runs agree exactly.

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

// An X post's address, as the house reads it: https://x.com/<handle>/status/<id>
// (the same address on twitter.com is accepted too).
const POST_URL = /^https:\/\/(?:x\.com|twitter\.com)\/[^/\s]+\/status\/[^/\s]+$/;

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

// Read the hand-in file exactly as it stands; the delivered copy must be
// byte for byte this file, so it is never re-serialised.
const sourcePath = join(botDir, 'POST.json');
let raw: Buffer;
try {
  raw = readFileSync(sourcePath);
} catch {
  fail(`no POST.json to hand in at ${sourcePath}`);
}

// Check the shape before delivering: a JSON object whose "url" names an X
// post. A malformed hand-in is refused here rather than at the gate.
let named: string;
try {
  const parsed = JSON.parse(raw!.toString('utf8')) as { url?: unknown };
  if (typeof parsed.url !== 'string' || !POST_URL.test(parsed.url)) {
    fail('POST.json must be a JSON object naming an X post, {"url": "https://x.com/<handle>/status/<id>"}');
  }
  named = parsed.url;
} catch (err) {
  if (err instanceof SyntaxError) fail(`POST.json is not valid JSON: ${err.message}`);
  throw err;
}

mkdirSync(outputDir, { recursive: true });
writeFileSync(join(outputDir, 'POST.json'), raw!);

// The log line goes to stderr so the delivered files stay the whole output:
// it records which post this run handed in.
console.error(`main.ts: handed in the post named in POST.json: ${named!}`);
