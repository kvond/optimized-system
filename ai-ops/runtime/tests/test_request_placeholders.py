import contextlib,io,json,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import birthday_check
import doe_worker

PLACEHOLDERS=('ACTUAL_UTC_RUN_TIME','doe-watch-YYYYMMDDTHHMMSSZ','YYYYMMDDTHHMMSSZ')

class RequestPlaceholderTests(unittest.TestCase):
    def invoke(self,module,request,extra=()):
        out=io.StringIO()
        with patch.object(sys,'argv',[module.__name__,'--request-id',request,*extra]),contextlib.redirect_stdout(out):code=module.main()
        return code,json.loads(out.getvalue())
    def test_birthday_placeholders_rejected_before_any_work(self):
        for ident in (*PLACEHOLDERS,' ACTUAL_UTC_RUN_TIME '):
            with self.subTest(request=ident),patch.object(birthday_check,'run') as run,patch.object(birthday_check,'build_context') as context,patch.object(birthday_check,'resolve_storage') as storage:
                code,result=self.invoke(birthday_check,ident)
                self.assertEqual(code,2);self.assertEqual(result['reason'],'literal_request_timestamp_placeholder')
                self.assertEqual(result['ai_calls'],0);self.assertIsNone(result['counts'])
                run.assert_not_called();context.assert_not_called();storage.assert_not_called()
    def test_doe_placeholders_rejected_before_any_work_even_detail(self):
        for ident in (*PLACEHOLDERS,' YYYYMMDDTHHMMSSZ '):
            with self.subTest(request=ident),patch.object(doe_worker,'packet') as packet,patch.object(doe_worker,'build_context') as context,patch.object(doe_worker,'resolve_storage') as storage,patch.object(doe_worker.doe_check,'check') as source:
                code,result=self.invoke(doe_worker,ident,('--vacancy-id','37293'))
                self.assertEqual(code,2);self.assertEqual(result['reason'],'literal_request_timestamp_placeholder')
                self.assertEqual(result['ai_calls'],0);self.assertIsNone(result['listings'])
                packet.assert_not_called();context.assert_not_called();storage.assert_not_called();source.assert_not_called()
    def test_explicit_existing_ids_pass_through_unchanged(self):
        for ident in ('doe-watch-20261013T003000Z','20261013T003000Z','existing-request-42'):
            with self.subTest(request=ident),patch.object(birthday_check,'run',return_value={'status':'complete'}) as run:
                code,result=self.invoke(birthday_check,ident);self.assertEqual(code,0);run.assert_called_once_with(ident)
            with self.subTest(request=ident),patch.object(doe_worker,'packet',return_value={'status':'complete'}) as packet:
                code,result=self.invoke(doe_worker,ident,('--vacancy-id','37293'));self.assertEqual(code,0);packet.assert_called_once_with(ident,'37293')
if __name__=='__main__':unittest.main()
