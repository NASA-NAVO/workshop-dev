# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""
VO Queries
"""

from __future__ import print_function, division
#from IPython.core.debugger import Tracer
from astroquery.query import BaseQuery
#from astroquery.utils.tap.core import Tap as aqTap, TapPlus
from pyvo.dal import tap as pyvoTap
import numpy
from . import utils

# For raw Data Access Layer Information requests
import urllib.request
import urllib.error
import xml.etree.ElementTree

__all__ = ['Tap', 'TapClass']

class TapClass(BaseQuery):
    """
    Tap query class.
    """


    def __init__(self):

        super(TapClass, self).__init__()
        self._TIMEOUT = 60 # seconds
        self._RETRIES = 2 # total number of times to try

    def query(self, service, query, upload_file=None,upload_name=None):
        """Simple wrapper based on pyvo.dal.tap.

        Accepts either a string URL or an entry in an astropy table
        that has an "access_url" entry as returned by a
        Registry.query().  Optional file upload for
        cross-correlations.

        """

        if type(service) is str:
            service = {"access_url":service}

        ##  Remove the /sync? if you're going to use pyvoTap instead of aqTap
        url = service['access_url'] #  + '/sync?'

        ##  The following is the original navo_utils.Tap way based on astroquery's 
        ##  BaseQuery
        """
        tap_params = {
            "request": "doQuery",
            "lang": "ADQL",
            "query": query
        }
        if upload_file is not None:
            import requests, io
            if upload_name is None:
                print("ERROR: you have to give upload_name to use in the query for the uploaded table.")
                return None

            ## Why does neither of these work with utils.try_query(files=files....) ?
            #files={'uplt':open(upload_file,'rb')}
            #files={'uplt':upload_file}
            #tap_params['upload'] = upload_name+',param:uplt'

            if type(upload_file) is str:
                files={'uplt':open(upload_file, 'rb')}
            elif type(upload_file) is io.BytesIO:
                files={'uplt':upload_file}
            cc_params={
                'lang': 'ADQL', 
                'request': 'doQuery',
                'upload':'{},param:uplt'.format(upload_name)
                }

            cc_params["query"]=query
            response = requests.post(url,data=cc_params,stream=True,files=files)
            
        else:
            response = utils.try_query(url, post_data=tap_params, timeout=self._TIMEOUT, retries=self._RETRIES)

        aptable = utils.astropy_table_from_votable_response(response)

        """

        ##  Not terribly well documented what's Tap and what's TapPlus in 
        ##  https://astroquery.readthedocs.io/en/latest/utils/tap.html
        ##  but this should work for all generic Tap services.  

        ## Using astroquery/gaia original way
        #service=TapPlus(url)
        #job=service.launch_job(query=query,upload_resource=upload_file, upload_table_name=upload_name)
        #return job.get_results()
    
        ## Using pyvo way
        service=pyvoTap.TAPService(url)
        ## Internet example service.run_sync(query, uploads = {'t1': open('/path/to/votable.xml')})
        if upload_name is not None:
            ## UNTESTED
            return service.run_sync(query=query,uploads={upload_name:upload_file})
        else:
            return service.run_sync(query=query)



    def list_tables(self,service_url,contains=None):
        """Uses astroquery/gaia Tap.load_tables()"""
        #tap_service = aqTap(url=service_url)
        #tables=tap_service.load_tables()
        tables=pyvoTap.TAPService(service_url).tables
        retlist=[]
        for tname in (tables.keys()):
            #tname=table.get_qualified_name()
            if contains is None or (contains is not None and contains in tname):
                #print(tname)
                retlist.append(tname)
        return retlist


    def list_columns(self, service_url, tablename):
        """Simple way to get column names by getting 1st row only.  To be done more intelligently."""

        query="select top 1 * from {}".format(tablename) 
        try:
            table=self.query( service_url, query).table
            if len(table) > 0:
                return table.columns
            else:
                return table.meta
        except:
            return table.meta
        
    def list_examples(self, service_url):
        """Simple way to get list of ADQL example queries provided by the service. Empty list if no examples endpoint provided."""
        retlist=[]
        try:
            DALI_response = urllib.request.urlopen(service_url + '/examples')
            DALI_doctree = xml.etree.ElementTree.parse(DALI_response)
            root = DALI_doctree.getroot()
            exampleElements = root.findall('.//*[@property="query"]')
            for example in exampleElements:
                retlist.append(example.text)
        except urllib.error.URLError:
            retlist=[]
        return retlist

Tap = TapClass()
