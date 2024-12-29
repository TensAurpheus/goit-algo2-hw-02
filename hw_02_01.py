from typing import List, Dict
from dataclasses import dataclass
from copy import copy


@dataclass
class PrintJob:
    id: str
    volume: float
    priority: int
    print_time: int


@dataclass
class PrinterConstraints:
    max_volume: float
    max_items: int


def optimize_printing(print_jobs: List[Dict], constraints: Dict) -> Dict:
    """
    Оптимізує чергу 3D-друку згідно з пріоритетами та обмеженнями принтера

    Args:
        print_jobs: Список завдань на друк
        constraints: Обмеження принтера

    Returns:
        Dict з порядком друку та загальним часом
    """
    
    constraints = PrinterConstraints(**constraints)

    print_jobs = [PrintJob(**job) for job in print_jobs]
    
    jobs_by_time = sorted(print_jobs, key=lambda x: x.print_time, reverse=True)
    jobs_by_priority = sorted(
        jobs_by_time, key=lambda x: x.priority)

    cur_queue = []
    queue = []
    total_time = 0
    job_times = []

    cur_constraints = copy(constraints)
    while len(jobs_by_priority) > 0: 
        cur_job = jobs_by_priority[0]
                
        if (cur_job.volume <= cur_constraints.max_volume) and (cur_constraints.max_items > 0):
            cur_queue.append(cur_job.id)
            job_times.append(cur_job.print_time)
            jobs_by_priority.pop(0)
            cur_constraints.max_volume -= cur_job.volume
            cur_constraints.max_items -= 1
            # print('current queue', cur_queue)
        else:
            queue.extend(cur_queue)
            total_time += max(job_times)
            job_times =[]
            cur_queue = []
            cur_constraints = copy(constraints)
            # print('new queue started')
            # print('total queue',queue)
        
        if len(jobs_by_priority) == 0:
            queue.extend(cur_queue)
            total_time += max(job_times)
       
    return {
        "print_order": queue,
        "total_time": total_time
    }

# Тестування


def test_printing_optimization():
    # Тест 1: Моделі однакового пріоритету
    test1_jobs = [
        {"id": "M1", "volume": 100, "priority": 1, "print_time": 120},
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},
        {"id": "M3", "volume": 120, "priority": 1, "print_time": 150}
    ]

    # Тест 2: Моделі різних пріоритетів
    test2_jobs = [
        {"id": "M1", "volume": 100, "priority": 2,
            "print_time": 120},  # лабораторна
        {"id": "M2", "volume": 150, "priority": 1, "print_time": 90},  # дипломна
        {"id": "M3", "volume": 120, "priority": 3,
            "print_time": 150}  # особистий проєкт
    ]

    # Тест 3: Перевищення обмежень об'єму
    test3_jobs = [
        {"id": "M1", "volume": 250, "priority": 1, "print_time": 180},
        {"id": "M2", "volume": 200, "priority": 1, "print_time": 150},
        {"id": "M3", "volume": 180, "priority": 2, "print_time": 120}
    ]

    constraints = {
        "max_volume": 300,
        "max_items": 2
    }

    print("Тест 1 (однаковий пріоритет):")
    result1 = optimize_printing(test1_jobs, constraints)
    print(f"Порядок друку: {result1['print_order']}")
    print(f"Загальний час: {result1['total_time']} хвилин")

    print("\\nТест 2 (різні пріоритети):")
    result2 = optimize_printing(test2_jobs, constraints)
    print(f"Порядок друку: {result2['print_order']}")
    print(f"Загальний час: {result2['total_time']} хвилин")

    print("\\nТест 3 (перевищення обмежень):")
    result3 = optimize_printing(test3_jobs, constraints)
    print(f"Порядок друку: {result3['print_order']}")
    print(f"Загальний час: {result3['total_time']} хвилин")


if __name__ == "__main__":
    test_printing_optimization()
