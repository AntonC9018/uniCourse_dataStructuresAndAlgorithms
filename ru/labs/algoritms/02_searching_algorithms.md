# Лабораторная работа 2

Тема: **Алгоритмы поиска**.

Цели лабы:
- Создать тип (структуру), которую будете использовать в дальнейших работах;
- Написать код сериализации и десериализации в формат CSV;
- Программирование методов поиска в неотсортированных массивах (линейный, бинарное дерево поиска)
- Программирование методов поиска в отсортированных массивах (бинарный, и один другой на выбор)
- Запись времени выполнения алгоритмов в зависимости от размера массива и расположения элементов
  (в сортированном порядке, в порядке обратным этому, в слуайном порядке).

## Система подсчета времени выполнения алгоритмов

Поскольку в дальнейшем нужно будет практически анализировать скорость алгоритмов
в разных ситуациях, нужно создать систему, которая позволит вам совершить эти проверки.

Подходов может быть много, самый примитивный (без использования полиморфизма) наверное будет
заключаться в использовании нескольких вложенных циклов и switch.
Примерный outline:

```cpp
std::array<std::vector<Record>> allData;
allData.resize(DATA_COUNT);

std::array<std::string_view, DATA_COUNT> fileNames =
{
    { "small.csv" },
    { "medium.csv" },
    { "large.csv" },
};

bool hasErrors = false;
for (int di; di < DATA_COUNT; di++)
{
    std::string_view fileName = fileNames[di];
    ifstream file{fileName};
    bool success = parseRecordsFromCsv(file, allData[di]);
    if (!success)
    {
        // You might return more context here,
        // depends on the implementation of the csv parser.
        std::cout << "Could not parse file " << fileName;
        hasErrors = true;
    }
}

if (hasErrors)
{
    return 1;
}

std::vector<Record> items;
for (int ai = 0; ai < ALGORITHM_COUNT; ai++)
{
    for (int di; di < DATA_COUNT; di++)
    {
        const std::vector<Record>& sortedData = allData[di];
        items.resize(sortedData.size());

        for (int si = 0; si < SHUFFLE_COUNT; si++)
        {
            time_t totalTime = 0;
            for (int ei = 0; ei < EXPERIMENT_COUNT; ei++)
            {
                switch (si)
                {
                    // Sorted array
                    case 0:
                    {
                        // Copy from sortedData into items
                        break;
                    }

                    // Unsorted array
                    case 1:
                    {
                        // Copy from sortedData in some random order
                        break;
                    }

                    // Unsorted
                    case 2:
                    {
                        // Copy in reverse order
                        break;
                    }
                }

                time_t experimentStartTime = ...;

                switch (ai)
                {
                    // Linear search
                    case 0:
                    {
                        // ...
                        break;
                    }

                    // Binary search tree
                    case 1:
                    {
                        // ...
                        break;
                    }
                }

                time_t experimentEndTime = ...;
                totalTime += experimentEndTime - experimentStartTime;
            }

            // Store the time for this type of shuffle
            // ...
        }

        // Store the times for each shuffle for this data size
    }

    {
        // Print the total times for this algorithm
        std::array<std::string_view, ALGORITHM_COUNT> algorithmNames =
        {
            { "Linear" },
            { "Binary Search Tree" },
        };
        std::string_view algorithmName = algorithmNames[ai];

        std::cout << "Average time for the algorithm " << algorithmName << ": ";
        // ...
    }
}
```

Однако наверняка заметите при программировании,
что вытащить общий код записи времени сложно.
Это лучше решить через полиморфизм (передавать функцию алгоритма параметром).
Про полиморфизм почитайте [здесь](../05a_programming_fundamentals/11_polymorphism.md),
но надо знать и про [темплейты](../05a_programming_fundamentals/07_template.md),
и про указатели на функции (не особо глубоко, просто понимать базовый синтаксис).


## Программирование алгоритмов

Напишите код для следующих алгоритмов:
- Линейный поиск
- Бинарное дерево посика
- Бинарный поиск
- Один алгоритм поиска в отсортированных массивах на выбор

Протестируйте алгоритмы на разных размерностях массива, и разном расположении элементов (там где применимо):
- Отсортированный массив (меньший к большему)
- Обратно отсортированный массив (больший к меньшему)
- Случайный порядок элементов

Проводите тестирование несколько раз (5+), и усредняйте результаты.

Можете проводить все тесты в одной программе, или каждый тест в своей,
а можете использовать аргументы командной строки для выбора теста
(найдите как с этим работать, если решите пойти этим путем).

Для работы со временем используйте библиотеки `std::chrono` или `ctime`.
Вместо всего этого можете также использовать консольные команды
`Measure-Command` в PowerShell (Windows), или `time` в bash (Linux/Mac/WSL).

Проанализируйте полученные результаты:
- Сравните как затраченное время зависит от количества
  и расположения элементов для каждого из алгоритмов.
- Сравните практическую сложность каждого из алгоритмов
  (затраченное время в зависимости от количества элементов) с теоретической.
- Объясните в каких ситуациях стоит применить тот или иной алгоритм,
  и объясните почему он оптимальней других для этих задач.

