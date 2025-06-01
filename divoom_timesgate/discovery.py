"""
Device discovery for Times Gate devices.
"""

import aiohttp
import asyncio
from typing import List, Dict, Any
import logging

from .exceptions import TimesGateError

logger = logging.getLogger(__name__)


async def discover_devices() -> List[Dict[str, Any]]:
    """
    Discover Times Gate devices on the local network.
    
    Returns:
        List of device information dictionaries with:
        - DeviceName: Name of the device
        - DeviceId: Unique device ID
        - DevicePrivateIP: IP address of the device
        - DeviceMac: MAC address of the device
    """
    url = "https://app.divoom-gz.com/Device/ReturnSameLANDevice"
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, timeout=aiohttp.ClientTimeout(total=10)) as response:
                data = await response.json()
                
                if data.get("ReturnCode") != 0:
                    raise TimesGateError(f"Discovery failed: {data.get('ReturnMessage', 'Unknown error')}")
                
                devices = data.get("DeviceList", [])
                
                # Filter for Times Gate devices
                times_gate_devices = [
                    device for device in devices 
                    if "timegate" in device.get("DeviceName", "").lower() or
                       "times gate" in device.get("DeviceName", "").lower()
                ]
                
                logger.info(f"Found {len(times_gate_devices)} Times Gate devices")
                
                return times_gate_devices if times_gate_devices else devices
                
        except aiohttp.ClientError as e:
            raise TimesGateError(f"Failed to discover devices: {str(e)}")
        except Exception as e:
            raise TimesGateError(f"Unexpected error during discovery: {str(e)}") 