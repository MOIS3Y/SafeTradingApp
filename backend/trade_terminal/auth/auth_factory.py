from flask import Blueprint

# * Create Blueprint
bp = Blueprint('auth', __name__)


# * Praetorian blacklist
blacklist = set()


def is_blacklisted(jti):
    """ Gets and returns a blocked token from the blacklist"""
    return jti in blacklist
