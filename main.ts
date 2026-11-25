// Publisher for the make.fun entry: drops the bundled entry.png into the
// output directory the grader points at, defaulting to /output.
import * as fs from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

// The picture lives next to this file, wherever this file is run from.
const folderHere = dirname(fileURLToPath(import.meta.url));
const picturePath = resolve(folderHere, "entry.png");

// The grader's directory: env var first, /output when it is not set.
const destinationFolder = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const destinationPath = resolve(destinationFolder, "entry.png");

// Create the folder if it is missing, then place the picture inside it.
fs.mkdirSync(destinationFolder, { recursive: true });
fs.cpSync(picturePath, destinationPath);
