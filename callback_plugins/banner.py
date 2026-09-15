from __future__ import annotations
import os
from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'aggregate'
    CALLBACK_NAME = 'banner'
    CALLBACK_NEEDS_ENABLED = True

    def v2_playbook_on_start(self, playbook):
        path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'img', 'banner.txt'
        )
        try:
            with open(path) as f:
                self._display.display("\n" + f.read())
        except OSError:
            pass
