from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from textSummarizer.config.configuration import ConfigurationManager


class PredictionPipeline:

    def __init__(self):
        self.config = ConfigurationManager().get_model_evaluation_config()

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model_path = str(self.config.model_path)
        self.tokenizer_path = str(self.config.tokenizer_path)

        self.tokenizer = AutoTokenizer.from_pretrained(self.tokenizer_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_path).to(self.device)

        self.model.eval()

        self.MAX_INPUT_TOKENS = 900
        self.MAX_OUTPUT_TOKENS = 256
        self.OVERLAP = 100

    # -------- Chunking --------
    def chunk_text(self, text):
        tokens = self.tokenizer.encode(text)
        chunks = []

        start = 0
        while start < len(tokens):
            end = start + self.MAX_INPUT_TOKENS
            chunk_tokens = tokens[start:end]
            chunk_text = self.tokenizer.decode(chunk_tokens, skip_special_tokens=True)
            chunks.append(chunk_text)
            start += self.MAX_INPUT_TOKENS - self.OVERLAP

        return chunks

    # -------- Single summary pass --------
    def summarize_chunk(self, text, min_len, max_len):
        inputs = self.tokenizer(
            text,
            truncation=True,
            max_length=1024,
            return_tensors="pt"
        ).to(self.device)

        # Safety fallback for eos_token_id
        eos_id = self.tokenizer.eos_token_id if self.tokenizer.eos_token_id is not None else 1

        with torch.no_grad():
            ids = self.model.generate(
                inputs["input_ids"],
                attention_mask=inputs.get("attention_mask"), # Explicitly pass attention mask
                min_length=min_len,
                max_length=max_len,
                num_beams=8,
                length_penalty=1.0,
                early_stopping=True,
                # --- GENERATION GUARDRAILS ADDED BELOW ---
                repetition_penalty=2.0,                  # Stops word loops
                no_repeat_ngram_size=3,                  # Stops phrase loops
                pad_token_id=self.tokenizer.pad_token_id, 
                eos_token_id=eos_id                       
            )

        return self.tokenizer.decode(ids[0], skip_special_tokens=True)

    # -------- Public API --------
    def predict(self, text: str, user_target_words: int):

        input_words = len(text.split())
        min_words = max(30, input_words // 10)
        max_words = max(80, input_words // 2)
        target_words = max(min_words, min(user_target_words, max_words))

        min_len = int(target_words * 0.7)
        max_len = int(target_words * 1.3)

        # Long-document handling
        chunks = self.chunk_text(text)
        summaries = []

        for chunk in chunks:
            s = self.summarize_chunk(chunk, min_len, max_len)
            summaries.append(s)

        combined_summary = " ".join(summaries)

        # Refinement pass for coherence
        final_summary = self.summarize_chunk(combined_summary, min_len, max_len)

        return final_summary