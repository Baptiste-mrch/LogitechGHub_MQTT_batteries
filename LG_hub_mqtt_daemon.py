#!/usr/bin/env python3
import subprocess
import json
import ast
import time
import threading
import paho.mqtt.client as mqtt
from LG_hub_devices_battery_info import get_data

# --- CONFIG ---
MQTT_BROKER = "mqtt.local"
MQTT_PORT = 1883
MQTT_USERNAME = "user"
MQTT_PASSWORD = "password"
MQTT_PREFIX = "logitech"
MQTT_CLIENT_ID = "LG_hub_mqtt_daemon_v2"

debugenabled = False

# --- MQTT client with sync publish confirmation ---
connected_event = threading.Event()
publish_events = {}  # mid -> threading.Event()

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("MQTT: connected to the broker")
        connected_event.set()
    else:
        print(f"MQTT: connexion failed rc={rc}")

def on_disconnect(client, userdata, rc, properties=None):
    print(f"MQTT: disconnected rc={rc}, attempt to reconnect...")
    connected_event.clear()

def on_publish(client, userdata, mid, reasonCode, properties):
    ev = publish_events.pop(mid, None)
    if ev:
        ev.set()

# create client (explicit protocol to avoid deprecation warning)
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, MQTT_CLIENT_ID)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_publish = on_publish

client.connect_async(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# Wait for connect
if not connected_event.wait(timeout=5):
    print("MQTT: Connection not found after 5 seconds — check broker/credentials")
    # we continue anyway; publishes will likely fail

def safe_parse_output(text):
    text = (text or "").strip()
    if not text:
        return {}
    # try JSON first
    try:
        return json.loads(text)
    except Exception:
        pass
    # fallback to literal_eval (safer than eval)
    try:
        return ast.literal_eval(text)
    except Exception as e:
        print("Parse output error:", e)
        return {}

def get_battery_info():
    """
    Execute LG_hub_devices_battery_info.py -> get_data() function and receive dictionary
    """
    data = get_data()
    if debugenabled:
        print("DEBUG - dict:", data)
    if not isinstance(data, dict):
        print("No dict return, we return {}")
        return {}
    return data

def slugify_device(name: str) -> str:
    # replace spaces by underscore and remove special character
    s = name.strip().replace(" ", "_")
    # keep only chars alnum, underscore and dash
    return "".join(c for c in s if c.isalnum() or c in ("_", "-"))

def publish_mqtt(device_name: str, info: dict, timeout_per_message: float = 5.0):
    """
    Publish every property of a device on a specific topic
    Wait for the broker confirmation.
    Exemple: logitech/PRO_X_WIRELESS/state
    """
    device_id = slugify_device(device_name)
    topic_base = f"{MQTT_PREFIX}/{device_id}"

    # DO NOT publish payloads on topic_base (this may hide subtopics in some clients)
    for key, value in info.items():
        topic = f"{topic_base}/{key}"
        # clean conversion of values
        if isinstance(value, bool):
            payload = "true" if value else "false"
        elif value is None:
            payload = "null"
        else:
            payload = str(value)

        # publish and wait for confirmation via on_publish
        rc, mid = client.publish(topic, payload, retain=True)
        if rc != mqtt.MQTT_ERR_SUCCESS:
            print(f"Initial publish error for {topic} rc={rc}")
            continue

        ev = threading.Event()
        publish_events[mid] = ev
        ok = ev.wait(timeout=timeout_per_message)
        if ok:
            if debugenabled:
                print(f"[PUB] Published on {topic}: {payload} (mid={mid})")
        else:
            print(f"Timeout publish for {topic} (mid={mid}) — verify the broker")
            # on retire l'event si toujours présent
            publish_events.pop(mid, None)

def ha_discovery(device_name: str, info: dict):
    """
    Publish the Home Assistant configuration via MQTT Discovery for a Logitech device.
    """

    device_id = slugify_device(device_name)
    topic_base = f"{MQTT_PREFIX}/{device_id}"

    # Define the manufacturer and model
    manufacturer = "Logitech"
    model = info['model']
    if info['model'] is None:
        model = ""

    # General device information
    device = {
        "identifiers": [device_id],
        "name": device_id,
        "manufacturer": "Logitech",
        "model": model
    }
    # --- 1. State (state) ---
    state_config = {
        "name": f"Etat",
        "state_topic": f"{topic_base}/state",
        "available": True,
        "unique_id": f"{device_id}_state",
        "device": device,
        "icon": "mdi:headphones"
    }
    # --- 2. Battery (pourcentage) ---
    battery_config = {
        "name": f"Batterie",
        "state_topic": f"{topic_base}/percentage",
        "unit_of_measurement": "%",
        "device_class": "battery",
        "unique_id": f"{device_id}_battery",
        "device": device
    }
    # --- 3. Charge (charging) ---
    charging_config = {
        "name": f"En charge",
        "state_topic": f"{topic_base}/charging",
        "device_class": "power",
        "payload_on": "true",
        "payload_off": "false",
        "unique_id": f"{device_id}_charging",
        "device": device
    }

    # Sending configurations to Home Assistant
    client.publish(f"homeassistant/sensor/{device_id}_state/config",
                json.dumps(state_config), retain=True)

    client.publish(f"homeassistant/sensor/{device_id}_battery/config",
                json.dumps(battery_config), retain=True)

    client.publish(f"homeassistant/binary_sensor/{device_id}_charging/config",
                json.dumps(charging_config), retain=True)

    # --- Envoi des états actuels ---
    client.publish(state_config['state_topic'], info['state'])
    client.publish(battery_config['state_topic'], info['percentage'])
    client.publish(charging_config['state_topic'], info['charging'])




def main():
    # --- Initial execution ---
    devices = get_battery_info()
    if not devices:
        print("No devices found, exit.")
        return

    for device_name, info in devices.items():
        if not isinstance(info, dict):
            print(f"Ignoré {device_name} because info is not a dict.")
            continue
        publish_mqtt(device_name, info) # Publish data
        ha_discovery(device_name, info) # Publish discovery

    time.sleep(0.2)

    # --- Loop ---
    while True:
        # Wait for MQTT connection
        if not connected_event.wait(timeout=10):
            print("MQTT: waiting for connection...")
            continue

        try:
            devices = get_battery_info()
            for device_name, info in devices.items():
                # If not connected -> Charging should be False. Prevent infinite charging status
                if info['state'] == "NOT_CONNECTED":
                    info['charging'] = False
                publish_mqtt(device_name, info)
            time.sleep(5)

        except Exception as e:
            print(f"[ERREUR] {e}, pause before retry...")
            time.sleep(5)

if __name__ == "__main__":
    main()