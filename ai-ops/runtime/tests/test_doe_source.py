import datetime as dt
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from doe_source import GRANT, SOURCE_URL, IncompleteSource, parse_output, read_source

NOW=dt.datetime(2026,10,12,22,30,tzinfo=dt.timezone.utc)
SHELL=b'var targetURL = "jobpostings/Output.asp"; var Search = location.search; ScriptLoc = targetURL + Search'

def output(count=1, location='Delaware Department of Education', ids=('101',), description=True):
    h="<div id='AppliTrackOutput'><form>Having location:\""+location+'\" ('+str(count)+' openings)'
    for key in ids:
        h+="<table><td id='wrapword'>Synthetic public opening</td><td>JobID: "+key+'</td></table>'
        if description:h+="<span id='DescriptionText"+key+"_1'><span>"+('Public job responsibilities and application requirements. '*4)+'</span></span>'
    h+='</form></div>'
    return ("document.write('"+h.replace('\\','\\\\').replace("'","\\'")+"');").encode()

class DoeSourceTests(unittest.TestCase):
    def test_complete_exact_scope_and_public_authentication(self):
        calls=[]
        def fetch(url):calls.append(url);return SHELL if url==SOURCE_URL else output()
        result=read_source(fetch=fetch,now=lambda:NOW)
        self.assertIsNone(result.reason);self.assertTrue(result.read.complete)
        self.assertFalse(result.read.authenticated);self.assertFalse(GRANT.requires_authentication)
        self.assertEqual(result.read.records[0]['vacancy_id'],'101')
        self.assertEqual(len(calls),2);self.assertIn('jobpostings/Output.asp?',calls[1])
        self.assertIn('location%3A%22Delaware+Department+of+Education%22',calls[1])
        self.assertEqual(result.evidence['model_calls'],0)
    def test_truncated_and_metadata_only_are_holds(self):
        for body in (b'<html>metadata only</html>',output()[:-25],output(count=2),output(description=False)):
            with self.subTest(body_size=len(body)):
                result=read_source(fetch=lambda url:SHELL if url==SOURCE_URL else body,now=lambda:NOW)
                self.assertFalse(result.read.complete);self.assertFalse(result.read.available)
                self.assertIsNone(result.evidence['posting_count']);self.assertEqual(result.read.records,[])
    def test_filter_isolation_duplicates_and_external_script_rejected(self):
        for body in (output(location='Other employer'),output(count=2,ids=('101','101'))):
            with self.assertRaises(IncompleteSource):parse_output(body)
        calls=[]
        def fetch(url):calls.append(url);return b'var targetURL="https://other.example/postings"'
        result=read_source(fetch=fetch,now=lambda:NOW)
        self.assertFalse(result.read.complete);self.assertEqual(calls,[SOURCE_URL])
    def test_timeout_size_and_unsupported_escapes_preserve_unknown(self):
        def timeout(url):raise TimeoutError('not included in receipt')
        result=read_source(fetch=timeout,now=lambda:NOW)
        self.assertEqual(result.reason,'TimeoutError');self.assertIsNone(result.evidence['posting_count'])
        result=read_source(fetch=lambda url:b'x'*1_000_001,now=lambda:NOW)
        self.assertFalse(result.read.complete)
        with self.assertRaises(IncompleteSource):parse_output(output().replace(b'Synthetic',b'\\x41Synthetic'))
    def test_zero_is_complete_only_with_exact_structural_evidence(self):
        self.assertEqual(parse_output(output(count=0,ids=())),[])
        with self.assertRaises(IncompleteSource):parse_output(output(count=0))

if __name__=='__main__':unittest.main()
