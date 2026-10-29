"""Full host lifecycle against local CLI fixtures, with no external service calls."""

import json
import os
import signal
import socket
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from urllib.request import ProxyHandler, build_opener


class HostTests(unittest.TestCase):
    def test_configured_scope_batches_and_shutdown_preserve_data(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with socket.socket() as sock:
                sock.bind(("127.0.0.1", 0))
                port = sock.getsockname()[1]
            dws = root / "dws-fixture"
            dws.write_text(
                "#!"
                + sys.executable
                + """
import sys,json,time
assert sys.argv[1:3]==['event','+listen-im']
assert sys.argv[sys.argv.index('--profile')+1]=='fixture:employee'
kind=sys.argv[sys.argv.index('--kind')+1]
group=kind=='group'
if group: assert sys.argv[sys.argv.index('--chat-id')+1]=='fixture-group'
print('[event] ready',file=sys.stderr,flush=True)
print(json.dumps({'conversation_id':'fixture-group' if group else 'fixture-direct',
 'message_id':'group-message' if group else 'same-message',
 'sender_open_dingtalk_id':'other-person','sender':'测试同事','content':'合成消息，请查收'}),flush=True)
while True: time.sleep(1)
"""
            )
            codex = root / "codex-fixture"
            codex.write_text(
                "#!"
                + sys.executable
                + """
import sys,json
assert sys.argv[1:3]==['app-server','--stdio']
def send(value): print(json.dumps(value),flush=True)
for line in sys.stdin:
 x=json.loads(line); method=x.get('method')
 if method=='initialize': send({'id':x['id'],'result':{}})
 elif method in ['thread/start','thread/resume','thread/fork']:
  send({'id':x['id'],'result':{'thread':{'id':'fixture-thread'}}})
 elif method=='turn/start':
  tid=x['params']['threadId']
  send({'id':x['id'],'result':{'turn':{'id':'fixture-turn'}}})
  text=json.dumps({'summary':'收到合成消息','needs_reply':False,'draft':'','todos':[]})
  send({'method':'turn/completed','params':{'threadId':tid,'turn':{
   'id':'fixture-turn','status':'completed','items':[{'type':'agentMessage','text':text}]}}})
"""
            )
            for command in [dws, codex]:
                os.chmod(str(command), 0o700)
            config = root / "config.json"
            config.write_text(
                json.dumps(
                    {
                        "profile": "fixture:employee",
                        "self_id": "fixture-self",
                        "display_name": "测试用户",
                        "group": {"id": "fixture-group", "name": "设计组"},
                        "server": {"port": port},
                        "commands": {"dws": str(dws), "codex": str(codex)},
                        "batch": {"direct_seconds": 1, "group_seconds": 1},
                    }
                )
            )
            process = subprocess.Popen(
                [sys.executable, "-m", "backend", "--config", str(config), "run"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            opener = build_opener(ProxyHandler({}))
            result = None
            try:
                deadline = time.monotonic() + 20
                while time.monotonic() < deadline:
                    self.assertIsNone(process.poll(), "host unexpectedly exited")
                    try:
                        with opener.open(
                            "http://127.0.0.1:" + str(port) + "/api/state", timeout=1
                        ) as response:
                            result = json.load(response)
                        if (
                            len(result["messages"]) == 2
                            and result["overview"]["updated"]
                            and all(item["draft"] for item in result["messages"])
                        ):
                            break
                    except OSError:
                        pass
                    time.sleep(0.2)
                self.assertIsNotNone(result)
                self.assertEqual(len(result["messages"]), 2)
                self.assertEqual(result["status"]["group_name"], "设计组")
                self.assertTrue(result["overview"]["updated"])
                direct = next(
                    item
                    for item in result["messages"]
                    if item["conversation_id"] == "fixture-direct"
                )
                self.assertEqual(set(direct["sources"]), {"direct", "at"})
                self.assertEqual(direct["draft"]["text"], "")
            finally:
                process.send_signal(signal.SIGTERM)
                out, err = process.communicate(timeout=20)
            self.assertEqual(process.returncode, 0, err.decode())
            self.assertTrue((root / "data/panel.db").is_file())
            state = json.loads((root / "data/output/运行状态.json").read_text())
            self.assertEqual(state["state"], "stopped")
