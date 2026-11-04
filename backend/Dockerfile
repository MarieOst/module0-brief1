# 1. Image de base légère et sécurisée
FROM python:3.12-slim

# 2. Variables d'environnement Python
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

# 3. Répertoire de travail
WORKDIR /app

# 4. Installation de uv pour un build ultra-rapide
RUN pip install --no-cache-dir uv

# Copier les metadonnees et les sources necessaires a l'installation du package.
COPY pyproject.toml uv.lock README.md ./
COPY backend ./backend
COPY src ./src
COPY data ./data
COPY models ./models

# Installer les dependances et le package iatos_core.
RUN uv sync --frozen --no-dev

# 8. Exposition du port API
EXPOSE 8000

# 9. Commande de lancement uvicorn
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]