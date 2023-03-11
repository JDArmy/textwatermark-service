FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

# RUN pip3 config --global set global.index-url http://pypi.douban.com/simple
# RUN pip3 config --global set install.trusted-host pypi.douban.com

RUN pip3 config --global set global.index-url https://mirrors.aliyun.com/pypi/simple/
RUN pip3 config --global set install.trusted-host mirrors.aliyun.com

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

# COPY ./src/textwatermark_service /code/textwatermark_service

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

CMD /wait && uvicorn textwatermark_service.main:app --host 0.0.0.0 --port 8000
