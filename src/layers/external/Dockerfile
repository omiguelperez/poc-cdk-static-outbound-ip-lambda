FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install --upgrade pip

RUN pip install --upgrade -r requirements.txt --target=/asset/python

CMD ["python"]
