FROM python:3.11-alpine
WORKDIR /app
COPY Pipfile pylibby.py /app/
RUN pip3 install pipenv && \
    pipenv install && \
    printf \
'echo "Checking for CRON_SCHEDULE."\n\
if [ -n "$CRON_SCHEDULE" ]; then\n\
    echo "CRON_SCHEDULE found, creating cron job."\n\
    echo "${CRON_SCHEDULE} cd /app; pipenv run python3 -u pylibby.py" | crontab -\n\
    echo "Running CMD once, then running crond."\n\
    eval "$@"\n\
    echo "Running crond..."\n\
    crond -f\n\
else\n\
    echo "CRON_SCHEDULE not found, running CMD."\n\
    exec "$@"\n\
fi\n'\
    > /app/entrypoint.sh && \
    chmod +x /app/entrypoint.sh

# ^^^if CRON_SCHEDULE is set, create a cron job, run CMD once, then start crond, else run CMD^^^

ENTRYPOINT [ "sh", "/app/entrypoint.sh" ]
CMD ["pipenv", "run", "python3", "-u", "pylibby.py"]