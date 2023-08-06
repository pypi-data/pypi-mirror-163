# Mobile Verification Toolkit (MVT)
# Copyright (c) 2021-2022 Claudio Guarnieri.
# Use of this software is governed by the MVT License 1.1 that can be found at
#   https://license.mvt.re/1.1/

import logging

from mvt.common.command import Command

from .modules.backup import BACKUP_MODULES
from .modules.mixed import MIXED_MODULES

log = logging.getLogger(__name__)


class CmdIOSCheckBackup(Command):

    def __init__(self, target_path: str = None, results_path: str = None,
                 ioc_files: list = [], module_name: str = None,
                 serial: str = None, fast_mode: bool = False):
        super().__init__(target_path=target_path, results_path=results_path,
                         ioc_files=ioc_files, module_name=module_name,
                         serial=serial, fast_mode=fast_mode, log=log)

        self.name = "check-backup"
        self.modules = BACKUP_MODULES + MIXED_MODULES

    def module_init(self, module):
        module.is_backup = True
