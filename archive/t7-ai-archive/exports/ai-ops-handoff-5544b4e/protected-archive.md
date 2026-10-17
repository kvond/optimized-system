# Protected raw-export storage

The T7 archive is verified for sanitized preservation. It is ExFAT with encryption unverified; the Mac's FileVault is off. Existing preserved source files stay intact. Raw private account histories await a recoverable encrypted container.

Use a new encrypted disk image within `/Volumes/T7/AI-Archive`, without formatting the drive. Intended image: `AI-Private-Archive.sparsebundle`, mounted as `AI-Private-Archive`, APFS, AES256, logical maximum20GB. A sparse bundle grows with stored data.

October12 UI attempt: Disk Utility's new-image fields were verified as the existing T7 AI-Archive folder, APFS, GUID partition map, Sparse Bundle Image (UDSB), 256-bit AES and20GB. Save started a Creating disk image dialog, but no password-entry or completion result was exposed. A partial bundle exists at the intended path with zero logical size and no bands; `hdiutil isencrypted` returns NO. No password was entered by the agent. Treat this as incomplete and unprotected. Preserve and reconcile this operation before retrying; do not overwrite the path, assume encryption, mount it for private work or download raw histories into it.

Katherine must enter and retain the new archive password privately in macOS. Do not put it in a chat, tool argument, environment variable, GitHub, manifest or report. Apple warns that losing the password makes the contents inaccessible. [Apple's disk-image guide](https://support.apple.com/en-ie/guide/disk-utility/dskutl11888/mac) documents encrypted images and password entry. The installed `hdiutil` manual documents APFS, SPARSEBUNDLE, AES256, and interactive passphrase handling; do not pass a password on the command line.

After creation, verify image encryption, unlock/mount it through normal macOS handling, and record its actual backing image and mount path. Confirm a synthetic file can be copied back with identical SHA256 and private POSIX permissions. That check establishes encrypted-container configuration plus file-copy behavior; it is not an export receipt.

Only then acquire provider exports directly into the verified protected destination. Prefer a download destination inside the mounted image; do not stage raw histories in the unprotected T7 root or internal Downloads folder. Preserve export files without expanding them by default. Record platform, exact account email, export date, covered date range or null, size, SHA256, privacy classification and source/destination readback. Keep private filenames and raw manifests inside protected storage, outside Git.

Both Claude ready emails are dated October12. The links expire; obtain a fresh link only after reconciling whether the original was already downloaded. UD ChatGPT's export request remains unconfirmed at UD authentication and must not be blindly repeated. Eject the encrypted image when work is finished; an unlocked mounted image remains accessible to the logged-in user.
