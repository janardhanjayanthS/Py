FROM public.ecr.aws/lambda/python:3.12

# Copy requirements file
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire src directory
COPY src/ ${LAMBDA_TASK_ROOT}/src/

# Copy Lambda handler to root
COPY mangum_handler.py ${LAMBDA_TASK_ROOT}/

# Set the Lambda handler
CMD ["mangum_handler.handler"]
