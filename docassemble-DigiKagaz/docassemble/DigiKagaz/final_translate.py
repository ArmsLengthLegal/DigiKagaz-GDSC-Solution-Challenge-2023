import apiclient
import docassemble.base.util
from googletrans import Translator

def paid_trans(arr):
  try:
    out = {}
    api = docassemble.base.util.DAGoogleAPI()
    service = apiclient.discovery.build('translate', 'v2', developerKey='AIzaSyAKMRS7UKIg4kMMwXEVv0OyyB6RPCUmctM')
    res = service.translations().list(source="en",target="hi",q=arr).execute()
    for i in range(len(arr)):
      out[arr[i]] = res['translations'][i]['translatedText']
    return True, out
  except Exception as e:
    return False, e

def trans(arr):
    output = {}
    translator = Translator()
    for trans in translator.translate(arr, src='en', dest='hi'):
        if trans.origin == trans.text:
            return paid_trans(arr)
        output[trans.origin] = trans.text
    return True, output  