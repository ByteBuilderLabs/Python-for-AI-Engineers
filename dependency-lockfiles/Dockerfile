FROM python@sha256:aa943ce411423c7582288f18707ff66eddcbaeb510502d747a72aeb34f30d159
COPY --from=ghcr.io/astral-sh/uv:0.11.32 /uv /usr/local/bin/uv
WORKDIR /app
COPY agent.py questions.py run_eval.py requirements*.txt pyproject.toml uv.lock ./
ENV PATH="/app/.venv/bin:$PATH"
ARG REQS=requirements.txt
ARG CUTOFF=2026-10-27T00:00:00Z
RUN if [ "$REQS" = "uv.lock" ]; then \
      uv sync --locked --no-dev --no-cache; \
    else \
      pip install --no-cache-dir pip==26.2.2 && \
      pip install --no-cache-dir --uploaded-prior-to "$CUTOFF" -r "$REQS"; \
    fi
CMD ["python", "run_eval.py"]
RUN uv pip install rich
