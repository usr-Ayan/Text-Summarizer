from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
import torch
from textSummarizer.config.configuration import ConfigurationManager

class PredictionPipeline:
    def __init__(self):
        self.config = ConfigurationManager().get_model_evaluation_config()

        self.device = 0 if torch.cuda.is_available() else -1

        self.model_path = str(self.config.model_path)
        self.tokenizer_path = str(self.config.tokenizer_path)

        # Load once
        self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path)

        self.pipe = pipeline(
            "summarization",
            model=self.model,
            tokenizer=self.tokenizer,
            device=self.device
        )

    def predict(self, text: str) -> str:
        gen_kwargs = {
            "length_penalty": 0.8,
            "num_beams": 8,
            "max_length": 128
        }

        summary = self.pipe(text, **gen_kwargs)[0]["summary_text"]
        return summary
