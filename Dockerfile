FROM davidtnfsh/python


EXPOSE 8000

# Add demo app
COPY ./app /app
# WORKDIR /app
RUN pip3 install -r app/requirements.txt

ENTRYPOINT [""]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app.main"]