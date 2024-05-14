import asyncio
import logging
from queue import Empty

from fastapi import FastAPI
from starlette.responses import StreamingResponse
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer

from ray import serve

logger = logging.getLogger("ray.serve")

app = FastAPI()


@serve.deployment
@serve.ingress(app)
class Textbot:
    def __init__(self, model_id: str):
        self.loop = asyncio.get_running_loop()

        self.model_id = model_id
        self.model = AutoModelForCausalLM.from_pretrained(self.model_id)
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)