# Tutorial: Desplegar Agente IA con Gradio en Producción

Este proyecto muestra cómo desplegar un agente de IA con interfaz web usando Gradio, Docker y GitHub Actions.

## Requisitos previos

- Servidor con Ubuntu (ej: Hetzner)
- Docker y docker-compose instalados
- Dominio (ej: en Cloudflare)
- Tu proyecto con Dockerfile, docker-compose.yml y web.py

---

## Paso 1: Subir código al servidor

```bash
git clone <tu-repo> /home/usuario/proyecto
cd /home/usuario/proyecto
```

---

## Paso 2: Configurar variables de entorno

```bash
nano .env
```

Añade tus claves:
```
OPENROUTER_API_KEY=sk-...
```

---

## Paso 3: Construir y ejecutar el contenedor

```bash
sudo docker-compose up -d --build
```

---

## Paso 4: Verificar que funciona

```bash
sudo docker-compose ps          # Ver estado
sudo docker logs agente-ia-web  # Ver logs
ss -tlnp | grep 7860            # Verificar puerto
```

Prueba accediendo a: `http://TU_IP:7860`

---

## Paso 5: Configurar DNS en Cloudflare

1. Ve a https://dash.cloudflare.com
2. Selecciona tu dominio
3. DNS → Add record:
   - **Type**: A
   - **Name**: chat (o el subdominio que quieras)
   - **IPv4**: IP de tu servidor
   - **Proxy**: DNS only (nube gris)

---

## Paso 6: Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/mi-app
```

Contenido:
```nginx
server {
    listen 80;
    server_name chat.tudominio.com;

    location / {
        proxy_pass http://127.0.0.1:7860;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Activar y recargar:
```bash
sudo ln -s /etc/nginx/sites-available/mi-app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Paso 7: Instalar SSL con Certbot

```bash
sudo certbot --nginx -d chat.tudominio.com
```

---

## Paso 8: Acceder

✅ Tu aplicación está disponible en: **https://chat.tudominio.com**

---

## Paso 9: Configurar GitHub Actions (Despliegue Automático)

### 9.1 Crear usuario para GitHub Actions en el servidor

Ejecuta estos comandos en tu servidor:

```bash
# 1. Crear usuario github-deploy
sudo adduser github-deploy --disabled-password --gecos ""

# 2. Agregar al grupo docker
sudo usermod -aG docker github-deploy

# 3. Crear directorio SSH
sudo mkdir -p /home/github-deploy/.ssh
sudo chmod 700 /home/github-deploy/.ssh

# 4. Generar SSH key
sudo ssh-keygen -t ed25519 -C "github-actions-deploy" -f /home/github-deploy/.ssh/id_ed25519 -N ""

# 5. Añadir clave pública a authorized_keys
sudo cat /home/github-deploy/.ssh/id_ed25519.pub | sudo tee -a /home/github-deploy/.ssh/authorized_keys

# 6. Permisos correctos
sudo chmod 600 /home/github-deploy/.ssh/authorized_keys
sudo chown -R github-deploy:github-deploy /home/github-deploy/.ssh

# 7. Dar permisos del proyecto a github-deploy
sudo chown -R github-deploy:github-deploy /home/usuario/proyecto

# 8. Mostrar la clave PRIVADA (cópiala completa)
sudo cat /home/github-deploy/.ssh/id_ed25519
```

### 9.2 Configurar Secrets en GitHub

Copia la clave privada completa que muestra el último comando (desde `-----BEGIN` hasta `-----END`).

Luego ve a GitHub:
1. Tu repositorio → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** y crea estos secrets:

| Secret Name | Value |
|-------------|-------|
| `SSH_PRIVATE_KEY` | La clave privada completa |
| `SSH_HOST` | IP o dominio de tu servidor (ej: `162.55.208.55` o `chat.tudominio.com`) |
| `SSH_USER` | `github-deploy` |
| `SSH_PORT` | `22` |
| `PROJECT_PATH` | `/home/usuario/proyecto` |

### 9.3 Crear el archivo de workflow

Crea el archivo `.github/workflows/deploy.yml` en tu repositorio:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Deploy to server
      uses: appleboy/ssh-action@master
      with:
        host: ${{ secrets.SSH_HOST }}
        username: ${{ secrets.SSH_USER }}
        key: ${{ secrets.SSH_PRIVATE_KEY }}
        port: ${{ secrets.SSH_PORT }}
        script: |
          cd ${{ secrets.PROJECT_PATH }}
          git pull
          docker-compose down
          docker-compose up -d --build
```

### 9.4 Probar el despliegue automático

```bash
# En tu PC local
git add .
git commit -m "Test auto-deploy"
git push
```

Ve a GitHub → **Actions** y verás el workflow ejecutándose. ¡Cada `git push` actualizará tu servidor automáticamente! 🚀

---

## Actualizar código

Cuando hagas cambios en tu código local:

```bash
# En tu PC local
git add .
git commit -m "Descripción de cambios"
git push

# En el servidor
cd /home/usuario/proyecto
git pull
sudo docker-compose down
sudo docker-compose up -d --build
```

---

## Estructura del proyecto

```
agente-ia-produccion/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── web.py
├── .env.example
└── README.md
```

---

## Tecnologías utilizadas

- **Python 3.11**
- **Gradio 5.9.1** - Interfaz web
- **OpenRouter API** - Backend de IA (Grok)
- **Docker** - Contenedorización
- **Nginx** - Reverse proxy
- **Let's Encrypt** - Certificados SSL

---

## Licencia

MIT
