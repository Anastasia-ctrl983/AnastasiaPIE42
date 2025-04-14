import random
import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Union

@dataclass
class BeeStats:
    """Статистика улья"""
    time: int
    queen_alive: bool
    workers: int
    honey_workers: int
    cleaner_workers: int
    drones: int
    larvae: int
    dead_bees: int
    honey_store: float
    idle_cleaners: int

class Bee(ABC):
    """Базовый класс для всех пчел"""
    def __init__(self, bee_id: int, birth_time: int):
        self._id = bee_id
        self._birth_time = birth_time
        self._weight = random.randint(100, 220) if not isinstance(self, Larva) else random.randint(5, 15)
        self._hunger = True
        self._alive = True
        
    @property
    def id(self) -> int: return self._id
    @property
    def birth_time(self) -> int: return self._birth_time
    @property
    def weight(self) -> int: return self._weight
    @property
    def is_hungry(self) -> bool: return self._hunger
    @property
    def is_alive(self) -> bool: return self._alive
        
    def die(self) -> None: self._alive = False
        
    @abstractmethod
    def consume_honey(self) -> float: pass
    @abstractmethod
    def check_lifespan(self, current_time: int) -> bool: pass

class BeeQueen(Bee):
    """Пчелиная матка"""
    def __init__(self, bee_id: int, birth_time: int):
        super().__init__(bee_id, birth_time)
        self._weight = random.randint(180, 220)
        self._lifespan = 365 * 3
        self._productivity = 2000
        self._consumption_rate = 0.08
        
    def consume_honey(self) -> float: return self.weight * self._consumption_rate
    def check_lifespan(self, current_time: int) -> bool: return (current_time - self.birth_time) >= self._lifespan
        
    def lay_eggs(self, honey_store: float) -> int:
        return int(self._productivity * min(1.0, honey_store / 10000) * random.uniform(0.9, 1.1))

class Drone(Bee):
    """Трутень"""
    def __init__(self, bee_id: int, birth_time: int):
        super().__init__(bee_id, birth_time)
        self._lifespan = 365
        self._fertility = random.randint(10, 20)
        self._consumption_rate = 0.05
        
    def consume_honey(self) -> float: return self.weight * self._consumption_rate
    def check_lifespan(self, current_time: int) -> bool: return (current_time - self.birth_time) >= self._lifespan
    def fertilize_eggs(self) -> int: return random.randint(self._fertility - 2, self._fertility + 2)

class WorkerBee(Bee):
    """Рабочая пчела"""
    WORKER_TYPES = ['honey', 'cleaner']
    
    def __init__(self, bee_id: int, birth_time: int, worker_type: str):
        super().__init__(bee_id, birth_time)
        self._lifespan = 365
        self._consumption_rate = 0.03
        self._type = worker_type if worker_type in self.WORKER_TYPES else 'honey'
        
    def consume_honey(self) -> float: return self.weight * self._consumption_rate
    def check_lifespan(self, current_time: int) -> bool: return (current_time - self.birth_time) >= self._lifespan
    def work(self) -> float: return random.uniform(0.5, 1.5) if self._type == 'honey' else 0

class Larva(Bee):
    """Личинка пчелы"""
    def __init__(self, bee_id: int, birth_time: int):
        super().__init__(bee_id, birth_time)
        self._development_time = 10
        self._consumption_rate = 0.02
        
    def consume_honey(self) -> float: return self._consumption_rate
    def check_lifespan(self, current_time: int) -> bool: return (current_time - self.birth_time) >= self._development_time
        
    def develop(self) -> Union[WorkerBee, Drone]:
        return WorkerBee(self.id, self.birth_time, random.choice(WorkerBee.WORKER_TYPES)) if random.random() < 0.8 else Drone(self.id, self.birth_time)

class Hive:
    """Улей с пчелами"""
    def __init__(self):
        self.queen = BeeQueen(1, 0)
        self.workers: List[WorkerBee] = [WorkerBee(i, 0, 'honey' if i < 12 else 'cleaner') for i in range(2, 15)]
        self.drones: List[Drone] = [Drone(i, 0) for i in range(15, 20)]
        self.larvae: List[Larva] = []
        self.dead_bees: List[Bee] = []
        self.honey_store = 10000
        self.time = 0
        self.total_dead_bees = 0
            
    def update(self) -> None:
        self.time += 1
        if self.queen.is_alive: 
            self.larvae.extend(Larva(len(self.larvae) + 1000, self.time) for _ in range(self.queen.lay_eggs(self.honey_store)))
        
        self._feed_bees()
        self._check_lifespans()
        self._develop_larvae()
        self.honey_store += sum(w.work() for w in self.workers if w._type == 'honey' and w.is_alive)
        self._clean_dead_bees()
        self._random_events()
        
    def _feed_bees(self) -> None:
        for bee in [self.queen] + self.drones + self.workers + self.larvae:
            if bee.is_alive:
                consumption = bee.consume_honey()
                if self.honey_store >= consumption:
                    self.honey_store -= consumption
                    bee._hunger = False
                else:
                    bee.die()
                    self._add_dead_bee(bee)
        
    def _check_lifespans(self) -> None:
        for bee in [self.queen] + self.drones + self.workers + self.larvae:
            if bee.is_alive and bee.check_lifespan(self.time):
                bee.die()
                self._add_dead_bee(bee)
        self._remove_dead_bees()
        
    def _add_dead_bee(self, bee: Bee) -> None:
        if bee not in self.dead_bees:
            self.dead_bees.append(bee)
            self.total_dead_bees += 1
        
    def _remove_dead_bees(self) -> None:
        self.drones = [d for d in self.drones if d.is_alive]
        self.workers = [w for w in self.workers if w.is_alive]
        self.larvae = [l for l in self.larvae if l.is_alive]
        
    def _develop_larvae(self) -> None:
        for larva in [l for l in self.larvae if l.check_lifespan(self.time)]:
            new_bee = larva.develop()
            self.workers.append(new_bee) if isinstance(new_bee, WorkerBee) else self.drones.append(new_bee)
            self.larvae.remove(larva)
        
    def _clean_dead_bees(self) -> None:
        cleaners = [w for w in self.workers if w._type == 'cleaner' and w.is_alive]
        self.dead_bees = self.dead_bees[min(len(cleaners), len(self.dead_bees)):]
        
    def _random_events(self) -> None:
        if random.random() < 0.05 and self.workers:
            for _ in range(random.randint(1, min(5, len(self.workers)))):
                bee = random.choice(self.workers)
                bee.die()
                self._add_dead_bee(bee)
                self.workers.remove(bee)
                
        if random.random() < 0.03 and self.honey_store > 0:
            self.honey_store -= random.uniform(0.1, 0.3) * self.honey_store
            
    def get_stats(self) -> BeeStats:
        alive_workers = [w for w in self.workers if w.is_alive]
        honey_workers = sum(1 for w in alive_workers if w._type == 'honey')
        cleaner_workers = len(alive_workers) - honey_workers
        
        return BeeStats(
            time=self.time,
            queen_alive=self.queen.is_alive,
            workers=len(alive_workers),
            honey_workers=honey_workers,
            cleaner_workers=cleaner_workers,
            drones=sum(1 for d in self.drones if d.is_alive),
            larvae=sum(1 for l in self.larvae if l.is_alive),
            dead_bees=self.total_dead_bees,
            honey_store=self.honey_store,
            idle_cleaners=max(0, cleaner_workers - len(self.dead_bees))
        )

class BeeSimulationUI:
    """Интерфейс симуляции"""
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Пчелиная семья - Симулятор")
        self.root.geometry("800x600")
        self.hive = Hive()
        self.simulation_running = False
        self.stats_history: List[BeeStats] = []
        self._setup_ui()
        
    def _setup_ui(self) -> None:
        # Панель управления
        self.btn_frame = tk.Frame(self.root)
        self.btn_frame.pack(pady=10)
        
        self.start_btn = tk.Button(self.btn_frame, text="Старт", command=self.start_simulation)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(self.btn_frame, text="Стоп", command=self.stop_simulation, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.step_btn = tk.Button(self.btn_frame, text="Шаг", command=self.step_simulation)
        self.step_btn.pack(side=tk.LEFT, padx=5)
        
        # Отображение статистики
        stats_frame = tk.Frame(self.root)
        stats_frame.pack(fill=tk.BOTH, expand=True)
        
        self.stats_tree = ttk.Treeview(stats_frame, columns=('value'), show='tree headings')
        self.stats_tree.heading('#0', text='Параметр')
        self.stats_tree.heading('value', text='Значение')
        self.stats_tree.column('#0', width=200)
        self.stats_tree.column('value', width=100)
        self.stats_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # График
        chart_frame = tk.Frame(self.root)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(chart_frame, bg='white', height=200)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self._update_stats_display()
        
    def start_simulation(self) -> None:
        """Запуск симуляции"""
        if not self.simulation_running:
            self.simulation_running = True
            self.start_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.NORMAL)
            self.step_btn.config(state=tk.DISABLED)
            self._run_simulation()
        
    def stop_simulation(self) -> None:
        """Остановка симуляции"""
        if self.simulation_running:
            self.simulation_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.step_btn.config(state=tk.NORMAL)
        
    def step_simulation(self) -> None:
        """Шаг симуляции"""
        if not self.simulation_running:
            self.hive.update()
            self._update_stats_display()
            self._update_chart()
        
    def _run_simulation(self) -> None:
        """Основной цикл симуляции"""
        if self.simulation_running:
            self.hive.update()
            self._update_stats_display()
            self._update_chart()
            self.root.after(500, self._run_simulation)
            
    def _update_stats_display(self) -> None:
        """Обновление отображения статистики"""
        stats = self.hive.get_stats()
        self.stats_history.append(stats)
        self.stats_tree.delete(*self.stats_tree.get_children())
        
        for param, value in [
            ('Время (дни)', stats.time),
            ('Матка', 'Жива' if stats.queen_alive else 'Мертва'),
            ('Всего рабочих пчел', stats.workers),
            ('Пчелы-добытчики', stats.honey_workers),
            ('Пчелы-уборщики', stats.cleaner_workers),
            ('Трутни', stats.drones),
            ('Личинки', stats.larvae),
            ('Мертвые пчелы (всего)', stats.dead_bees),
            ('Запасы меда', f"{stats.honey_store:.1f}"),
            ('Простаивающие уборщики', stats.idle_cleaners)
        ]:
            self.stats_tree.insert('', 'end', text=param, values=(value,))
        
    def _update_chart(self) -> None:
        """Обновление графика запасов меда"""
        self.canvas.delete('all')
        if len(self.stats_history) < 2: return
            
        honey_values = [s.honey_store for s in self.stats_history]
        max_h, min_h = max(honey_values or [1]), min(honey_values or [0])
        range_h = max(1, max_h - min_h)
        w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
        
        points = [(i/(len(honey_values)-1)*(w-20)+10, h-20-((v-min_h)/range_h)*(h-40)) for i,v in enumerate(honey_values)]
        for i in range(1, len(points)): 
            self.canvas.create_line(*points[i-1], *points[i], fill='blue', width=2)
        
        self.canvas.create_text(10, 10, anchor='nw', text=f"Мед: {honey_values[-1]:.1f}")
        self.canvas.create_text(w-10, h-10, anchor='se', text=f"День: {self.hive.time}")

def main():
    root = tk.Tk()
    app = BeeSimulationUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
