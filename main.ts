// news-image-20261123 — "Sum up 23 November's world news in one image".
//
// The entry is a single original front page (entry.png, 1024x1024) drawn by
// draw.py for this bounty: six panels for the six biggest stories of Monday
// 23 November 2026 — COP31 ending with no deal in Antalya, Ukraine sinking
// the Russian corvette Merkury at Benghazi, Nvidia bringing back Jensen
// Huang as CEO, the AI sell-off hitting Asian markets, a Russian strike
// killing 11 in Dymer, and Israeli coalition talks collapsing.
//
// The grader runs this program with no network. It copies entry.png into the
// output directory it names, then checks the copy twice: first by comparing
// the SHA-256 digest of what it wrote against the source, then by reading
// the PNG header so the size it reports comes from the file itself. Either
// mismatch fails loudly instead of leaving a bad artifact behind, so the
// two graded runs always write identical bytes.
//
// Local run:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { createHash } from "node:crypto";
import { copyFileSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

const SOURCE = new URL("./entry.png", import.meta.url);
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const DEST = join(OUT_DIR, "entry.png");

function sha256(buf: Buffer): string {
  return createHash("sha256").update(buf).digest("hex");
}

// PNG dimensions live in the IHDR chunk: width at bytes 16-19, height at
// 20-23, both big-endian. The 8-byte signature is checked first so a file
// that is not a PNG at all is caught here, not by the judge.
// The gate's caps for this bounty (RULES.txt): a whole PNG or JPEG of at
// most 1 MiB and at most 1024 by 1024 pixels. Check them here so a bad
// image fails loudly at build time instead of being refused by the gate.
const MAX_BYTES = 1048576;
const MAX_SIDE = 1024;

function pngSize(buf: Buffer): { width: number; height: number } {
  const signature = Buffer.from([
    0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
  ]);
  if (buf.length < 24 || !buf.subarray(0, 8).equals(signature)) {
    throw new Error("entry.png is not a PNG file");
  }
  if (buf.toString("ascii", 12, 16) !== "IHDR") {
    throw new Error("entry.png has no IHDR chunk where one belongs");
  }
  return { width: buf.readUInt32BE(16), height: buf.readUInt32BE(20) };
}

mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SOURCE, DEST);

const original = readFileSync(SOURCE);
const written = readFileSync(DEST);
if (original.length !== written.length || sha256(original) !== sha256(written)) {
  throw new Error(
    `copy mismatch: source ${original.length} bytes sha256 ${sha256(original)}, ` +
      `output ${written.length} bytes sha256 ${sha256(written)}`,
  );
}

const { width, height } = pngSize(written);
const bytes = statSync(DEST).size;
if (bytes > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes} bytes, over the 1 MiB cap`);
}
if (width > MAX_SIDE || height > MAX_SIDE) {
  throw new Error(`entry.png is ${width}x${height}, over the 1024x1024 cap`);
}
console.log(
  `entry.png -> ${DEST}: ${width}x${height} PNG, ${bytes} bytes, ` +
    `sha256 ${sha256(written)} — copy verified.`,
);
