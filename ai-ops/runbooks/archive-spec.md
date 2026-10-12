# AI Archive specification

Current checkpoint, October12: terminal reads and writes to T7 now succeed. Ten original checksum entries match, and eight sanitized handoff files were copied to `exports/ai-ops-handoff-a5f5acc` with direct source/destination SHA256 readback. This supersedes the historical CLI-access limitations below. Both Claude account exports are now ready by provider email, but no new raw account export is downloaded. T7 encryption remains unverified, FileVault is off, and an encrypted container is needed for raw histories. See [protected archive setup](protected-archive.md).

Intended stable root /Volumes/T7/AI-Archive. raw/chatgpt/{kvond12,ud}, raw/claude/{kvond12,ud}, raw/perplexity, raw/other, manifests, exports, checksums, preservation/repos.

For each item record source_platform, account, export_date, source_date_range, source_path, file_path, size_bytes, sha256, privacy_class, extraction_status, notes. Unknown fields null. Copy only; SHA256 verify source and destination; preserve originals.

Mounted T7 with ~829GB free, external USB ExFAT; encryption unverified. Initial mkdir stalled locally; cancelled task-owned command. Desktop Commander create_directory timed out; readback pending. No sensitive raw copy is authorized to an unverified destination by this run. If write remains blocked, this specification is the delivered archive foundation; no huge internal export.


Update: Finder created AI-Archive and copied the six prepared top-level entries. Finder destination listing verifies paths and sizes; CLI reads/hashing time out. Copy is visually present, checksum readback remains BLOCKED; do not delete originals or claim a checksum-verified external copy. Original prepared files remain under outputs/archive-contents with source checksums and three locally verified Git bundles (~2.8MB total).


Final verification: Finder copy-back from external AI-Archive to local outputs/archive-readback completed. All 11 prepared files (including SHA256SUMS) matched SHA256 on readback. Three Git bundles remain locally bundle-verified. This verifies the copied files via Finder readback despite command-line volume access timeout. No complete AI account exports obtained. Encryption remains unverified.
