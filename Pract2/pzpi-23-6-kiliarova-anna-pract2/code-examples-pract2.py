# Приклад агрегації даних (BFF) scala
case class TrackDto(
  id: Long,
  title: String,
  streamable: Boolean,
  author: String
)

def getTrackView(trackId: Long): Future[TrackDto] =
  for {
    track <- trackService.fetch(trackId)
    policy <- policyService.checkAvailability(trackId)
    user <- userService.fetch(track.authorId)
  } yield TrackDto(
    id = track.id,
    title = track.title,
    streamable = policy.allowed,
    author = user.displayName
  )

# Event-driven indexing
def on_track_updated(track_id: int):
    track = primary_store.load_track(track_id)
    doc = build_search_document(track)

    kafka.publish(
        topic="search.documents",
        key=str(track_id),
        value=doc
    )

def shipper():
    for message in kafka.consume("search.documents"):
        elasticsearch.index(
            index="tracks",
            id=message.key,
            document=message.value
        )

"""
Запити до ШІ

Інструмент: ChatGPT (OpenAI), модель GPT-5.3.
Мета використання: формування структури презентації, уточнення архітектурних підходів SoundCloud, 
генерація прикладів коду та пояснення взаємодії компонентів системи.
Внесок автора: усі відповіді перевірені, відредаговані та адаптовані відповідно до наукових джерел; 
використано лише верифіковану інформацію.

Запит 1 до ChatGPT. Тема: загальна архітектура SoundCloud.
Опиши архітектуру SoundCloud як розподіленої системи. Які основні рівні та компоненти системи?
Скорочена відповідь: SoundCloud використовує багаторівневу мікросервісну архітектуру, що включає 
BFF-рівень для клієнтів, Value-Added Services для агрегації даних, Domain Gateways для управління 
доменами та Foundation Services для роботи з даними. Для зберігання використовується MySQL, для подієвої 
взаємодії — Kafka, для пошуку — Elasticsearch.

Запит 2 до ChatGPT. Тема: взаємодія компонентів.
Поясни, як відбувається оновлення треку в SoundCloud із використанням Kafka та Elasticsearch.
Скорочена відповідь: Клієнт надсилає запит через BFF, який передається до foundation service. Дані 
зберігаються в MySQL, після чого Event Feeder публікує подію в Kafka. Indexer обробляє подію, формує 
документ і передає його до Elasticsearch через Shipper для оновлення пошукового індексу.

Запит 3 до ChatGPT. Тема: масштабованість системи.
Які підходи використовуються в SoundCloud для забезпечення масштабованості та надійності?
Скорочена відповідь: Система використовує Kubernetes для оркестрації, Kafka для асинхронної взаємодії, 
HAProxy для балансування навантаження та Zipkin для моніторингу. Також застосовуються патерни retry, 
timeout і circuit breaker.
"""