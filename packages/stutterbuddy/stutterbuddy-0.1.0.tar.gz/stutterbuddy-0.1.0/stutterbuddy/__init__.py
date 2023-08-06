"""
    Author: Jonas Briguet
    Date: 06.12.2021
    Last Change: 14.08.2022
    version: 0.1.0
    This is a library with functions to interact with the stutterbuddy.ch api 
"""

import requests
from requests_toolbelt import MultipartEncoderMonitor
import urllib.parse
import json

class Worker():
    """A class to interact with the stutterbuddy.ch api"""

    def __init__(self, API_KEY, verbose=1):
        self.API_KEY = API_KEY
        self.verbose = verbose

    def submit_url(self, url, use_profile='false', resolution='720', threshold='10', min_silence='0', stutter_detection='true', share_data='false', submit='true', notify_email='false', debug='false', detach_cuts='false', cut_list='false', video_name='', verbose=1):
        """A function to submit urls to stutterbuddy using the API. More information on the arguments taken available at https://stutterbuddy.ch/api-doc 
        returns a boolean which is true or false to tell if a request was sucessful and a the http response of the API server"""
        ENDPOINT = 'https://stutterbuddy.ch/api/submit/link'
        r = requests.post(URL,
                          json={
                              'api_key': self.API_KEY,
                              'video_url': video_url,
                              'video_name': video_name,
                              'use_profile': use_profile,
                              'resolution': resolution,
                              'threshold': threshold,
                              'min_silence': min_silence,
                              'stutter_detection': stutter_detection,
                              'share_data': share_data,
                              'submit': submit,
                              'notify_email': notify_email,
                              'detach_cuts': detach_cuts,
                              'cut_list': cut_list,
                              'debug': debug
                          },
                          ).json()

        if verbose >= 2:
            print(r)

        if 'error' in r:
            raise Exception(
                "Error occured when submitting video by url: "+r['error'])
        elif 'message' in r and r['message'] == 'success':
            return r['settings'], r['settings']['upload_id']

    def submit_file(self, path_to_file, use_profile='false', resolution='720', threshold='10', min_silence='0', stutter_detection='true', share_data='false', submit='true', notify_email='false', debug='false', detach_cuts='false', cut_list='false', video_name='', verbose=1, callback=None):
        """A function to submit local files to stutterbuddy using the API. More information on the arguments taken available at https://stutterbuddy.ch/api-doc
        returns the settings applied to the video and the upload_id of the video.
        Has 3 verbose levels: 0 for no cmd line output, 1 for basic information on progress and 3 for debugging purposes"""

        # request new upload id
        r = requests.get('https://stutterbuddy.ch/api/upload/request-upload?key=' +
                         urllib.parse.quote(self.API_KEY)).json()

        if verbose >= 2:
            print(r)

        if 'error' in r:
            raise Exception("Error occured when requesting slot: "+r['error'])

        upload_id = r['upload_id']
        cdn_url = r['worker_url']

        m = MultipartEncoderMonitor.from_fields(
            fields={
                'api_key': self.API_KEY,
                'video_name': video_name,
                'use_profile': use_profile,
                'resolution': resolution,
                'threshold': threshold,
                'min_silence': min_silence,
                'stutter_detection': stutter_detection,
                'share_data': share_data,
                'submit': submit,
                'notify_email': notify_email,
                'detach_cuts': detach_cuts,
                'cut_list': cut_list,
                'debug': debug,
                'files': (path_to_file, open(path_to_file, 'rb'), 'text/plain')
            },
            callback=(callback)
        )

        if verbose >= 1:
            print('Uploading file to StutterBuddy')

        r = requests.post(cdn_url+'/api/worker/submit/file/'+urllib.parse.quote(upload_id), data=m,
                          headers={'Content-Type': m.content_type}, timeout=(10, 2000)).json()
        if verbose >= 1:
            print('Upload finished')
        if verbose >= 2:
            print(r)

        if 'error' in r:
            raise Exception("Error occured when submitting video: "+r['error'])
        elif 'message' in r and r['message'] == 'success':
            return r['settings'], upload_id

    def get_info(self, upload_id):
        """
            Takes a single upload_id as string and the API_KEY
            returns video_name, video_url, status, timesaved corresponding to upload_id
        """
        result = requests.get('https://stutterbuddy.ch/api/data/request/single?key=' +
                              urllib.parse.quote(self.API_KEY)+"&uploadid="+urllib.parse.quote(upload_id)).json()

        if 'error' in result:
            raise Exception(
                "Error occured when requesting info: "+result['error'])
        else:
            return result['data']
