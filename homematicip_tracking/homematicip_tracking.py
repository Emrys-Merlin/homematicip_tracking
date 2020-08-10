"""Main module."""
import homematicip
from homematicip.home import Home
import pandas as pd
from time import sleep
from prometheus_client import Gauge
from requests.exceptions import ConnectionError


def filter_thermostats(device):
    tp = device.modelType
    is_thermostat = 'TH' in tp
    is_valve = 'TRV' in tp
    return is_valve or is_thermostat


class HomematiIP():
    def __init__(self, config_file):
        self.config = homematicip.load_config_file(config_file)

        self.home = Home()

        self.home.set_auth_token(self.config.auth_token)
        self.home.init(self.config.access_point)

        self.temperature = Gauge('temperature_gauge_c',
                                 'HomematicIP smart home temperature sensor reads',
                                 ['room', 'device_name', 'device_type'])
        self.humidity = Gauge('humidity_gauge_percent',
                              'HomematicIP smart home humidity sensor reads',
                              ['room', 'device_name', 'device_type'])

    def poll_thermostats(self):
        while True:
            try:
                self.home.get_current_state()
                break
            except ConnectionError:
                print('Connection timeout. Retry.')
                sleep(10)


        groups = self.home.groups
        df = []
        for group in filter(lambda grp: grp.groupType == 'META', groups):
            for device in filter(filter_thermostats, group.devices):
                row = pd.Series({
                    'group': group.label,
                    'device_name': device.label,
                    'device_type': device.modelType,
                    })

                if 'TH' in device.modelType:
                    row['device_temperature'] = device.actualTemperature
                    row['device_humidity'] = device.humidity
                    self.temperature.labels(
                        room=group.label,
                        device_name=device.label,
                        device_type=device.modelType,
                    ).set(device.actualTemperature)
                    self.humidity.labels(
                        room=group.label,
                        device_name=device.label,
                        device_type=device.modelType,
                    ).set(device.humidity)

                if 'TRV' in device.modelType:
                    row['device_temperature'] = device.valveActualTemperature
                    self.temperature.labels(
                        room=group.label,
                        device_name=device.label,
                        device_type=device.modelType,
                    ).set(device.valveActualTemperature)

                df.append(row)

        return pd.concat(df, axis=1, ignore_index=True).T
