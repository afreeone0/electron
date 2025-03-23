FROM python:3.12-alpine AS builder
WORKDIR /electron
ENV PYTHONUNBUFFERED=1
RUN python3 -m pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir gunicorn
RUN pip install --no-cache-dir -r requirements.txt
COPY ./electron .
RUN python3 manage.py collectstatic --noinput
ENTRYPOINT ["python3", "manage.py", "migrate", "&&", "gunicorn", "-w", "3", "-b", "0.0.0.0:8000", "electron.wsgi:application"]

FROM nginx AS proxy
COPY --from=builder /electron/staticfiles /var/www/static
COPY ./nginx.conf /etc/nginx/