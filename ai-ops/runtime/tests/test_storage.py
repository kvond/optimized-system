import pathlib,sys,tempfile,unittest,os
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from storage import resolve_storage,initialize_state,StorageError
from foundation import Store,CacheContract,UTC
import datetime as dt
from dataclasses import replace
class StorageTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.mount=pathlib.Path(self.tmp.name).resolve()/'private';self.mount.mkdir(mode=0o700);self.root=self.mount/'AI-Archive/state/ai-ops';self.image=pathlib.Path(self.tmp.name).resolve()/'backing.sparsebundle'
  self.probe=lambda mount,image:{'mount_verified':True,'encryption_verified':True,'filesystem':'apfs','mount':str(mount),'backing_image':str(image)}
 def tearDown(self):self.tmp.cleanup()
 def resolve(self,**kw):return resolve_storage(self.root,mount=self.mount,image=self.image,probe=self.probe,environ={},**kw)
 def test_missing_or_unverified_mount_makes_zero_directories(self):
  self.probe=lambda *args:{'mount_verified':False,'encryption_verified':False,'filesystem':'apfs'}
  with self.assertRaises(StorageError):self.resolve(initialize=True)
  self.assertFalse((self.mount/'AI-Archive').exists())
 def test_private_state_init_reopen_and_cache_survives(self):
  paths=self.resolve(initialize=True);first=initialize_state(paths)
  store=Store(paths.cache);contract=CacheContract('synthetic','storage-test','1','read','1',{},'1')
  store.put(contract,{'ok':True},dt.datetime.now(UTC)+dt.timedelta(days=1),succeeded=True)
  self.assertEqual(first,initialize_state(self.resolve(initialize=True)))
  self.assertEqual(Store(paths.cache).get(contract),{'ok':True})
  for path in [paths.root,paths.receipts]:self.assertEqual(path.stat().st_mode&0o777,0o700)
  for path in [paths.cache,paths.usage,paths.root/'runtime-storage.json']:self.assertEqual(path.stat().st_mode&0o777,0o600)
 def test_symlink_or_outside_mount_rejected_without_creating(self):
  outside=pathlib.Path(self.tmp.name).resolve()/'outside';outside.mkdir(mode=0o700);(self.mount/'AI-Archive').symlink_to(outside,target_is_directory=True)
  with self.assertRaises(StorageError):self.resolve(initialize=True)
  self.assertEqual(list(outside.iterdir()),[])
  with self.assertRaises(StorageError):resolve_storage(outside,mount=self.mount,image=self.image,probe=self.probe,initialize=True,environ={})
 def test_public_existing_directory_preserved_unchanged(self):
  public=self.mount/'AI-Archive';public.mkdir(mode=0o755);marker=public/'keep';marker.write_text('unchanged')
  with self.assertRaises(StorageError):self.resolve(initialize=True)
  self.assertEqual(marker.read_text(),'unchanged');self.assertEqual(public.stat().st_mode&0o777,0o755);self.assertFalse((public/'state').exists())
 def test_verification_loss_before_write_fails_closed(self):
  calls=[]
  def probe(*args):
   calls.append(1);return {'mount_verified':True,'encryption_verified':len(calls)==1,'filesystem':'apfs'}
  self.probe=probe
  with self.assertRaises(StorageError):self.resolve(initialize=True)
  self.assertFalse((self.mount/'AI-Archive').exists())
 def test_environment_selection_and_explicit_override(self):
  env={'AI_OPS_STORAGE_ROOT':str(self.root),'AI_OPS_ARCHIVE_MOUNT':str(self.mount),'AI_OPS_BACKING_IMAGE':str(self.image)}
  paths=resolve_storage(environ=env,probe=self.probe,initialize=True);self.assertEqual(paths.root,self.root)
  alternative=self.mount/'different';paths=resolve_storage(alternative,environ=env,probe=self.probe,initialize=True);self.assertEqual(paths.root,alternative)
 def test_parent_traversal_and_symlink_database_rejected(self):
  with self.assertRaises(StorageError):resolve_storage(self.mount/'..'/'escape',mount=self.mount,image=self.image,probe=self.probe,initialize=True,environ={})
  paths=self.resolve(initialize=True);target=pathlib.Path(self.tmp.name).resolve()/'protected-file';target.write_text('preserve')
  paths.cache.symlink_to(target)
  with self.assertRaises(StorageError):self.resolve(initialize=True)
  self.assertEqual(target.read_text(),'preserve')
 def test_lost_mount_after_resolve_cannot_initialize_databases(self):
  paths=self.resolve(initialize=True)
  # Revocation between root resolution and database setup must be checked again.
  paths=replace(paths,probe=lambda *args:{'mount_verified':False,'encryption_verified':False,'filesystem':'apfs'})
  with self.assertRaises(StorageError):initialize_state(paths)
  self.assertFalse(paths.cache.exists());self.assertFalse(paths.usage.exists())
 def test_private_existing_configuration_conflict_not_overwritten(self):
  paths=self.resolve(initialize=True);initialize_state(paths);config=paths.root/'runtime-storage.json';config.write_text('{"other":true}')
  with self.assertRaises(StorageError):initialize_state(paths)
  self.assertEqual(config.read_text(),'{"other":true}')
class VerifiedMountMetadataTests(unittest.TestCase):
 def setUp(self):
  import plistlib
  from unittest.mock import patch
  self.mount=pathlib.Path('/Volumes/Synthetic-Private-Archive')
  self.image=pathlib.Path('/Volumes/Synthetic-Backing/archive.sparsebundle')
  self.disk={'MountPoint':str(self.mount),'FilesystemType':'apfs'}
  self.entry={'image-path':str(self.image),'image-encrypted':True,
              'system-entities':[{'mount-point':str(self.mount)}]}
  self.entries=[self.entry];self.fallback=b'encrypted: YES\n';self.calls=[]
  def command(argv):
   self.calls.append(argv)
   if argv[:2]==['diskutil','info']:return plistlib.dumps(self.disk)
   if argv[:2]==['hdiutil','info']:return plistlib.dumps({'images':self.entries})
   if argv[:2]==['hdiutil','isencrypted']:return self.fallback
   raise AssertionError('unexpected command')
  for target,kwargs in [('storage.os.path.ismount',{'return_value':True}),
                        ('storage.Path.is_dir',{'return_value':True}),
                        ('storage._command',{'side_effect':command})]:
   mocker=patch(target,**kwargs);mocker.start();self.addCleanup(mocker.stop)
 def verify(self):
  from storage import verified_mount
  return verified_mount(self.mount,self.image)
 def test_true_exact_mounted_metadata_does_not_reopen_busy_image(self):
  self.assertTrue(self.verify()['encryption_verified'])
  self.assertFalse(any(c[:2]==['hdiutil','isencrypted'] for c in self.calls))
 def test_false_nonboolean_metadata_never_falls_back_to_yes(self):
  for value in (False,1,'true'):
   self.entry['image-encrypted']=value
   with self.assertRaises(StorageError):self.verify()
  self.assertFalse(any(c[:2]==['hdiutil','isencrypted'] for c in self.calls))
 def test_missing_encryption_metadata_requires_noninteractive_yes_probe(self):
  self.entry.pop('image-encrypted')
  self.assertTrue(self.verify()['encryption_verified'])
  self.assertIn(['hdiutil','isencrypted',str(self.image)],self.calls)
  self.fallback=b'encrypted: NO\n'
  with self.assertRaises(StorageError):self.verify()
 def test_fallback_busy_failure_does_not_infer_encryption(self):
  from unittest.mock import patch
  self.entry.pop('image-encrypted')
  original=__import__('storage')._command
  def busy(argv):
   if argv[:2]==['hdiutil','isencrypted']:raise StorageError('busy image')
   return original(argv)
  with patch('storage._command',side_effect=busy):
   with self.assertRaises(StorageError):self.verify()
 def test_wrong_image_or_duplicate_mount_binding_rejected(self):
  self.entry['image-path']='/Volumes/Synthetic-Backing/wrong.sparsebundle'
  with self.assertRaises(StorageError):self.verify()
  self.entry['image-path']=str(self.image);self.entries.append(dict(self.entry))
  with self.assertRaises(StorageError):self.verify()
 def test_wrong_mount_or_filesystem_rejected_despite_encrypted_true(self):
  self.disk['MountPoint']='/Volumes/Wrong'
  with self.assertRaises(StorageError):self.verify()
  self.disk['MountPoint']=str(self.mount);self.disk['FilesystemType']='exfat'
  with self.assertRaises(StorageError):self.verify()
 def test_fresh_changed_metadata_rejects_previously_verified_image(self):
  self.assertTrue(self.verify()['encryption_verified'])
  self.entry['image-encrypted']=False
  with self.assertRaises(StorageError):self.verify()

if __name__=='__main__':unittest.main()
