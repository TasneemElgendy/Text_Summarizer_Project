from TextSummarizer.config.configuration import ConfigurationManager
from transformers import AutoTokenizer, pipeline



class PredictionPipeline:
    def __init__(self, length_percent: int = 50):
        self.config= ConfigurationManager().get_model_evaluation_config()
        self.length_percent = max(10, min(length_percent, 50))
        self.max_input_chars = 4000
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        
        self.pipe = pipeline(
            "summarization",
            model=self.config.model_path,
            tokenizer=self.tokenizer,
            device=-1
        )
    def predict(self,text):       
        if len(text) > self.max_input_chars:
            text = text[:self.max_input_chars]

        approx_input_tokens = len(self.tokenizer.tokenize(text))
        max_len = max(60, int(approx_input_tokens * (self.length_percent / 100)))

        gen_kwargs = {"length_penalty": 0.8,
                    "num_beams":8,
                    "max_length": min(max_len, 256),
                    "min_length": max(20, int(max_len / 3))
        }


        print("Dialogue:")
        print(text)

        output = self.pipe(text, **gen_kwargs)[0]["summary_text"]
        print("\nModel Summary:")
        print(output)
        
        return output