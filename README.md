# HTTPrint Telegram Bot

Telegram Bot for uploading files to HTTPrint server

Runs on docker

## How to

### Docker

Add following settings to your`docker-compose.yml` file:

```yaml
  httprint_telegram_bot:
    build: https://github.com/httprint/httprint_telegram_bot.git
    container_name: httprint_telegram_bot  # optional
    environment:
      - TELEGRAM_TOKEN=xxxxxxx # telegram bot token
      - HTTPRINT_HOST=http://httprint.example.com:7777 # optional, defaults to http://httprint:7777
      - LOG_LEVEL=DEBUG  # optional, defaults to INFO
    restart: unless-stopped
  ```
  
  * `TELEGRAM_TOKEN` is your bot token. Please refer to Telegram [documentation](https://core.telegram.org/bots#how-do-i-create-a-bot) to create a Bot.
  * `HTTPRINT_HOST` is your httprint server's URI/URL. If run in the same docker-compose stack, name your httprint service `httprint` and omit this env var.
  

# License and copyright

Copyright 2023 itec <itec@ventuordici.org>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Printer icon created by Good Ware - Flaticon
