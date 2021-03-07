# Использование

Attention: Если вы работаете на Windows, cmd нужно запустить от имени администратора

1. `$ python -m pip install git+https://gitlab.com/ekon-university/8_sem_labs/pis/battleground`
1. `$ cs-battleground create-app APP-NAME`  
   или  
   `$ cs-battleground create-app APP-NAME --no-comments`
   чтобы получить проект без комментариев

В рабочей директории будет создан шаблонный проект:

```
├── controller.py
├── robot.ttm
├── scene.ttt
└── wrappers
    ├── __init__.py
    ├── joint.py
    └── sim_object.py
```

Для того, чтобы протестировать работоспособность пакета на вашей машине, необходимо:

* Открыть в CoppeliaSim сцену `battleground.ttt`
* `$ python controller.py` в терминале; ожидать надписи в духе "Connected"
* Поместите в левую часть экрана окно CoppeliaSim, а в правую -- терминал с запущенным скриптом (win+стрелки)
* Сделайте активным окно терминала.
* Все готово к управлению. Используйте WASD для перемещения и IJKL для атаки.
* Для завершения сессии управлении нажмите Ctrl+C

Для того, чтобы понять, как заставить ездить **вашего** робота, нужно разобраться в шаблоне и переделать под себя. 
Комментарии внутри


