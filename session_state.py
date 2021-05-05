# -*- coding: utf-8 -*-
"""
Created on Tue May  4 19:31:29 2021

@author: QTVo
"""
from typing import Callable, TypeVar
try:
    import streamlit.ReportThread as ReportThread
    from streamlit.server.Server import Server
except Exception:
    # Streamlit >= 0.65.0
    import streamlit.report_thread as ReportThread
    from streamlit.server.server import Server

T = TypeVar('T')


# noinspection PyProtectedMember
def get_state(setup_func: Callable[..., T], **kwargs) -> T:
    ctx = ReportThread.get_report_ctx()

    session = None
    session_infos = Server.get_current()._session_info_by_id.values()

    for session_info in session_infos:
         s = session_info.session
         if (
            # Streamlit < 0.54.0
            (hasattr(s, '_main_dg') and s._main_dg == ctx.main_dg)
            or
            # Streamlit >= 0.54.0
            (not hasattr(s, '_main_dg') and s.enqueue == ctx.enqueue)
            or
            # Streamlit >= 0.65.2
            (not hasattr(s, '_main_dg') and s._uploaded_file_mgr == ctx.uploaded_file_mgr)
        ):
            session = s

    if session is None:
        raise RuntimeError(
            "Oh noes. Couldn't get your Streamlit Session object"
            'Are you doing something fancy with threads?')

    # Got the session object! Now let's attach some state into it.

    if not getattr(session, '_custom_session_state', None):
        session._custom_session_state = setup_func(**kwargs)

    return session._custom_session_state