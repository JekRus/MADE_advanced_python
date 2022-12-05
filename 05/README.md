# Homework 05: Profiling

## Отчет

### 1. Описание задания

Необходимо было придумать свои типы с несколькими атрибутами:
* класс с обычными атрибутами;
* класс со слотами;
* класс с атрибутами weakref.

Также необходимо было реализовать декоратор для профилирования.

### 2. Решение

Декоратор для профилирования реализован в profiling_decorator.py.
Классы для сравнения реализованы в stock_types.py. 
В compare_performace.py содержится скрипт для запуска анализа.
Скрипт принимает на вход один агрумент N - количество создаваемых объектов.

Запуск скрипта:
```commandline
python compare_performace.py 1_000_000
```
Для профилирования использования памяти:
```commandline
python -m memory_profiler compare_performace.py 1_000_000
```

### 3. Сравнение времени создания экземпляров, доступа/изменения/удаления атрибутов

Время доступа и изменения атрибутов практически одинаково во всех трех случаях.
Время удаления немного меньше для StocksSlots. 
Самое маленькое время создания у StockSimple, 
а самое большое у StockWeakref.


![Alt text](screenshots/timer.png?raw=true "Timer")


### 4. Профилирование вызовов функций

При вызове с профилировщиком результаты не сильно отличаются.
Однако, время для создания объектов StocksSlots сильно уменьшилось.
Возможно, эти флуктуации связаны с работой процессорного кэша.

![Alt text](screenshots/fcall_profiling_simple.png?raw=true "Timer")

![Alt text](screenshots/fcall_profiling_slots.png?raw=true "Timer")

![Alt text](screenshots/fcall_profiling_weakref.png?raw=true "Timer")

### 5. Профилирование памяти

При профилировании памяти не выявлено изменений при доступе/записи/удалении атрибутов.
При создании объектов в случае StocksSimple расходуется примерно 440 MiB, 
для StocksSlots - 240 MiB, для StocksWeakref - 520 MiB.
Самым экономным по памяти, как и ожидалось, оказался вариант со слотами.
Также в ходе проведения экспериментов замечены странные отрицательные значения 
в отчете профилировщика. Судя по issues из репозитория библиотеки, эта проблема известна довольно давно.

![Alt text](screenshots/mem_profiling_simple.png?raw=true "Timer")

![Alt text](screenshots/mem_profiling_slots.png?raw=true "Timer")

![Alt text](screenshots/mem_profiling_weakref.png?raw=true "Timer")
