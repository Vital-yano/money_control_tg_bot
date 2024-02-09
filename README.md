# Money_control_tg_bot

![GitHub](https://img.shields.io/github/license/vital-yano/money_control_fastapi_backend) ![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/kaccuteput/money_control_tg_bot)

### Описание
Репозиторий содержит телеграмм бот для контроля своих расходов. 
Используемый стек:
- Python 3.11
- Python-telegram-bot
- Pyright
- Ruff
- Redis
- Docker

Redis поднимается в Docker.

### Инструкция по запуску проекта и работе с ним

Установка виртуального окружения и зависимостей:
```bash
python -m venv venv && source venv/bin/activate && pip install -r req.txt
```

Запуск контейнера redis:
```bash
make redis_up
```

Создание индекса в redis:
```bash
python create_redis_index.py
```


Запуск приложения:
```bash
python main.py
```

Доступные команды
```
/register - регистрация
/cancel - отмена регистрации
```

### Планы на будущее
На данный момент реализована только регистрация пользователей. Планируется реализовать позже:

- Взаимодействие с другими сущностями, такими как: 
	- статьи доходов/расходов, 
	- кошелёк, 
	- переводы, 
	- долги, 
	- бюджет.
