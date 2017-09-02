import csv
import urllib.request
import datetime
import time

from flask import redirect, render_template, request, session, url_for
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function
    
    
def convert_dt_s(dt):
    """
    Convert user date/time input into relative seconds (for comparison)
    
    """
    
    sdt = datetime.datetime.strptime(dt, "%m/%d/%Y %I:%S %p")
    print (sdt)
    condt = time.mktime(sdt.timetuple())
    return condt 
    

