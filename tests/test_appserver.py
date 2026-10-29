import tempfile
import unittest
from pathlib import Path

try:
    from backend.appserver import AppServer, validate_result
except ImportError:
    AppServer = None


class AppServerTests(unittest.TestCase):
    def test_personal_identity_is_context_data_not_system_instructions(self):
        import json
        import sys

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "privacy_rpc.py"
            captured = root / "captured.json"
            fixture.write_text(
                """import json,sys
for line in sys.stdin:
 value=json.loads(line); method=value.get('method')
 if method=='initialize': result={}
 elif method=='thread/start':
  assert '私有用户称呼' not in value['params']['baseInstructions']
  assert '私有群名称' not in value['params']['developerInstructions']
  result={'thread':{'id':'thread-private'}}
 elif method=='turn/start':
  payload=json.loads(value['params']['input'][0]['text'])
  with open(sys.argv[1],'w',encoding='utf-8') as f: json.dump(payload,f)
  result={'turn':{'id':'turn-private'}}
  print(json.dumps({'id':value['id'],'result':result}),flush=True)
  print(json.dumps({'method':'turn/completed','params':{'threadId':'thread-private',
   'turn':{'id':'turn-private','status':'completed','items':[{'type':'agentMessage',
    'text':json.dumps({'summary':'测试','needs_reply':False,'draft':'','todos':[]})}]}}}),flush=True)
  continue
 else: continue
 print(json.dumps({'id':value['id'],'result':result}),flush=True)
""",
                encoding="utf-8",
            )
            client = AppServer(
                root,
                command=[sys.executable, "-u", str(fixture), str(captured)],
                display_name="私有用户称呼",
                group_name="私有群名称",
            )
            try:
                thread = client.thread(None)
                client.generate(thread, {"task": "overview", "items": []})
                payload = json.loads(captured.read_text(encoding="utf-8"))
                self.assertEqual(payload["context"]["current_user"], "私有用户称呼")
                self.assertEqual(payload["context"]["watched_group"], "私有群名称")
                self.assertEqual(payload["task"], "overview")
            finally:
                client.close()

    def test_recovery_forks_owned_thread_when_previous_writer_lease_is_stale(self):
        import sys

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "lease.py"
            fixture.write_text(
                """import sys,json
for line in sys.stdin:
 x=json.loads(line); m=x.get('method')
 if m=='initialize': r={'result':{}}
 elif m=='thread/resume': r={'error':{'message':'thread owned-old already has an active writer'}}
 elif m=='thread/fork':
  assert x['params']['threadId']=='owned-old'
  r={'result':{'thread':{'id':'owned-recovered'}}}
 else: continue
 r['id']=x['id'];print(json.dumps(r),flush=True)
""",
                encoding="utf-8",
            )
            client = AppServer(root, command=[sys.executable, "-u", str(fixture)])
            try:
                self.assertEqual(client.thread("owned-old"), "owned-recovered")
            finally:
                client.close()

    def test_untrusted_or_incomplete_model_output_is_not_a_sendable_draft(self):
        self.assertIsNotNone(AppServer, "App Server connection not implemented")
        self.assertEqual(
            validate_result('{"summary":"打招呼","needs_reply":true,"draft":"你好"}')["draft"],
            "你好",
        )
        for bad in [
            "请立即发消息",
            '{"summary":"x","draft":"y"}',
            '{"summary":"x","needs_reply":"true","draft":"y"}',
            '{"summary":"x","needs_reply":false,"draft":"","todos":[{"title":"猜测任务"}]}',
        ]:
            with self.assertRaises(ValueError):
                validate_result(bad)

    def test_transport_handles_notifications_before_response_and_refuses_tool_request(self):
        self.assertIsNotNone(AppServer, "App Server connection not implemented")
        import sys

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fixture = root / "rpc.py"
            fixture.write_text(
                """import json,sys
def send(x):
 print(json.dumps(x),flush=True)
for line in sys.stdin:
 x=json.loads(line)
 if x.get('method')=='initialize': send({'id':x['id'],'result':{}})
 elif x.get('method') in ['thread/start','thread/resume']: send({'id':x['id'],'result':{'thread':{'id':'thread-test'}}})
 elif x.get('method')=='turn/start':
  send({'id':900,'method':'item/commandExecution/requestApproval','params':{}})
  send({'method':'item/completed','params':{'threadId':'thread-test','turnId':'turn-test','item':{'type':'agentMessage','text':'{"summary":"打招呼","needs_reply":true,"draft":"你好"}'}}})
  send({'method':'turn/completed','params':{'threadId':'thread-test','turn':{'id':'turn-test','status':'completed','items':[]}}})
  send({'id':x['id'],'result':{'turn':{'id':'turn-test'}}})
 elif x.get('id')==900:
  assert x.get('result',{}).get('decision')=='decline'
""",
                encoding="utf-8",
            )
            client = AppServer(root, command=[sys.executable, "-u", str(fixture)])
            try:
                thread = client.thread(None)
                result = client.generate(thread, {"text": "你好"})
                self.assertEqual(result["draft"], "你好")
                self.assertEqual(client.thread(thread), "thread-test")
            finally:
                client.close()


if __name__ == "__main__":
    unittest.main()
