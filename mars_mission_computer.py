import random
import time
import json
import threading

class DummySensor:
    # 더미 센서 클래스 초기화
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

    # 환경 정보를 랜덤 값으로 설정하는 메소드
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

    # 현재 환경 정보를 반환하는 메소드
    def get_env(self):
        return self.env_values


# 문제 조건에 맞게 DummySensor 객체를 ds라는 이름으로 생성
ds = DummySensor()


class MissionComputer:
    # 미션 컴퓨터 클래스 초기화
    def __init__(self):
        self.env_values = {
            'mars_base_internal_temperature': 0.0,
            'mars_base_external_temperature': 0.0,
            'mars_base_internal_humidity': 0.0,
            'mars_base_external_illuminance': 0.0,
            'mars_base_internal_co2': 0.0,
            'mars_base_internal_oxygen': 0.0
        }

        # 측정 이력을 저장할 리스트
        self.history = []

        # 프로그램 실행 상태를 저장하는 변수
        # True이면 계속 실행, False이면 종료
        self.is_running = True

    # 사용자가 stop을 입력했는지 별도로 감시하는 메소드
    def stop_listener(self):
        # 프로그램이 실행 중인 동안 계속 입력을 받음
        while self.is_running:
            user_input = input().strip().lower()

            # 사용자가 stop을 입력하면 실행 중지
            if user_input == 'stop':
                self.is_running = False
                print('Sytem stoped....')
                break

    # 최근 5분 평균값을 계산하여 출력하는 메소드
    def print_five_min_average(self):
        if len(self.history) < 60:
            return

        recent_history = self.history[-60:]
        
        # 평균값을 저장할 사전
        average_values = {}

        # 각 환경 항목별 평균 계산
        for key in self.env_values:
            total = 0.0

            for item in recent_history:
                total += item[key]

            average_values[key] = round(total / len(recent_history), 4)

        # 5분 평균값을 JSON 형태로 출력
        print('\n=== 5분 평균 환경값 ===')
        print(json.dumps(average_values, indent = 4))

    # 센서 데이터를 계속 가져와 출력하는 메소드
    def get_sensor_data(self):
        count = 0

        # stop 입력 감시용 쓰레드 생성
        listener = threading.Thread(target = self.stop_listener, daemon = True)

        # 감시 쓰레드 시작
        listener.start()

        print('환경 정보를 출력합니다. 종료하려면 stop 을 입력하세요.')

        try:
            # 실행 상태가 True인 동안 계속 반복
            while self.is_running:
                # 더미 센서의 값을 새로 설정
                ds.set_env()

                # 센서의 현재 값을 가져옴
                sensor_values = ds.get_env()

                # 센서값을 미션 컴퓨터의 env_values에 복사
                for key in self.env_values:
                    self.env_values[key] = sensor_values[key]

                # 현재 값을 history에 복사해서 저장
                self.history.append(dict(self.env_values))

                # 현재 환경값을 JSON 형태로 출력
                print(json.dumps(self.env_values, indent = 4))

                count += 1

                if count % 60 == 0:
                    self.print_five_min_average()

                for _ in range(5):
                    # stop이 입력되면 대기 중이라도 바로 반복 종료
                    if not self.is_running:
                        break
                    time.sleep(1)

        # Ctrl + C를 눌러 강제 종료한 경우
        except KeyboardInterrupt:
            self.is_running = False
            print('\nSytem stoped....')


# 문제 조건에 맞게 MissionComputer 객체를 RunComputer라는 이름으로 생성
RunComputer = MissionComputer()
RunComputer.get_sensor_data()