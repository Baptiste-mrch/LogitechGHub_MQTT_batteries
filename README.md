# LogitechGHub_MQTT_batteries
Retrieve batteries status of Logtech devices through G Hub into MQTT (useful in HomeAssistant)

## Goal of the project
I recently got a wireless Logitech headset from which I want to automate some actions based on it's data. After some research, it appears that the G Hub app don't have any public API from which we can talk to.
I found this repo [andyvorld/LGSTrayBattery](https://github.com/andyvorld/LGSTrayBattery) that seems to comunicate with the G Hub app and display the battery level on the Windows system tray (using private / non-documented API). After a lot of tinkering and vibe coding, I made this light version with no UI.
It expose batteries data of multiple devices from Logitech G Hub directly on Home Assistant with the help of MQTT so it can be multi-platform.

## Setup
In the top of the `LG_hub_mqtt_daemon.py`, there are variables for the MQTT credentials. Put yours and it should be sending data to the topic `logitech/%DEVICE%/`.

To make this script run on startup, make a bat file that execute the `LG_hub_mqtt_daemon.py` script, and put it on your startup folder (`shell:startup`). It's also possible to create an executable using PyInstaller.

## Structure of the project
I'm certainly not a developper, this project was only possible with the help of the repo mentionned above and generative AI. If you have any suggesion or question regarding the code, feel free.

I constructed this project around 2 mains script : `LG_hub_devices_battery_info.py` and `LG_hub_mqtt_daemon.py`
### - LG_hub_devices_battery_info.py
This code talk to the private G Hub api using WebSocket connection. It has 2 main functions :
<details><summary>get_all_devices_info() : retrieve all the data from devices in a JSON format (example with Pro X Wireless & G502 Hero inside G Hub)</summary>
  
  ```json
  {
   "id":"dev00000002",
   "name":"PRO X WIRELESS",
   "type":"HEADSET",
   "capabilities":{
      "audio":{
         "hasDts":false,
         "hasDolby":false,
         "hasDtsHx2e":true,
         "hasBlueVoice1":true,
         "hasBlueVoice2":false,
         "hasLogivoice":false,
         "hasSamplerApo":false,
         "hasAutomaticGainControl":false,
         "hasMicrophoneVolumeFeatures":false,
         "syncMicSettingsCardGainWithSystem":false,
         "hasProEq":false,
         "hasOnboardEq":false,
         "hasOnboardProEq":false,
         "hasCenturionEq":false,
         "hasCenturionOnboardEq":false,
         "hasLightspeedAux":false,
         "hasCenturionVolumeInAcoustics":false,
         "hasAudioMixingMatrix":false,
         "hasMicrophoneTest":false,
         "hasEq":true,
         "hasAcoustics":true,
         "hasHardwareNoiseReduction":false,
         "hasCenturionOnboardNoiseReduction":false,
         "hasHeadsetTones":false,
         "hasSidetoneInSettings":false,
         "hasCenturionVolumeInSettings":false,
         "hasNoiseExposureInSettings":false,
         "hasHidMic":false,
         "hasDenoiser":false,
         "hasHeadphoneJack":false,
         "micLightingOptOut":false,
         "hasMicFunctionalLighting":false,
         "hasLatchingMuteButton":false,
         "hasMicLedSupport":false,
         "hasMicrophoneSettings":false,
         "hasMicrophonePreset":false
      },
      "sleepTimer":false,
      "mstateSupport":{
         "count":1,
         "timeOut":0
      },
      "fnInversion":false,
      "presentSplashScreen":false,
      "customizableColor":false,
      "wirelessReportRate":false,
      "hybridEngine":false,
      "advancedSleepTimer":false,
      "angleSnapping":false,
      "excludeGShift":false,
      "hostRemovalSupport":false,
      "hostInfos":false,
      "gkeyLayout":"INVALID_GKEY_LAYOUT",
      "hasBatteryStatus":true,
      "powerOffTimer":true,
      "requiresBackupForDfu":false,
      "unifiedBattery":false,
      "dpiLighting":false,
      "hasGlobalDamping":false,
      "nonInteractive":false,
      "chargepadCompatible":false,
      "individuality":false,
      "defaultSlotFormat":"INVALID_FORMAT",
      "fnToggle":false,
      "isFullHidppWheel":false,
      "hasConfigurationProfiles":false,
      "disableCenterSpring":false,
      "hasOnboardDeviceName":false,
      "systemTraySupport":false,
      "cidBasedGameModeSupport":false,
      "depotNotRequired":false,
      "ledBrightness":false,
      "autoSleep":false,
      "hasFactoryReset":false,
      "disableLightingViewMenu":false,
      "dpiVersion":0,
      "hasWiredReportRate":false,
      "keyboardSize":"UNKNOWN",
      "uiThemeVersion":0,
      "deviceNameMaxLength":0,
      "hasBatteryEcoMode":false,
      "hasTotalUsageTime":false,
      "iprofileDatasyncSupport":false,
      "modeMatchingAlgorithm":"DEFAULT",
      "useRealSoc":false,
      "hasEuPowerModeControl":false,
      "hasBunnyHoppingSupport":false,
      "hasSpatialSound":false,
      "hasPerformanceReportRate":false,
      "hasRename":false,
      "deviceSettingsVersion":0,
      "hasOnboardEditSupport":false
   },
   "state":"NOT_CONNECTED",
   "activeInterfaces":[],
   "battery_percentage":98,
   "charging":false,
   "connected":"None"
},
{
   "id":"dev00000003",
   "name":"G502 HERO",
   "type":"MOUSE",
   "capabilities":{
      "lightingSupport":{
         "deviceCategory":"MOUSE_RGB_ZONAL",
         "typeMap":{
            "ZONE_BRANDING":"LOGO",
            "ZONE_PRIMARY":"PRIMARY"
         },
         "zones":[
            {
               "zoneType":"ZONE_PRIMARY",
               "supportedEffects":[
                  {
                     "id":"OFF",
                     "syncable":true,
                     "fixedIntensity":false,
                     "signature":false,
                     "inactivityOnly":false,
                     "name":"",
                     "fixedRate":false,
                     "fixedSaturation":false,
                     "derivativeOverrides":{}
                  },
                  {
                     "id":"FIXED",
                     "syncable":true,
                     "fixedIntensity":false,
                     "signature":false,
                     "inactivityOnly":false,
                     "name":"",
                     "fixedRate":false,
                     "fixedSaturation":false,
                     "derivativeOverrides":{}
                  },
                  {
                     "id":"CYCLE",
                     "syncable":true,
                     "fixedIntensity":false,
                     "signature":false,
                     "inactivityOnly":false,
                     "name":"",
                     "fixedRate":false,
                     "fixedSaturation":false,
                     "derivativeOverrides":{}
                  },
                  {
                     "id":"BREATHING",
                     "syncable":true,
                     "fixedIntensity":false,
                     "signature":false,
                     "inactivityOnly":false,
                     "name":"",
                     "fixedRate":false,
                     "fixedSaturation":false,
                     "derivativeOverrides":{}
                  }
               ],
               "onboardCluster":"CLUSTER_DEFAULT"
            },
            {
               "zoneType":"ZONE_BRANDING",
               "supportedEffects":[
                  {
                     "id":"OFF",
                     "syncable":true,
                     "fixedIntensity":false,
                     "signature":false,
                     "inactivityOnly":false,
                     "name":"",
                     "fixedRate":false,
                     "fixedSaturation":false,
                     "derivativeOverrides":{}
                  },
                  {
                     "id":"FIXED",
                     "syncable":true,
                     "fixedIntensity":false,
                     "signature":false,
                     "inactivityOnly":false,
                     "name":"",
                     "fixedRate":false,
                     "fixedSaturation":false,
                     "derivativeOverrides":{}
                  },
                  {
                     "id":"CYCLE",
                     "syncable":true,
                     "fixedIntensity":false,
                     "signature":false,
                     "inactivityOnly":false,
                     "name":"",
                     "fixedRate":false,
                     "fixedSaturation":false,
                     "derivativeOverrides":{}
                  },
                  {
                     "id":"BREATHING",
                     "syncable":true,
                     "fixedIntensity":false,
                     "signature":false,
                     "inactivityOnly":false,
                     "name":"",
                     "fixedRate":false,
                     "fixedSaturation":false,
                     "derivativeOverrides":{}
                  }
               ],
               "onboardCluster":"CLUSTER_DEFAULT"
            }
         ],
         "isMonochrome":false,
         "isPerKey":false,
         "brightnessLevels":[],
         "powerSavingEffect":false,
         "lowBatteryEffect":false,
         "brightnessPercentage":false,
         "gamma":false,
         "firmwareOnly":false,
         "offRamp":false,
         "activeDimming":false,
         "hasPositionalEffect":false,
         "hasPastelPalette":false,
         "hasRingLeds":false,
         "hasMasterSwitch":false,
         "needKeepAliveSignal":false,
         "hasPcStateSync":false,
         "btSoftwareEffects":false,
         "overallBrightness":false,
         "combinedLightingSettings":false,
         "hasLowSmoothSpeed":false,
         "defaultSmoothSpeed":0,
         "hasLimitedLowBatteryEffects":false,
         "hasReportRateLimitedLighting":false,
         "useFwInactivityLighting":false,
         "hasLightBar":false
      },
      "sleepTimer":false,
      "mstateSupport":{
         "count":1,
         "timeOut":0
      },
      "fnInversion":false,
      "presentSplashScreen":false,
      "customizableColor":false,
      "wirelessReportRate":false,
      "hybridEngine":false,
      "advancedSleepTimer":false,
      "onboardProfiles":{
         "disableProfileNaming":false,
         "profilesAlwaysActive":false,
         "supportsOnboardMode":true,
         "useFileSystem":false,
         "prioritizeSoftwareDefaults":false
      },
      "angleSnapping":false,
      "excludeGShift":false,
      "hostRemovalSupport":false,
      "hostInfos":false,
      "gkeyLayout":"INVALID_GKEY_LAYOUT",
      "hasBatteryStatus":false,
      "powerOffTimer":false,
      "requiresBackupForDfu":true,
      "unifiedBattery":false,
      "dpiLighting":true,
      "hasGlobalDamping":false,
      "nonInteractive":false,
      "chargepadCompatible":false,
      "individuality":false,
      "defaultSlotFormat":"INVALID_FORMAT",
      "fnToggle":false,
      "isFullHidppWheel":false,
      "hasConfigurationProfiles":false,
      "disableCenterSpring":false,
      "hasOnboardDeviceName":false,
      "systemTraySupport":false,
      "cidBasedGameModeSupport":false,
      "depotNotRequired":false,
      "ledBrightness":false,
      "autoSleep":false,
      "hasFactoryReset":false,
      "disableLightingViewMenu":false,
      "dpiVersion":0,
      "hasWiredReportRate":false,
      "keyboardSize":"UNKNOWN",
      "uiThemeVersion":0,
      "deviceNameMaxLength":0,
      "hasBatteryEcoMode":false,
      "hasTotalUsageTime":false,
      "iprofileDatasyncSupport":false,
      "modeMatchingAlgorithm":"DEFAULT",
      "useRealSoc":false,
      "hasEuPowerModeControl":false,
      "hasBunnyHoppingSupport":false,
      "hasSpatialSound":false,
      "hasPerformanceReportRate":false,
      "hasRename":false,
      "deviceSettingsVersion":0,
      "hasOnboardEditSupport":false
   },
   "state":"ACTIVE",
   "activeInterfaces":[
      {
         "type":"DEVIO",
         "id":"046d_c08b",
         "pid":49291,
         "modelId":0,
         "extendedModel":0,
         "serialNumber":"875644685",
         "path":"usb\\vid_046d&pid_c08b&mi_01\\9&1dd452ae&0&0001",
         "containerId":"2123d630-d100-501d-9b76-7c04d4994b82",
         "deviceType":"MOUSE",
         "deviceName":"G502 HERO Gaming Mouse",
         "keyboardLayout":"INVALID_LAYOUT",
         "firmwareVersion":"127.3.10",
         "firmwareName":"U127",
         "firmwareRevision":3,
         "hardwareRevision":0,
         "unitId":"875644685",
         "fwEntities":{},
         "connectionType":"USB",
         "hasOnboardMode":true,
         "parentPath":"",
         "hashedSerialNumber":"",
         "hashedUnitId":"fef19ca5686bf0c8ee4d07953d8c42238aeea5c28de69661b7d25a3401a5b389"
      }
   ]
}
  ```

</details>
<details><summary>get_data() : retreive only the battery information (formated Python dict returned with only Pro X Wireless because it's the only battery-powered device)</summary>
  
  ```python
{'PRO X WIRELESS': {'model': None, 'state': 'NOT_CONNECTED', 'percentage': 98, 'charging': False}}
  ```
</details>

### - LG_hub_mqtt_daemon.py
This one is in charge of connecting to the MQTT broker, call the get_data() function every 5 seconds, and publish the result to the MQTT queue. It also create and publish discovery packet for Home Assistant to automatically add devices in MQTT integration.

## Result
Device in the MQTT queue (MQTT explorer)

<img width="214" height="107" alt="image" src="https://github.com/user-attachments/assets/8d1a438c-57bd-4ed3-b6cd-cd612ffcb8a7" />

Device automatically discovered in Home Assistant

<img width="1617" height="598" alt="image" src="https://github.com/user-attachments/assets/71dc8ba4-24c4-4c58-9e69-218a8c74f053" />

## Bonus - Automation to change Windows audio source when headset is connected/disconnected
⚠️ You need to have setup HASS.Agent on your Windows

In HASS.Agent app, create 2 commands for switching audio source with the name of your audio sources. These should be in entity type "button"

<img width="850" height="83" alt="image" src="https://github.com/user-attachments/assets/e92938fc-9538-4d14-895e-c030ceb35d57" />

Paste and customize this automation

```yaml
alias: Headset audio source auto switcher
description: ""
triggers:
  - trigger: state
    entity_id:
      - sensor.pro_x_wireless_state
    to: ACTIVE
    id: ACTIVE
    from: NOT_CONNECTED
  - trigger: state
    entity_id:
      - sensor.pro_x_wireless_state
    to: NOT_CONNECTED
    id: NOT_CONNECTED
    from: ACTIVE
actions:
  - choose:
      - conditions:
          - condition: trigger
            id:
              - ACTIVE
        sequence:
          - action: button.press
            metadata: {}
            data: {}
            target:
              entity_id: button.<YOUR_PC>_sortie_audio_casque
      - conditions:
          - condition: trigger
            id:
              - NOT_CONNECTED
        sequence:
          - action: button.press
            metadata: {}
            data: {}
            target:
              entity_id: button.<YOUR_PC>_sortie_audio_hp
mode: single
```

## Acknowledgment
Thanks to @andyvorld for the reverse enginnering process that helps me understand how to retreive G Hub information

Thanks to ChatGPT since I'm really not a developer
