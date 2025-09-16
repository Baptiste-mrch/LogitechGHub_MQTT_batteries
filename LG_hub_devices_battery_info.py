#!/usr/bin/env python3
"""
headset_info.py - Retrieves device information via G Hub WebSocket.
"""

import json
import time
from websocket import create_connection, WebSocketTimeoutException, WebSocketException, WebSocketBadStatusException

WS_URI = "ws://localhost:9010"
CONNECT_TIMEOUT = 3
RECV_TIMEOUT = 1.0
OVERALL_TIMEOUT = 8.0
ORIGINS_TO_TRY = ["file://", "file:///", "file://localhost", "http://localhost", "https://localhost", "null", ""]

def recv_until_has(check_fn, ws, overall_timeout=OVERALL_TIMEOUT, recv_timeout=RECV_TIMEOUT, debug=False):
    start = time.time()
    ws.settimeout(recv_timeout)
    while time.time() - start < overall_timeout:
        try:
            raw = ws.recv()
            if debug:
                print("<<< RAW:", raw)
            try:
                msg = json.loads(raw)
            except Exception:
                continue
            try:
                if check_fn(msg):
                    return msg
            except Exception:
                continue
        except WebSocketTimeoutException:
            continue
        except WebSocketException:
            break
    return None

def try_connect_with_origins(origins, debug=False):
    last_exc = None
    headers_common = ["Pragma: no-cache", "Cache-Control: no-cache"]
    for origin in origins:
        try:
            ws = create_connection(
                WS_URI,
                origin=origin if origin != "" else None,
                header=headers_common,
                subprotocols=["json"],
                timeout=CONNECT_TIMEOUT
            )
            return ws, origin
        except Exception as e:
            last_exc = e
    raise last_exc


def get_all_devices_info(debug=False):
    try:
        ws, used_origin = try_connect_with_origins(ORIGINS_TO_TRY, debug=debug)
    except Exception as e:
        return None, str(e)

    try:
        ws.send(json.dumps({"msgId": "", "verb": "GET", "path": "/devices/list"}))

        def has_device_infos(msg):
            return isinstance(msg, dict) and msg.get("payload") and isinstance(msg["payload"].get("deviceInfos"), list)

        devices_msg = recv_until_has(has_device_infos, ws, overall_timeout=OVERALL_TIMEOUT, recv_timeout=RECV_TIMEOUT, debug=debug)
        if not devices_msg:
            return None, "No deviceInfos received (timeout)."

        device_infos = devices_msg["payload"]["deviceInfos"]
        devices_data = []

        for dev in device_infos:
            if not isinstance(dev, dict):
                continue

            device_data = {
                "id": dev.get("id"),
                "name": dev.get("displayName") or dev.get("extendedDisplayName"),
                "type": dev.get("deviceType"),
                "capabilities": dev.get("capabilities", {}),
                "state": dev.get("state"),
                "activeInterfaces": dev.get("activeInterfaces"),
            }

            # Recover battery if available
            if device_data["capabilities"].get("hasBatteryStatus"):
                ws.send(json.dumps({"msgId": "", "verb": "GET", "path": f"/battery/{device_data['id']}/state"}))

                def is_battery_msg(msg):
                    payload = msg.get("payload")
                    return isinstance(payload, dict) and payload.get("deviceId") == device_data['id']

                batt_msg = recv_until_has(is_battery_msg, ws, overall_timeout=OVERALL_TIMEOUT, recv_timeout=RECV_TIMEOUT, debug=debug)
                if batt_msg:
                    payload = batt_msg.get("payload", {})
                    device_data.update({
                        "battery_percentage": payload.get("percentage"),
                        "charging": payload.get("charging"),
                        "connected": payload.get("connected", payload.get("online"))
                    })
            devices_data.append(device_data)

        return devices_data, None

    finally:
        try:
            ws.close()
        except Exception:
            pass


def get_data(debug=False):
    devices, error = get_all_devices_info(debug=False)
    if error:
        print("Erreur:", error)
    else:
        # Extracting devices with hasBatteryStatus set to True
        battery_devices = {}
        for dev in devices:
            capabilities = dev.get('capabilities', {})
            has_battery = capabilities.get('hasBatteryStatus', False)
            if has_battery:
                name = dev.get('name')
                
                # Retrieve the template from activeInterfaces
                model = None
                active_interfaces = dev.get('activeInterfaces', [])
                if isinstance(active_interfaces, list) and len(active_interfaces) > 0:
                    model = active_interfaces[0].get('deviceName')

                state = dev.get('state')
                battery_percentage = dev.get('battery_percentage')
                charging = dev.get('charging')
                battery_devices[name] = {
                'model': model,
                'state': state,
                'percentage': battery_percentage,
                'charging': charging
                }

        # Result
        return battery_devices