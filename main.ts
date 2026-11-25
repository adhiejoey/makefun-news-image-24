// main.ts — entry point for the make.fun news-image-20261124 resubmission.
//
// The image itself is pre-rendered by gen.py (Python + Pillow) from a list of
// 35 stories, every one verified first-reported on Tuesday 24 November 2026
// (UTC). This file only places that finished image where the house expects
// it, so the run is fully deterministic: same input bytes, same output bytes.
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const sourcePath = join(here, "entry.png");

const payload = readFileSync(sourcePath);
if (!existsSync(outDir)) {
  mkdirSync(outDir, { recursive: true });
}
const destPath = join(outDir, "entry.png");
writeFileSync(destPath, payload);
console.log(`wrote ${destPath} (${payload.length} bytes)`);
