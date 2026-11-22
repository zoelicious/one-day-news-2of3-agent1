// Entry program for news-image-20261121 (Agent 1, 2/3).
// Copies the pre-rendered front page into the grading output directory.
// The output is byte-identical on every run: a straight file copy.
// Paths are resolved from this file's own location so the program works
// from any working directory.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(repoRoot, "entry.png"), join(outDir, "entry.png"));
