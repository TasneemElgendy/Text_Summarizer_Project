from TextSummarizer.pipeline.stage_01_data_ingestion import DataIngestionTrainingPipeline
from TextSummarizer.pipeline.stage_02_data_validation import DataValidationTrainingPipeline
from TextSummarizer.pipeline.stage_03_data_transformation import DataTransformationTrainingPipeline
from TextSummarizer.pipeline.stage_04_model_trainer import ModelTrainerTrainingPipeline
from TextSummarizer.pipeline.stage_05_model_evaluation import ModelEvaluationTrainingPipeline

from TextSummarizer.logging import logger

STAGE1_NAME = "Data Ingestion Stage"
try:
    logger.info(f"______________________________"*20)
    logger.info(f">>>>>> stage {STAGE1_NAME} started <<<<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>>>>> stage {STAGE1_NAME} completed <<<<<<\n\nx==========x")
    logger.info(f"______________________________"*20)
except Exception as e:
    logger.exception(e)
    raise e 


STAGE2_NAME = "Data Validation Stage"
try:
    logger.info(f"______________________________"*20)
    logger.info(f">>>>>> stage {STAGE2_NAME} started <<<<<<")
    data_validation = DataValidationTrainingPipeline()
    data_validation.main()
    logger.info(f">>>>>> stage {STAGE2_NAME} completed <<<<<<\n\nx==========x")
    logger.info(f"______________________________"*20)
except Exception as e:
    logger.exception(e)
    raise e 

STAGE3_NAME = "Data Transformation Stage"
try:
    logger.info(f"______________________________"*20)
    logger.info(f">>>>>> stage {STAGE3_NAME} started <<<<<<")
    data_transformation = DataTransformationTrainingPipeline()
    data_transformation.main()
    logger.info(f">>>>>> stage {STAGE3_NAME} completed <<<<<<\n\nx==========x")
    logger.info(f"______________________________"*20)
    
except Exception as e:
    logger.exception(e)
    raise e


STAGE4_NAME = "Model Trainer Stage"
try:
    logger.info(f"______________________________"*20)
    logger.info(f">>>>>> stage {STAGE4_NAME} started <<<<<<")
    model_trainer = ModelTrainerTrainingPipeline()
    model_trainer.main()
    logger.info(f">>>>>> stage {STAGE4_NAME} completed <<<<<<\n\nx==========x")
    logger.info(f"______________________________"*20)
    
except Exception as e:
    logger.exception(e)
    raise e

STAGE5_NAME = "Model Evaluation Stage"
try:
    logger.info(f"______________________________"*20)
    logger.info(f">>>>>> stage {STAGE5_NAME} started <<<<<<")
    model_evaluation = ModelEvaluationTrainingPipeline()
    model_evaluation.main()
    logger.info(f">>>>>> stage {STAGE5_NAME} completed <<<<<<\n\nx==========x")
    logger.info(f"______________________________"*20)
    
except Exception as e:
    logger.exception(e)
    raise e
