from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import Trainer, TrainingArguments
from transformers import DataCollatorForSeq2Seq
from datasets import load_dataset, load_from_disk
import torch
from TextSummarizer.entity import ModelTrainerConfig
import os

class ModelTrainer:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config
        
    def train(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"

        local_checkpoint = r"C:/Users/Tasne/Documents/Ashter Katkoota/NLP Projects/TextSummarizer/Text_Summarizer_Project/artifacts/model_trainer/checkpoint-800"
        # ✅ Use local model if available (offline mode)
        if os.path.exists(local_checkpoint):
            print(f"🔹 Using local checkpoint from: {local_checkpoint}")
            tokenizer = AutoTokenizer.from_pretrained(local_checkpoint)
            model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(local_checkpoint, use_safetensors=True).to(device)
        else:
            print(f"🌐 Downloading model from Hugging Face: {self.config.model_ckpt}")
            tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
            model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt, use_safetensors=True).to(device)

        # tokenizer = AutoTokenizer.from_pretrained(self.config.model_ckpt)
        # model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_ckpt,
                                                        #   use_safetensors=True).to(device)
        seq2seq_data_collator = DataCollatorForSeq2Seq(tokenizer, model=model_pegasus)
        
        # load data:
        dataset_samsum_pt = load_from_disk(self.config.data_path)
        
        training_args = TrainingArguments(
            output_dir=self.config.root_dir, num_train_epochs=self.config.num_train_epochs, warmup_steps=self.config.warmup_steps,
            per_device_train_batch_size=self.config.per_device_train_batch_size, per_device_eval_batch_size=self.config.per_device_train_batch_size,
            weight_decay=self.config.weight_decay, logging_steps=self.config.logging_steps,
            eval_strategy=self.config.eval_strategy, eval_steps=self.config.eval_steps, save_steps=self.config.save_steps,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps , fp16=True 
        )
        
        trainer = Trainer(model=model_pegasus, args=training_args,
                    tokenizer=tokenizer, data_collator=seq2seq_data_collator,
                    train_dataset=dataset_samsum_pt["train"],
                    eval_dataset=dataset_samsum_pt["validation"])
        
        # Resume from last checkpoint if available
        if os.path.exists(local_checkpoint):
            print("🔄 Resuming training from last checkpoint...")
            trainer.train(resume_from_checkpoint=local_checkpoint)
        else:
            print("🚀 Starting fresh training...")
            trainer.train()
        
        
        # trainer.train(resume_from_checkpoint="C:/Users/Tasne/Documents/Ashter Katkoota/NLP Projects/TextSummarizer/Text_Summarizer_Project/artifacts/model_trainer/checkpoint-800")
        model_save_path = os.path.join(self.config.root_dir, "pegasus-samsum-model")
        tokenizer_save_path = os.path.join(self.config.root_dir, "tokenizer")

        #save model:
        model_pegasus.save_pretrained(model_save_path)
        #save tokenizer:
        tokenizer.save_pretrained(tokenizer_save_path)
