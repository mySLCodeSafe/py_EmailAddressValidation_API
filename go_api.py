import flask
from dns.resolver import query
from difflib import get_close_matches
from flask import request, jsonify
from cachetools import cached, TTLCache

cache_validateDomain = TTLCache(maxsize=1000, ttl=300)
cache_suggestDomain = TTLCache(maxsize=1000, ttl=300) # set a lower ttl for new domains added to the safelist during i_validateDomain_MX to come into affect
app = flask.Flask(__name__)
safeList={'gmail.com','argos.co.uk','homeretailgroup.com'}

app.config["DEBUG"] = False

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@cached(cache_validateDomain)
def i_validateDomain_MX(domain):  # function performing under cache to reduce the number of calls
    try:
        if domain in safeList:
            return True
        else:
            query(domain, 'MX')
            safeList.add (domain) # add domain with valid MX record to the safelist - will be used once the suggestCorrectDomain cache expires
            return True # return positive as domain has a valid MX record
    except:
        return False # return negative as domain has no valid MX record

@cached(cache_suggestDomain)
def i_suggestCorrectDomain(domain):
    try:
        rtnResult = (get_close_matches(domain,safeList))
        return (rtnResult) # return results back from close match
    except:
        return False

# ** App route functions **

@app.route('/', methods=['GET'])
def home():
    return "<h1>This will return POSTMAN API documentation</p>"

@app.route('/api/v1/validateDomain', methods=['GET'])
def validateDomain():
    if 'domain' in request.args:
        ext_domainToValidate = str(request.args['domain'])
        results = int(i_validateDomain_MX(ext_domainToValidate))
    else:
        return "Error: No domain field provided. Please specify an domain."
    return jsonify(results)

@app.route('/api/v1/suggestDomain',methods=['GET'])
def suggestCorrectDomain():
    if 'domain' in request.args:
        ext_domainToQuery = str(request.args['domain'])
        results = (i_suggestCorrectDomain(ext_domainToQuery))
    else:
        return "Error: No domain field provided. Please specify a domain."
    return jsonify(results)

@app.route('/admin/',methods=['GET'])
def listSize():
    if 'safelistsize' in request.args:
        results = str(len(safeList))
    else:
        return "Error: no field provided."
    return jsonify(results)

app.run()