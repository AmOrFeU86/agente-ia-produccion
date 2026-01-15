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
