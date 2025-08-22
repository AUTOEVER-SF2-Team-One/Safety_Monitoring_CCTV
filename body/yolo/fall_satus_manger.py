class FallStatusManager:
    """
    각 사람의 넘어짐 상태를 추적하고 관리하는 클래스.
    - 임계값 기반으로 최종 넘어짐 여부를 판단합니다.
    - 화면에서 사라진 사람의 데이터를 자동으로 정리합니다.
    """
    def __init__(self, threshold: int):
        """
        초기화 메서드
        Args:
            threshold (int): 최종 넘어짐으로 판단하기까지 필요한 프레임 수
        """
        self.threshold = threshold
        self.person_counters = {}  # {person_idx: counter} 형태의 딕셔너리

    def update_status(self, person_predictions: list) -> bool:
        """
        현재 프레임의 예측 결과를 받아 상태를 업데이트하고 최종 알람 여부를 반환합니다.

        Args:
            person_predictions (list): [(person_idx, is_fallen_bool), ...] 형태의 현재 프레임 예측 결과 리스트

        Returns:
            bool: 최종 넘어짐 경보를 울려야 하는지 여부
        """
        final_alarm = False
        
        # --- 1. 현재 프레임에 감지된 사람들의 인덱스 집합 생성 ---
        current_person_indices = {p[0] for p in person_predictions}

        # --- 2. 카운터 업데이트 ---
        for person_idx, is_fallen in person_predictions:
            if is_fallen:
                # 넘어짐 상태: 카운터 증가
                self.person_counters[person_idx] = self.person_counters.get(person_idx, 0) + 1
            else:
                # 정상 상태: 카운터 리셋
                self.person_counters[person_idx] = 0

        # --- 3. 화면에서 사라진 사람의 데이터 정리 ---
        # to_delete = [idx for idx in self.person_counters if idx not in current_person_indices]
        # for idx in to_delete:
        #     del self.person_counters[idx]
        
        # 딕셔너리 컴프리헨션을 사용한 더 간결한 정리 방법
        self.person_counters = {idx: count for idx, count in self.person_counters.items() if idx in current_person_indices}

        # --- 4. 최종 알람 여부 확인 ---
        for counter in self.person_counters.values():
            if counter >= self.threshold:
                final_alarm = True
                break  # 한 명이라도 조건 만족 시 즉시 확인 종료
        
        return final_alarm