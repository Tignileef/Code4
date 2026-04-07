import random
import time
import json
import threading


class DummySensor:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

    def set_env(self):
        self.env_values['mars_base_internal_temperature'] = round(
            random.uniform(18, 30), 2
        )
        self.env_values['mars_base_external_temperature'] = round(
            random.uniform(0, 21), 2
        )
        self.env_values['mars_base_internal_humidity'] = round(
            random.uniform(50, 60), 2
        )
        self.env_values['mars_base_external_illuminance'] = round(
            random.uniform(500, 715), 2
        )
        self.env_values['mars_base_internal_co2'] = round(
            random.uniform(0.02, 0.10), 4
        )
        self.env_values['mars_base_internal_oxygen'] = round(
            random.uniform(4, 7), 2
        )

    def get_env(self):
        return self.env_values


ds = DummySensor()


class MissionComputer:
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }
        self.history = []
        self.is_running = True

    def stop_listener(self):
        while self.is_running:
            user_input = input().strip().lower()

            if user_input == 'stop':
                self.is_running = False
                print('Sytem stoped....')
                break

    def print_five_min_average(self):
        if len(self.history) < 5:
            return

        recent_history = self.history[-5:]
        average_values = {}

        for key in self.env_values:
            total = 0.0

            for item in recent_history:
                total += item[key]

            average_values[key] = round(total / len(recent_history), 4)

        print('\n=== 5분 평균 환경값 ===')
        print(json.dumps(average_values, indent = 4))
        print('\n=====================')

    def get_sensor_data(self):
        count = 0

        listener = threading.Thread(target = self.stop_listener, daemon = True)
        listener.start()

        print('환경 정보를 출력합니다. 종료하려면 stop 을 입력하세요.')

        try:
            while self.is_running:
                ds.set_env()
                sensor_values = ds.get_env()

                for key in self.env_values:
                    self.env_values[key] = sensor_values[key]

                self.history.append(dict(self.env_values))

                print(json.dumps(self.env_values, indent = 4))

                count += 1

                if count % 5 == 0:
                    self.print_five_min_average()

                for _ in range(1):
                    if not self.is_running:
                        break
                    time.sleep(1)

        except KeyboardInterrupt:
            self.is_running = False
            print('\nSytem stoped....')


RunComputer = MissionComputer()
RunComputer.get_sensor_data()