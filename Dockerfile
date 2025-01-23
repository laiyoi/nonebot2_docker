FROM python:3.12-slim

WORKDIR /app

COPY . /app/

ENV TZ Asia/Shanghai
ENV PYTHONPATH=/app

COPY ./docker/gunicorn_conf.py ./docker/start.sh /
RUN apt-get update && apt-get install -y gcc libjpeg-dev zlib1g-dev build-essential libgl1-mesa-glx \
  && chmod +x /start.sh

ENV APP_MODULE _main:app
ENV MAX_WORKERS 1

#COPY --from=requirements_stage /tmp/bot.py /app
COPY ./docker/_main.py /app
#COPY --from=requirements_stage /wheel /wheel
RUN python -m pip install --user pipx \
  && python -m pipx run --no-cache nb-cli generate -f /app/bot.py \
  && pip install --no-cache-dir gunicorn uvicorn[standard] nonebot2 \
# && pip install --no-cache-dir --no-index --force-reinstall --find-links=/wheel -r /wheel/requirements.txt && rm -rf /wheel
  && pip install --no-cache-dir nonebot-plugin-crazy-thursday nonebot-plugin-tarot \
  && pip install --no-cache-dir -r /app/requirements.txt
  # && rm -rf /wheel

CMD ["/start.sh"]