#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from uuid import uuid4

from dash import CeleryManager
from dash import DiskcacheManager
from diskcache import Cache
from celery import Celery

launch_uid = uuid4()


def create_cache_manager(app):
    """Create new cache manager."""

    if isinstance(app.config.get("REDIS_URL"), str):
        celery_app = Celery(
            __name__,
            broker=app.config.get("REDIS_URL"),
            backend=app.config.get("REDIS_URL"),
        )
        manager = CeleryManager(
            celery_app,
            cache_by=[lambda: launch_uid],
            expire=60,
        )
    else:
        cache = Cache(
            path.join(app.instance_path, ".cache"),
        )
        manager = DiskcacheManager(
            cache,
            cache_by=[lambda: launch_uid],
            expire=60,
        )
    return manager
