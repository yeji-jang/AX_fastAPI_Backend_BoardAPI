"""
Board 엔티티 (게시판 설정)
"""

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

from board.domain.enums import Role