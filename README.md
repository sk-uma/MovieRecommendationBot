# MovieRecommendationBot
Bot using telegram API

### 実行方法

.env ファイルを作成し[TELEGRAM_APIKEY](https://core.telegram.org/), [TMDB_APIKEY](https://developers.themoviedb.org/3/getting-started)を記述

```shell
$> cat .env
TELEGRAM_APIKEY='spam-ham'
TMDB_APIKEY='ham-egg'
```

以下を実行

```shell
$> docker build -t chatbot .
$> docker run --name chatBotContainer -d -it chatbot
```

### 機能

telegramを利用した映画推薦Botです。
