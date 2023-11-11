#!/usr/bin/env python3

import os
import io
from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters

import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class httprint_telegram_bot():
    def __init__(self, conf: dict):
        # Initialize the class.
        super().__init__()

        telegram_token = conf.get("telegram-token")
        self.httprint_host = conf.get("httprint-host")
                
        self.application = Application.builder().token(telegram_token).build()
        self.application.add_handler(CommandHandler("start", self.t_start))
        self.application.add_handler(MessageHandler(filters.Document.PDF, self.t_attachment))


    def start(self):
        self.application.run_polling()

    async def t_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text("Welcome to httprint. Send me a pdf")

    async def t_attachment(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        # Download file
        message = update.message

        fname = message.document.file_name
        logger.info(f"Document {fname} received")
        logger.debug(f"Caption {message.caption}")

        new_file = await message.effective_attachment.get_file()
        # await new_file.download_to_drive(fname)
        fio=io.BytesIO()
        await new_file.download_to_memory(fio)
        files = {'file': (fname, fio.getvalue())}

        params = parseopt(message.caption)
        
        url = self.httprint_host + '/api/upload'
        try:
            r = requests.post(url, files=files, params = params)
            icon = "❌" if r.json().get("error") else "✅"
            msg = f"{icon} {r.json().get('message')}"
        except requests.exceptions.RequestException as e:
            msg = "🛑 Server error. Retry later"

        await update.message.reply_text(msg)
        logger.info(msg)


def parseopt(optstr):
    if not optstr:
        return({})
    opts = optstr.lower().split()
    
    d = {}
    for opt in opts:
        match opt:
            case "single" | "one":
                d["sides"] = "one-sided"
            case "long" | "2l" | "2long" | "twol" | "duplex" | "two":
                d["sides"] = "two-sided-long-edge"
            case "short" | "2s" | "2short" | "twos":
                d["sides"] = "two-sided-short-edge"
            case "a3" | "a4" | "a5":
                d["media"] = opt.upper()
            case "mono" | "gray" | "black" | "bw":
                d["color"] = "false"
            case "color" | "col" | "rgb" | "cmyk":
                d["color"] = "true"
            case _:
                if opt.isnumeric():
                    d["copies"] = int(opt)
    return(d)



if __name__ == '__main__':
    log_level = os.environ.get("LOG_LEVEL", "INFO")

    logging.basicConfig(level=log_level)
    logging.getLogger('telegram').setLevel(logging.WARNING)
    logging.getLogger('httpx').setLevel(logging.WARNING)
    logging.getLogger('httpcore').setLevel(logging.WARNING)

    config = {}
    config["httprint-host"] = os.environ.get("HTTPRINT_HOST", "http://httprint:7777")
    config["telegram-token"] = os.environ.get("TELEGRAM_TOKEN", "")

    HTB = httprint_telegram_bot(config)
    HTB.start()