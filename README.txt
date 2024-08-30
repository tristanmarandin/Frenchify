Instructions to build the AWS production environment:
+ Implement the AWS Lambda Function available Under /resources.
+ Collect the URL that will be used as an Endpoint for your local code.
+ Mention this URL in the local code, in the lambda function call.

Instructions to finetune your model:
+ Parametrize your Sagemaker Instance
+ The data are located under ./resources.
+ Run the Jupyter Notebook related to the data processing under /resources so you can use a proper dataset.
+ Run the Jupyter Notebook under /resources in your SageMaker instance

Instructions related to the local code:
The local code is asking for a path to the file to translate (support .pdf, .doc, .docx) as soon as run.
This way you can easily incorporate it into AAQE