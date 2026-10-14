"""Resolve and initialize private working state on a verified mounted encrypted image.

No provider calls, authentication, mount changes, permission grants, or school jobs.
OwnersEnabled is not a gate; actual directory/file privacy is checked separately.
"""
from __future__ import annotations
import argparse, datetime as dt, json, os, plistlib, re, sqlite3, stat, subprocess
from dataclasses import dataclass
from pathlib import Path

DEFAULT_MOUNT=Path('/Volumes/AI-Private-Archive')
DEFAULT_IMAGE=Path('/Volumes/T7/AI-Archive/AI-Private-Archive-v2.sparsebundle')
RELATIVE_STATE=Path('AI-Archive/state/ai-ops')

class StorageError(RuntimeError):pass

def _command(argv):
    completed=subprocess.run(argv,capture_output=True,timeout=10,check=False)
    if completed.returncode:raise StorageError('storage metadata probe failed: '+argv[0])
    return completed.stdout

def verified_mount(mount: Path,image: Path) -> dict:
    """Metadata-only probes; no password prompts or image/source payload reads."""
    if not os.path.ismount(mount) or not image.is_dir():raise StorageError('expected mount/image missing; no writes')
    # Require the backing image's external /Volumes disk to be mounted too.
    if len(image.parts)<4 or image.parts[:2]!=('/', 'Volumes') or not os.path.ismount(Path(*image.parts[:3])):
        raise StorageError('external backing disk is not mounted; no writes')
    disk=plistlib.loads(_command(['diskutil','info','-plist',str(mount)]))
    if disk.get('MountPoint')!=str(mount) or str(disk.get('FilesystemType','')).lower()!='apfs':raise StorageError('expected APFS mount not verified')
    images=plistlib.loads(_command(['hdiutil','info','-plist'])).get('images',[])
    matched=[i for i in images if any(s.get('mount-point')==str(mount) for s in i.get('system-entities',[]))]
    if len(matched)!=1 or Path(matched[0].get('image-path','')).resolve()!=image.resolve():raise StorageError('mount does not match intended encrypted backing image')
    # The mounted image's fresh authoritative metadata avoids reopening an
    # attached sparsebundle (isencrypted can fail with Resource temporarily
    # unavailable). Never accept a truthy string/integer or override false.
    if 'image-encrypted' in matched[0]:
        if matched[0]['image-encrypted'] is not True:
            raise StorageError('backing-image encryption unverified; no writes')
    else:
        encryption=_command(['hdiutil','isencrypted',str(image)]).decode(errors='replace')
        if not re.search(r'^encrypted:\s*YES\s*$',encryption,re.M):raise StorageError('backing-image encryption unverified; no writes')
    return {'mount':str(mount),'backing_image':str(image),'filesystem':'apfs','encryption_verified':True,'mount_verified':True}

@dataclass(frozen=True)
class RuntimePaths:
    root: Path
    cache: Path
    usage: Path
    receipts: Path
    proof: dict
    probe: object = verified_mount
    def report(self):
        return {'root':str(self.root),'cache_database':str(self.cache),'usage_database':str(self.usage),
                'receipts_directory':str(self.receipts),'verification':self.proof,'ownership_enforcement_required':False}

def _no_symlinks(path: Path):
    for item in [path,*path.parents]:
        if item.is_symlink():raise StorageError('symlink storage paths are forbidden')

def _private_directory(path: Path):
    if not path.is_dir() or path.is_symlink():raise StorageError('private directory missing or replaced')
    mode=path.stat().st_mode
    if mode & 0o077:raise StorageError('existing directory is not private; preserve it for review')

def resolve_storage(root=None,*,mount=None,image=None,initialize=False,probe=verified_mount,environ=None) -> RuntimePaths:
    """Fail closed before writing. CLI flags override environment; no internal fallback."""
    env=os.environ if environ is None else environ
    mount=Path(mount or env.get('AI_OPS_ARCHIVE_MOUNT') or DEFAULT_MOUNT)
    image=Path(image or env.get('AI_OPS_BACKING_IMAGE') or DEFAULT_IMAGE)
    root=Path(root or env.get('AI_OPS_STORAGE_ROOT') or mount/RELATIVE_STATE)
    if any('..' in p.parts for p in (root,mount,image)):raise StorageError('parent traversal storage paths forbidden')
    if not all(p.is_absolute() for p in (root,mount,image)):raise StorageError('absolute storage paths required')
    for p in (root,mount,image):_no_symlinks(p)
    if root==mount or mount not in root.parents:raise StorageError('working state must remain inside the verified archive mount')
    proof=probe(mount,image)
    if proof.get('encryption_verified') is not True or proof.get('mount_verified') is not True or proof.get('filesystem')!='apfs':raise StorageError('mount/encryption evidence incomplete; no writes')
    # Preflight every existing descendant before any mkdir; do not chmod old data.
    chain=[];p=mount
    for part in root.relative_to(mount).parts:
        p=p/part;chain.append(p)
        if p.exists():_private_directory(p)
    for name in ('cache.sqlite','usage.sqlite','runtime-storage.json'):
        p=root/name
        if p.is_symlink():raise StorageError('symlink state file rejected')
        if p.exists() and (not p.is_file() or p.stat().st_mode&0o077):raise StorageError('existing state file is not private; preserve for review')
    receipts=root/'receipts'
    if receipts.exists():_private_directory(receipts)
    if initialize:
        # Metadata is rechecked immediately before setup. External ejection races
        # still require operator/OS supervision; no unverified fallback is allowed.
        proof=probe(mount,image)
        if proof.get('mount_verified') is not True or proof.get('encryption_verified') is not True or proof.get('filesystem')!='apfs':raise StorageError('verification changed; no writes')
        for p in [*chain,receipts]:
            try:p.mkdir(mode=0o700)
            except FileExistsError:pass
            _private_directory(p)
    elif not root.is_dir():raise StorageError('state directory not initialized')
    paths=RuntimePaths(root,root/'cache.sqlite',root/'usage.sqlite',receipts,proof,probe)
    return paths

def initialize_state(paths: RuntimePaths):
    """Initialize existing reusable local stores without enabling paid routes."""
    resolve_storage(paths.root,mount=paths.proof['mount'],image=paths.proof['backing_image'],probe=paths.probe,initialize=False,environ={})
    from foundation import Store
    from usage import UsageLedger
    Store(paths.cache);UsageLedger(paths.usage,business_timezone='America/New_York')
    for path in (paths.cache,paths.usage):
        if path.stat().st_mode&0o077:raise StorageError('database permissions not private')
        with sqlite3.connect(path) as db:
            if db.execute('PRAGMA quick_check').fetchone()[0]!='ok':raise StorageError('database integrity check failed')
    config={'schema_version':1,'privacy':'private runtime state; never commit databases/receipts','paths':paths.report(),
            'paid_routes_enabled':False,'cloud_service_claim':False}
    destination=paths.root/'runtime-storage.json'
    data=json.dumps(config,indent=2,sort_keys=True)+'\n'
    try:
        fd=os.open(destination,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        with os.fdopen(fd,'w') as f:f.write(data);f.flush();os.fsync(f.fileno())
    except FileExistsError:
        existing=json.loads(destination.read_text())
        if existing!=config:raise StorageError('existing storage configuration differs; not overwritten')
    return config

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path);parser.add_argument('--mount',type=Path);parser.add_argument('--image',type=Path)
    parser.add_argument('--initialize',action='store_true')
    args=parser.parse_args()
    paths=resolve_storage(args.root,mount=args.mount,image=args.image,initialize=args.initialize)
    report=initialize_state(paths) if args.initialize else paths.report()
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
