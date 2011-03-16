import urllib2
import json
from base64 import b64encode

class Harvest(object):
    
    
    def __init__(self, uri, username, password):
        """ Set the things we need to use harvest """
        
        self.uri = uri
        self.username = username
        self.password = password
        
        self.headers = {
        'Authorization':'Basic '+b64encode('%s:%s' % (self.username, self.password)),
        'Accept':'application/json',
        'Content-Type':'application/json',
        'User-Agent':'harvest.py',
        }
        
    def _request(self, url):
        """ Make a request to the harvest web service """
        
        request = urllib2.Request(url = self.uri + url, headers = self.headers)
        
        r = urllib2.urlopen(request)
        j = r.read()
        return json.loads(j)
    
    def get_project_list(self):
        """ Get a list of projects from harvest """
        data = self._request('/daily')
        return data['projects']
    
    def get_project_in_categories(self):
        """ Get the project list, but organised into clients """
        data = self.get_project_list()
        
        ret_data = {}
        
        for project in data:
            if ret_data.has_key(project['client']):
                ret_data[project['client']].append(project)
            else:
                ret_data[project['client']] = [project]
                
        return ret_data