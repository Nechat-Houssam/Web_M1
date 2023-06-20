# Utilise l'image Python 3.9 officielle comme image de base
FROM python:3.9

# Définit le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copie le fichier requirements.txt dans le conteneur
COPY requirements.txt /app/requirements.txt

# Installe les dépendances du projet, y compris Django
RUN pip install -r requirements.txt

# Copie le contenu du projet Django dans le conteneur
COPY . /app

# Expose le port sur lequel le projet Django s'exécute
EXPOSE 8000

# Définit la commande de démarrage du projet Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
