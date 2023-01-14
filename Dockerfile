FROM python:3.11-alpine
WORKDIR /app
COPY Pipfile pylibby.py /app/
RUN pip3 install pipenv && \
    pipenv install && \
    printf \
'if [ -n "$CRON_SCHEDULE" ]; then\n\
    echo "${CRON_SCHEDULE} cd /app; pipenv run python3 -u pylibby.py" | crontab -\n\
    crond && exec "$@"\n\
else\n\
    exec "$@"\n\
fi\n'\
    > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# ^^^if CRON_SCHEDULE is set, create a cron job, start crond and run CMD, else run CMD^^^

ENTRYPOINT [ "sh", "/app/entrypoint.sh" ]
CMD ["pipenv", "run", "python3", "-u", "pylibby.py"]