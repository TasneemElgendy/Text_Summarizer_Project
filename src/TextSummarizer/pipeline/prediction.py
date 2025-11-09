from TextSummarizer.config.configuration import ConfigurationManager
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM  # ✅ تعديل: أضفنا AutoModelForSeq2SeqLM بدل pipeline


class PredictionPipeline:
    def __init__(self, length_percent: int = 50):
        self.config = ConfigurationManager().get_model_evaluation_config()
        self.length_percent = max(10, min(length_percent, 50))
        self.max_input_chars = 4000

        # تحميل التوكنيزر
        self.tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        
        # ✅ حذف الـ pipeline لأننا هنستخدم model.generate بدلًا منها
        self.model = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path)  # ✅ سطر جديد

    def predict(self, text):       
        # تقطيع النص الطويل
        if len(text) > self.max_input_chars:
            text = text[:self.max_input_chars]

        # حساب التوكنز التقريبي
        approx_input_tokens = len(self.tokenizer.tokenize(text))
        max_len = min(256, max(60, int(approx_input_tokens * (self.length_percent / 100))))  # ✅ نفس المنطق
        min_len = max(20, int(max_len / 3))  # ✅ نفس المنطق

        # ✅ تعديل: حساب length_penalty بناءً على النسبة من 10% لـ 50%
        length_penalty = 2.5 - (self.length_percent / 40)
        length_penalty = round(length_penalty, 2)

        print(f"Using length_penalty={length_penalty}, max_len={max_len}, min_len={min_len}, for length_percent={self.length_percent}%")

        # ✅ حذف gen_kwargs القديم، واستبداله باستدعاء generate مباشر
        # تجهيز الإدخال للموديل
        inputs = self.tokenizer(
            text,
            return_tensors="pt",
            truncation=True,
            padding="longest",
            max_length=1024
        )

        # ✅ استدعاء generate من الموديل نفسه (بدون pipeline)
        summary_ids = self.model.generate(
            **inputs,
            num_beams=8,
            max_length=max_len,
            min_length=min_len,
            length_penalty=length_penalty,
            early_stopping=True
        )

        # ✅ فك التشفير من التوكنز للنص النهائي
        output = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

        print("\nModel Summary:")
        print(output)
        return output
