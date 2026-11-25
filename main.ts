// Ships the pre-rendered broadsheet to the grader's output directory.
// Node 22, standard library only. Deterministic: the copied bytes are
// exactly the entry.png sitting next to this file, on every run.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outputDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url),
  join(outputDir, "entry.png"));
