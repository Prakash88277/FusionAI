import os
import json
import time
import requests
from typing import Optional
import logging

logger = logging.getLogger(__name__)

ZENROWS_API_KEY = os.getenv('ZENROWS_API_KEY')
ZENROWS_BASE_URL = os.getenv('ZENROWS_BASE_URL', 'https://api.zenrows.com/v1/')

class ZenRowsClient:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.api_key = api_key or ZENROWS_API_KEY
        self.base_url = (base_url or ZENROWS_BASE_URL).rstrip('/')
        
        if not self.api_key:
            logger.warning("ZenRows API key not found in environment variables")

    def fetch(self, url: str, js_render: bool = True, extra_params: dict = None, timeout: int = 30):
        """Fetch URL content using ZenRows API with exponential backoff"""
        
        if not self.api_key:
            raise RuntimeError("ZenRows API key not configured")
            
        params = {
            'apikey': self.api_key,
            'url': url,
            'js_render': 'true' if js_render else 'false'
        }
        if extra_params:
            params.update(extra_params)

        logger.info(f"ZenRows fetching: {url}")

        # exponential backoff for 429/5xx
        for attempt in range(3):
            try:
                resp = requests.get(self.base_url, params=params, timeout=timeout)
                resp.raise_for_status()
                
                logger.info(f"ZenRows fetch successful for {url} (attempt {attempt + 1})")
                
                try:
                    return resp.json()
                except ValueError:
                    return resp.text
                    
            except requests.HTTPError as e:
                status = getattr(e.response, 'status_code', None)
                logger.warning(f"ZenRows HTTP error {status} for {url} (attempt {attempt + 1})")
                
                if status in (429, 500, 502, 503, 504):
                    sleep_time = 2 ** attempt
                    logger.info(f"Retrying in {sleep_time} seconds...")
                    time.sleep(sleep_time)
                    continue
                raise
            except Exception as e:
                logger.error(f"ZenRows fetch error for {url}: {str(e)}")
                if attempt == 2:  # last attempt
                    raise
                time.sleep(2 ** attempt)
                
        raise RuntimeError('ZenRows fetch failed after retries')
