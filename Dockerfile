FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md ./
COPY logparse ./logparse
RUN pip install --no-cache-dir . && useradd --uid 10001 --create-home logreader
USER logreader
ENTRYPOINT ["logparse"]
CMD ["--help"]
