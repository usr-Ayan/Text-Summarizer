from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
from textSummarizer.config.configuration import ConfigurationManager


class PredictionPipeline:

    def __init__(self):
        self.config = ConfigurationManager().get_model_evaluation_config()

        self.device = 0 if torch.cuda.is_available() else -1

        self.model_path = str(self.config.model_path)
        self.tokenizer_path = str(self.config.tokenizer_path)

        # Load model and tokenizer once
        self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path)

        self.pipe = pipeline(
            "summarization",
            model=self.model,
            tokenizer=self.tokenizer,
            device=self.device
        )

    def predict(self, text: str, user_target_words: int):

        input_words = len(text.split())

        min_words = max(30, input_words // 10)
        max_words = max(80, input_words // 2)

        target_words = max(min_words, min(user_target_words, max_words))

        gen_kwargs = {
            "min_length": int(target_words * 0.7),
            "max_length": int(target_words * 1.3),
            "num_beams": 8,
            "length_penalty": 1.0,
            "early_stopping": True
        }

        result = self.pipe(text, **gen_kwargs)[0]["summary_text"]
        return result
