import urllib2
import urllib
import json
from base64 import b64encode
from datetime import datetime

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
        
        self.xml_headers = {
        'Authorization':'Basic '+b64encode('%s:%s' % (self.username, self.password)),
        'Accept':'application/xml',
        'Content-Type':'application/xml',
        'User-Agent':'harvest.py',
        }
        
    def _request(self, url):
        """ Make a request to the harvest web service """
        
        request = urllib2.Request(url = self.uri + url, headers = self.headers)
        
        r = urllib2.urlopen(request)
        j = r.read()
        return json.loads(j)
    
    def _post(self, url, data):
        """ Send data to the harvest web service """
        request = urllib2.Request(url = self.uri + url, data = data, headers = self.headers)
        
        r = urllib2.urlopen(request)
        j = r.read()
        return json.loads(j)
    
    def get_day_entries(self):
        """ Get all the information from the daily api """
        data = self._request('/daily')
        return data['day_entries']
    
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
    
    def timer_toggle(self, project, task):
        
        # first check if we have a daily entry for this project and task
        data = self.get_day_entries()
        
        entry_id = None
        
        for entry in data:
            if entry['project'] == project['name'] and entry['task'] == task['name']:
                entry_id = entry['id']
                
        if entry_id:
            url = "/daily/timer/" + str(entry_id)
        
            return self._request(url)
        else:
            
            # if we get here, we don't have a day entry for this project yet
            # create one, then use that
            
            data = {}
            data['notes'] = "Timer started by harvest-notifier"
            data['hours'] = " "
            data['project_id'] = project['id']
            data['task_id'] = task['id']
            data['spent_at'] = datetime.now().strftime("%a, %d %b %Y")
            
            data = json.dumps(data)
            
            return self._post('/daily/add', data)
        