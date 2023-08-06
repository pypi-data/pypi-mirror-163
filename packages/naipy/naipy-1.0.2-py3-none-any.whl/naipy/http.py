import urllib.request
import warnings
from typing import List, Dict
import json
from naipy.error import ConverError
import aiohttp


class NaipyRequest:
  base_url = "https://openapi.naver.com/v1/"
  
  def __init__(
    self, 
    client_id : str = None, 
    client_secret : str = None
  ) -> None:
    if not client_id or not client_secret:
      self.client_id = "p7aYK48ehm6TqdhTt_yv"
      self.client_secret = "UJAqwrxSfQ"
      warnings.warn("샘플키로 요청합니다.", UserWarning)
    else:
      self.client_id = client_id
      self.client_secret = client_secret

  def s_request(
    self,
    tag : List[str],
    text : str
  ):
    encText = urllib.parse.quote(text)
    URL = self.base_url + tag[0] + "/" + tag[1] + "?query=" + encText
    request = urllib.request.Request(URL)
    request.add_header("X-Naver-Client-Id", self.client_id)
    request.add_header("X-Naver-Client-Secret", self.client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
      response_body = response.read()
      result = json.loads(response_body)
      return result

  def t_request(
    self,
    tag : List[str],
    text : str
  ):
    encText = urllib.parse.quote(text)
    URL = self.base_url + tag[0] + "/" + tag[1]
    
    data = tag[2] + encText
    request = urllib.request.Request(URL)
    request.add_header("X-Naver-Client-Id", self.client_id)
    request.add_header("X-Naver-Client-Secret", self.client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if(rescode==200):
      response_body = response.read()
      result = json.loads(response_body)
      return result
    else:
      raise ConverError(f"Error Code : {rescode}")  

  def get_result(self, tag: List[str], text):
    if tag[0] == "search":
      return self.s_request(tag, text)
    else:
      return self.t_request(tag, text)

class AsyncNaipyRequest:
  base_url = "https://openapi.naver.com/v1/"

  def __init__(
    self, 
    client_id : str = None, 
    client_secret : str = None
  ) -> None:
    if not client_id or not client_secret:
      self.client_id = "p7aYK48ehm6TqdhTt_yv"
      self.client_secret = "UJAqwrxSfQ"
      warnings.warn("샘플키로 요청합니다.", UserWarning)
      warnings.warn("샘플키로 요청합니다.", UserWarning)
    else:
      self.client_id = client_id
      self.client_secret = client_secret

  async def s_request(
    self,
    tag : List[str],
    text : str
  ):
    headers : Dict = {"X-Naver-Client-Id" : self.client_id,
                      "X-Naver-Client-Secret" : self.client_secret}
    encText = urllib.parse.quote(text)
    URL = self.base_url + tag[0] + "/" + tag[1] + "?query=" + encText
    async with aiohttp.ClientSession(headers = headers) as session:
      async with session.get(URL) as response:
        rescode = response.status
        if(rescode==200):
          result = await response.json()
          return result
        else:
          raise ConverError(f"Error Code : {rescode}")

  async def t_request(
    self,
    tag : List[str],
    text : str
  ):
    headers : Dict = {"X-Naver-Client-Id" : self.client_id,
                      "X-Naver-Client-Secret" : self.client_secret,
                      "Content-Type" : "application/x-www-form-urlencoded"
                     }
    encText = urllib.parse.quote(text)
    URL = self.base_url + tag[0] + "/" + tag[1]
    params = tag[2] + encText
    async with aiohttp.ClientSession(headers = headers) as session:
      async with session.post(URL, data = params.encode('utf-8')) as response:
        rescode = response.status
        if(rescode==200):
          result = await response.json()
          return result
        else:
          raise ConverError(f"Error Code : {rescode}")

  async def get_result(self, tag: List[str], text):
    if tag[0] == "search":
      return await self.s_request(tag, text)
    else:
      return await self.t_request(tag, text)