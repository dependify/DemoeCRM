"""
Demo Backend Module
"""

from .demo_database import (
    get_demo_database,
    get_main_database,
    close_demo_database,
    close_main_database,
    create_demo_indexes,
    reset_demo_database,
    get_demo_stats,
    DEMO_COLLECTIONS,
    DEMO_DB_SUFFIX,
)

__all__ = [
    "get_demo_database",
    "get_main_database",
    "close_demo_database",
    "close_main_database",
    "create_demo_indexes",
    "reset_demo_database",
    "get_demo_stats",
    "DEMO_COLLECTIONS",
    "DEMO_DB_SUFFIX",
]
