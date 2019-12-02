from testingframework.logging.logger.mlflow_logger import MLflowLogger
from testingframework.datagenerator.predict_data_generator import PredictDataGenerator
from testingframework.logging.session import Session
from testingframework.datagenerator.units.cross_validation_unit import CrossValidationUnit
from testingframework.datagenerator.units.every_pair_unit import EveryPairUnit
from testingframework.test.TestModel import TestModel

#unexisting folder
session = Session("experiment1", "project1", "./projects")
logger = MLflowLogger(session)
print("Experiment 1 done")

#empty names
session = Session("", "project", "./projects")
logger = MLflowLogger(session)

print("Experiment 2 done")

session = Session("experiment2", "", "./projects")
logger = MLflowLogger(session)

print("Experiment 3 done")

session = Session("experiment3", "project3", "")
logger = MLflowLogger(session)

print("Experiment 4 done")

#real path
session = Session("experiment4", "project4", "./LoggerTest")
print ("Session was created")
units = [CrossValidationUnit(fold_size=2), EveryPairUnit()]
print ("Units was created")
test_model = TestModel()
print ("Model was created")
data = PredictDataGenerator(units=units, file_names=["train_data"], batch_size= test_model.batch_size)
print ("Data generator was created")
with MLflowLogger(session) as logger:
    logger.log_parameter("param1", 30)
    logger.log_parameter("param2", 16)
    
    test_model.model.fit_generator(data, steps_per_epoch=test_model.nb_train_samples, epochs=test_model.epochs)
    logger.log_metric("metric1", 59)

    logger.log_input_data(data)

    with open("artifact.txt", "w+") as file:
        file.write("text")

    logger.log_artifact("artifact.txt", "storage_dir")

