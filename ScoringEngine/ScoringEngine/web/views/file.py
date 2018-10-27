from datetime import datetime
from flask import render_template, make_response, request
from ScoringEngine.web import app
from ScoringEngine.core.db import getSession, tables

from ScoringEngine.web.flask_utils import db_user, require_group
from flask_login import current_user, login_required

from pyclamd import ClamdNetworkSocket, ClamdUnixSocket, ConnectionError, BufferTooLongError
from ScoringEngine.core import config, logger
from socket import error

from mimetypes import guess_type

@app.route('/file/<id>')
@login_required
@require_group(3)
@db_user
def file_download(id):
    session = getSession()
    f = session.query(tables.Attachment).filter(tables.Attachment.id == id).first()
    if f:
        if config.get_item("clam/enabled") and 'ignore_virus' not in request.args and not f.ignore_virus:
            if config.get_item("clam/stream_limit") < f.size:
                return render_template(
                    "injectscore/virus_error.html",
                )
            try:
                if config.has_item("clam/path"):
                    cd = ClamdUnixSocket(config.get_item("clam/path"))
                elif config.has_item("clam/address"):
                    cd = ClamdNetworkSocket(config.get_item("clam/address").encode('ascii'), config.get_item("clam/port"))
                cd.ping()
                logger.debug(cd.version())
                virus_info = cd.scan_stream(f.data)
                logger.debug(virus_info)
                if virus_info is not None:
                    return render_template(
                        "injectscore/virus.html",
                        virus_info=virus_info,
                        title="Virus Found"
                    )
            except ConnectionError as ce:
                logger.error(ce.message)
                return render_template(
                    "injectscore/virus_error.html",
                )
            except BufferTooLongError as btle:
                logger.error(btle.message)
                return render_template(
                    "injectscore/virus_error.html",
                )
            except error as se:
                logger.error(se.message)
                return render_template(
                    "injectscore/virus_error.html"
                )
        r = make_response(f.data)
        r.headers['Content-Disposition'] = 'inline; filename="' + f.filename + '"'
        ty, _ = guess_type(f.filename)
        if ty:
            r.mimetype = ty
        else:
            r.mimetype='application/octet-stream'
        return r
    from ScoringEngine.web.views.errors import page_not_found
    return page_not_found(None)