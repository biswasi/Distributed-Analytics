# Install Sagemaker
!pip install boto3 sagemaker
import sagemaker
import boto3
from sagemaker import get_execution_role
from sagemaker.inputs import TrainingInput
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Initialize the SageMaker session
sagemaker_session = sagemaker.Session()

# Define the S3 bucket and prefix to store data
output_bucket = sagemaker.Session().default_bucket()
output_prefix = 'sagemaker/linear-learner'
role = get_execution_role()

# Load the Iris dataset
iris = load_iris()
X = iris.data
y = iris.target

# Convert to DataFrame for easier manipulation
data = pd.DataFrame(X, columns=iris.feature_names)
data['target'] = y

train_data, validation_data = train_test_split(data, test_size=0.2, random_state=42
  # Save to CSV
train_data.to_csv('train.csv', index=False, header=False)
validation_data.to_csv('validation.csv', index=False, header=False)
s3 = boto3.client('s3')
s3.upload_file('train.csv', output_bucket, f'{output_prefix}/train/train.csv')

s3.upload_file('validation.csv', output_bucket, f'{output_prefix}/validation/validation.csv')

s3_train_data = f"s3://{output_bucket}/{output_prefix}/train"
print(f"training files will be taken from: {s3_train_data}")
s3_validation_data = f"s3://{output_bucket}/{output_prefix}/validation"
print(f"validation files will be taken from: {s3_validation_data}")
output_location = f"s3://{output_bucket}/{output_prefix}/output"
print(f"training artifacts output location: {output_location}")

# generating the session.s3_input() format for fit() accepted by the sdk
train_data = sagemaker.inputs.TrainingInput(
    s3_train_data,
    distribution="FullyReplicated",
    content_type="text/csv",
    s3_data_type="S3Prefix",
    record_wrapping=None,
    compression=None,
)

#TODO: Name it as `validation_data`
validation_data = sagemaker.inputs.TrainingInput(
    s3_validation_data,
    distribution="FullyReplicated",
    content_type="text/csv",
    s3_data_type="S3Prefix",
    record_wrapping=None,
    compression=None,
)
from sagemaker.image_uris import retrieve

container = retrieve("linear-learner", boto3.Session().region_name, version="1")
print(container)
deploy_amt_model = True

%%time
import boto3
import sagemaker
from time import gmtime, strftime

sess = sagemaker.Session()

job_name = "linear-learner-iris-regression-" + strftime("%Y%m%d-%H-%M-%S", gmtime())
print("Training job", job_name)

linear = sagemaker.estimator.Estimator(
    container,
    role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=output_location,
    sagemaker_session=sagemaker_session,
)

# TODO: Use the set_hyperparameters function and set the following hyperparameters on linear learner
# feature_dim=4, predictor_type='regressor', mini_batch_size=20
linear.set_hyperparameters(
    feature_dim=4,  # Adjust this to match your feature dimension
    predictor_type='regressor',  # Use 'classifier' for classification
    mini_batch_size=20
)

%%time
linear.fit(inputs={"train": train_data, "validation": validation_data}, job_name=job_name)
