FROM python:3.12-slim
ARG LAMBDA_TASK_ROOT="/var/task"
ENV LAMBDA_TASK_ROOT=${LAMBDA_TASK_ROOT}
WORKDIR ${LAMBDA_TASK_ROOT}

# Copy requirements file
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire src directory
COPY src/ ${LAMBDA_TASK_ROOT}/src/

# Copy Lambda handler to root
COPY lambda_handler.py ${LAMBDA_TASK_ROOT}/

# Set the Lambda handler
CMD ["lambda_handler.handler"]
