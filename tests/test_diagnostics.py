"""Read real subprocess outputs from a local CLI fixture, never real tokens."""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

from backend.config import load_config
from backend.diagnostics import doctor


class DiagnosticsTests(unittest.TestCase):
    def test_user_id_verifies_profile_without_inventing_missing_open_id(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cli = root / "cli"
            cli.write_text(
                "#!"
                + sys.executable
                + """
import json,sys
if sys.argv[1:3] == ['auth','status']:
 print(json.dumps({'authenticated':True,'user_id':'person','token_valid':True}))
elif sys.argv[1:4] == ['contact','user','get-self']:
 print(json.dumps({'result':[{'orgEmployeeModel':{'userId':'person'}}]}))
elif sys.argv[1:3] == ['login','status']:
 print('Logged in using ChatGPT')
else: sys.exit(2)
"""
            )
            os.chmod(str(cli), 0o700)
            path = root / "config.json"
            path.write_text(
                json.dumps(
                    {
                        "profile": "corp:person",
                        "self_id": "known-open-id",
                        "display_name": "我",
                        "group": {"id": "cid", "name": "设计"},
                        "commands": {"dws": str(cli), "codex": str(cli)},
                    }
                )
            )
            results = doctor(load_config(path))
            open_id = next(item for item in results if item["name"] == "本人 OpenID")
            self.assertEqual(open_id.get("level"), "warning")
            self.assertFalse(open_id["ok"])
            self.assertTrue(next(item for item in results if item["name"] == "钉钉本人")["ok"])
            self.assertNotIn("token_valid", json.dumps(results))
