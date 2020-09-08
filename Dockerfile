FROM python:3.8.5

ENV PYTHONUNBUFFERED=TRUE
WORKDIR /app
COPY . .
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN make html
RUN useradd -ms /bin/bash edbook
USER edbook
CMD python -m http.server $PORT --directory /app/_build/html 