import logging

# Add logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Any
from urllib.parse import urlencode
import requests
import os

BaseAPIURL = "https://api.ghanapostgps.com/v2/PublicGPGPSAPI.aspx"

CorsByPass = [
    "Base-Url", "Client-IP", "Http-Url", "Proxy-Host", "Proxy-Url", "Real-Ip", "Redirect",
    "Referer", "Referrer", "Refferer", "Request-Uri", "Uri", "Url", "X-Client-Ip", "X-Forwarded-For",
    "Cf-Connecting-Ip", "X-Client-IP", "X-Custom-IP-Authorization", "X-Forward-For", "X-Forwarded-By",
    "X-Forwarded-By-Original", "X-Forwarded-For-Original", "X-Forwarded-For", "X-Forwarded-Host",
    "X-Forwarded-Server", "X-Forwarder-For", "X-HTTP-Destinationurl", "X-Http-Host-Override",
    "X-Original-Remote-Addr", "X-Original-Url", "X-Originating-IP", "X-Proxy-Url", "X-Remote-Addr",
    "X-Remote-IP", "X-Rewrite-Url", "X-True-IP", "Fastly-Client-Ip", "True-Client-Ip", "X-Cluster-Client-Ip",
    "X-Forwarded", "Forwarded-For", "Forwarded", "X-Real-Ip"
]

@dataclass
class Params:
    ApiURL: str
    Authorization: str
    AsaaseUser: str
    LanguageCode: str
    Language: str
    DeviceId: str
    AndroidCert: str
    AndroidPackage: str
    Country: str
    CountryName: str

def get_default_params() -> Params:
    """Loads parameters from environment variables."""
    return Params(
        ApiURL=os.getenv("GPGPS_API_URL", BaseAPIURL),
        Authorization=os.getenv("GPGPS_AUTHORIZATION"),
        AsaaseUser=os.getenv("GPGPS_ASAASE_USER"),
        LanguageCode=os.getenv("GPGPS_LANGUAGE_CODE"),
        Language=os.getenv("GPGPS_LANGUAGE"),
        DeviceId=os.getenv("GPGPS_DEVICE_ID"),
        AndroidCert=os.getenv("GPGPS_ANDROID_CERT"),
        AndroidPackage=os.getenv("GPGPS_ANDROID_PACKAGE"),
        Country=os.getenv("GPGPS_COUNTRY"),
        CountryName=os.getenv("GPGPS_COUNTRY_NAME")
    )

def get_data_request(values: Dict[str, Any]) -> str:
    """Encode form values into application/x-www-form-urlencoded string."""
    return urlencode(values)

def api_request(method: str, params: Params, payload: Optional[str]) -> str:
    """
    Make an HTTP request using the given method to params.ApiURL with the provided payload.
    payload should be the urlencoded string (from get_data_request).
    Returns response text (or exception text on error).
    """
    headers = {
        "Authorization": "Basic " + params.Authorization if params.Authorization else "",
        "LanguageCode": params.LanguageCode,
        "Language": params.Language,
        "CountryName": params.CountryName,
        "DeviceId": params.DeviceId,
        "X-Android-Cert": params.AndroidCert,
        "AsaaseUser": params.AsaaseUser,
        "Country": params.Country,
        "X-Android-Package": params.AndroidPackage,
        "Content-Type": "application/x-www-form-urlencoded",
    }

    for h in CorsByPass:
        headers[h] = "127.0.0.1"

    logger.info(f"Making {method} request to {params.ApiURL} with payload: {payload}")

    try:
        resp = requests.request(method=method.upper(), url=params.ApiURL, data=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.text
    except Exception as e:
        logger.error(f"Request failed: {e}")
        return str(e)

def get_location(code: str, defaults: Params) -> str:
    values = {
        "AsaaseLogs": "",
        "Action": "GetLocation",
        "GPSName": code,
    }
    data_request = get_data_request(values)
    return api_request("POST", defaults, data_request)

def get_address(latitude: str, longitude: str, defaults: Params) -> str:
    values = {
        "AsaaseLogs": "",
        "Action": "GetGPSName",
        "Lati": latitude,
        "Longi": longitude,
    }
    data_request = get_data_request(values)
    return api_request("POST", defaults, data_request)
