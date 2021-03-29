# tg_yanao_news
Агрегатор новостей ЯНАО в телеграм для канала СЦ: Новости ЯНАО

## Dependencies
- Python 3.8
- PostgreSQL 10+
- Docker

## How to build and run
```bash
# Сборка контейнера
docker build -t tg_yanao_news_sc .

# Запуск контейнера
docker run --network host tg_yanao_news_sc
```