// Entry program for news-image-20261124 (Node 22, standard library only).
//
// The image this entry submits is entry.png, drawn for Tuesday 24 November
// 2026 and shipped beside this file. This program reads those bytes and
// writes them to <output>/entry.png, creating the output directory first.
// It takes no input, reaches for no network and writes the same bytes on
// every run, so the grader's two runs agree.
//
// Run it locally the way the grader does:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const source = fileURLToPath(new URL("./entry.png", import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(outDir, "entry.png");

mkdirSync(dirname(target), { recursive: true });
const bytes = readFileSync(source);
writeFileSync(target, bytes);

// Read back what was written: the grader runs this program twice and the
// two runs must agree, so a short write would fail loudly here instead.
if (readFileSync(target).length !== bytes.length) {
  throw new Error("entry.png was not written in full");
}
