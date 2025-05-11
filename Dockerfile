FROM python:3.12 as requirements_stage

WORKDIR /wheel

RUN python -m pip install --user pipx

COPY ./pyproject.toml \
  ./requirements.txt \
  /wheel/


RUN pip install --upgrade pip \
  && python -m pip wheel --wheel-dir=/wheel --no-cache-dir nonebot-plugin-miragetank nonebot_plugin_crazy_thursday nonebot-plugin-zxui nonebot-plugin-tortoise-orm nonebot-plugin-batitle \
  && python -m pip wheel --wheel-dir=/wheel --no-cache-dir --requirement ./requirements.txt \
  && python -m pip wheel --wheel-dir=/wheel --no-cache-dir nonebot-plugin-game-collection nonebot_plugin_memes

RUN python -m pipx run --no-cache nb-cli generate -f /tmp/bot.py


FROM python:3.12-slim

WORKDIR /app

VOLUME ["/app"]

ENV TZ Asia/Shanghai
ENV PYTHONPATH=/app

COPY ./docker/gunicorn_conf.py ./docker/start.sh /
RUN chmod +x /start.sh

ENV APP_MODULE _main:app
ENV MAX_WORKERS 1

COPY --from=requirements_stage /tmp/bot.py /app
COPY ./docker/_main.py /app
COPY --from=requirements_stage /wheel /wheel

RUN pip install --no-cache-dir gunicorn uvicorn[standard] nonebot2 \
  && pip install --no-cache-dir --no-index --force-reinstall --find-links=/wheel nonebot-plugin-miragetank nonebot_plugin_crazy_thursday nonebot-plugin-zxui nonebot-plugin-tortoise-orm nonebot-plugin-batitle \
  && pip install --no-cache-dir --no-index --force-reinstall --find-links=/wheel -r /wheel/requirements.txt \
  && pip install --no-cache-dir --no-index --force-reinstall --find-links=/wheel nonebot-plugin-game-collection nonebot_plugin_memes \
  && rm -rf /wheel
COPY . /app/
RUN mkdir /usr/share/fonts/ \
  && cp /app/simsun.ttc /usr/share/fonts/simsun.ttc \
  && fc-cache -f -v 
CMD ["/start.sh"]