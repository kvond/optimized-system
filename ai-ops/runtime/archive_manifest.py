"""Private, bounded archive receipts. Never persist generated manifests in Git."""
import hashlib
import json
import os
from pathlib import Path
import stat


def _identity(path):
    s = path.lstat()
    if not stat.S_ISREG(s.st_mode):
        raise ValueError('Only regular files allowed; symlinks rejected')
    return (s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns, s.st_ctime_ns)


def _safe_path(path):
    path = Path(os.path.abspath(path))
    for part in (path, *path.parents):
        if part.is_symlink():
            raise ValueError('Symlink path rejected')
    return path


def checksum(path, max_bytes=100_000_000):
    path = _safe_path(path)
    before = _identity(path)
    if before[2] > max_bytes:
        raise ValueError('Byte limit exceeded')
    digest = hashlib.sha256()
    total = 0
    with path.open('rb') as stream:
        while True:
            block = stream.read(min(1024 * 1024, max_bytes - total + 1))
            if not block:
                break
            total += len(block)
            if total > max_bytes:
                raise ValueError('Byte limit exceeded')
            digest.update(block)
    if _identity(path) != before:
        raise ValueError('Source mutated during checksum')
    return {'size_bytes': total, 'sha256': digest.hexdigest()}


def inventory(root, *, platform=None, account=None, date_range=None,
              max_files=1000, max_bytes=100_000_000):
    if max_files < 1 or max_bytes < 0:
        raise ValueError('Invalid bounds')
    root = _safe_path(root)
    if not root.is_dir():
        raise ValueError('Inventory root must be a directory')
    paths = []
    for directory, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            _safe_path(Path(directory) / name)
        dirs.sort()
        for name in sorted(files):
            paths.append(Path(directory) / name)
            if len(paths) > max_files:
                raise ValueError('File limit exceeded')
    result = []; total = 0
    for path in sorted(paths):
        receipt = checksum(path, max_bytes=max_bytes-total)
        total += receipt['size_bytes']
        result.append({'path': str(path.relative_to(root)), **receipt})
    return {'schema_version': 1, 'platform': platform, 'account': account,
            'date_range': date_range, 'metadata_status': 'explicit_or_unknown',
            'privacy': {'classification': 'unknown', 'contains_student_data': 'unknown',
                        'contains_secrets': 'unknown', 'manifest_destination': 'private_local_only'},
            'files': result, 'total_bytes': total}


def verified_copy(source, destination, *, max_bytes=100_000_000):
    source = _safe_path(source); destination = _safe_path(destination)
    before = _identity(source)
    if before[2] > max_bytes:
        raise ValueError('Byte limit exceeded')
    digest = hashlib.sha256(); total = 0; created = False
    try:
        fd = os.open(str(destination), os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
        created = True
        with os.fdopen(fd, 'wb') as output:
            if stat.S_IMODE(os.fstat(output.fileno()).st_mode) != 0o600:
                raise ValueError('Filesystem does not support required private mode 0600')
            with source.open('rb') as stream:
                while True:
                    block = stream.read(min(1024 * 1024, max_bytes-total+1))
                    if not block: break
                    total += len(block)
                    if total > max_bytes: raise ValueError('Byte limit exceeded')
                    digest.update(block); output.write(block)
            output.flush(); os.fsync(output.fileno())
        if _identity(source) != before:
            raise ValueError('Source mutated during copy')
        receipt = checksum(destination, max_bytes=max_bytes)
        if receipt['sha256'] != digest.hexdigest():
            raise ValueError('Destination verification failed')
        if stat.S_IMODE(destination.lstat().st_mode) != 0o600:
            raise ValueError('Destination private mode changed')
        return {'status': 'verified', 'permission_mode': '0600', 'encryption': 'unknown', **receipt}
    except BaseException:
        if created: destination.unlink(missing_ok=True)
        raise


def inspect_export_fixture(path, *, platform, account=None, date_range=None,
                           max_bytes=10_000_000, max_conversations=10000):
    """Inspect explicitly designated synthetic fixtures only; return no message data."""
    if platform not in ('chatgpt', 'claude'):
        raise ValueError('Explicit supported platform required')
    path = _safe_path(path)
    if path.name != 'conversations.json':
        raise ValueError('Expected conversations.json')
    before = _identity(path)
    if before[2] > max_bytes: raise ValueError('Fixture byte limit exceeded')
    with path.open('rb') as stream:
        opened = os.fstat(stream.fileno())
        if (opened.st_dev, opened.st_ino, opened.st_size, opened.st_mtime_ns, opened.st_ctime_ns) != before:
            raise ValueError('Fixture replaced before read')
        raw = stream.read(max_bytes + 1)
    if len(raw) > max_bytes: raise ValueError('Fixture byte limit exceeded')
    receipt = {'size_bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
    data = json.loads(raw)
    if _identity(path) != before: raise ValueError('Fixture mutated')
    if not isinstance(data, list) or len(data) > max_conversations:
        raise ValueError('Invalid or oversized conversation list')
    key = 'mapping' if platform == 'chatgpt' else 'chat_messages'
    if any(not isinstance(row, dict) or key not in row or
           not isinstance(row[key], dict if platform == 'chatgpt' else list)
           for row in data):
        raise ValueError('Platform structure mismatch')
    return {'platform': platform, 'account': account, 'date_range': date_range,
            'conversation_count': len(data), 'structure': key,
            'privacy': 'unknown', **receipt}


def manifest_json(manifest):
    return json.dumps(manifest, sort_keys=True, indent=2, ensure_ascii=True) + '\n'
