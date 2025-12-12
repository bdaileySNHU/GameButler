# Deployment Guide for GameButler

This guide explains how to deploy GameButler to a VPS (Virtual Private Server) using Docker.

## Prerequisites
- A VPS (e.g., DigitalOcean, Linode, AWS EC2) running Ubuntu/Debian.
- **Git** installed on the VPS.
- `docker` and `docker-compose` (or `docker compose` for newer versions) installed on the VPS.
- Domain name `gamebutler.bdailey.com` pointing to your VPS IP.

## Method 1: Manual Deployment (Simple)

1.  **SSH into your VPS:**
    ```bash
    ssh user@your-vps-ip
    ```
    (Replace `user` with your VPS username, and `your-vps-ip` with its IP address.)

2.  **Prepare Project Directory and Clone the Repository:**
    It's recommended to clone your project into a dedicated directory, for example, `/var/www/gamebutler`.

    First, ensure Git is installed:
    ```bash
    sudo apt update
    sudo apt install git -y # For Debian/Ubuntu based systems. Adjust for other OS.
    ```

    Then, create the directory and clone your repository:
    ```bash
    sudo mkdir -p /var/www/gamebutler
    sudo chown $USER:$USER /var/www/gamebutler # Grant ownership to your current user
    cd /var/www/gamebutler
    git clone https://github.com/bdaileySNHU/GameButler.git . # The '.' clones into the current empty directory
    ```
    *Note: If `/var/www/gamebutler` is not empty or `git clone` fails, you might need to manually empty it or address other issues. For pulling updates later, you'd use `git pull` from inside `/var/www/gamebutler`.*

3.  **Setup Environment:**
    Create a `.env` file for production configuration. This file will be read by Docker Compose to set environment variables for your services.
    ```bash
    nano .env
    ```
    Content:
    ```env
    # Frontend will need to know where the API is. 
    # Since we use Nginx proxy in Docker, relative path '/api' works best.
    VITE_API_URL=/api
    ```
    (Press `Ctrl+X`, then `Y`, then `Enter` to save and exit `nano`.)

4.  **Run with Docker Compose:**
    ```bash
    docker compose up -d --build # Use 'docker compose' (with a space) for newer Docker versions
    ```
    -   `docker compose up`: Starts the services defined in `docker-compose.yml`.
    -   `-d`: Runs the containers in detached mode (in the background).
    -   `--build`: Rebuilds the images if there are any changes in the Dockerfiles or context.

    This command will:
    -   Build the `backend` Docker image from `Dockerfile.backend`.
    -   Build the `frontend` Docker image from `Dockerfile.frontend`.
    -   Start the `backend` container, mapping its internal port 8000 to the host's port 8000.
    -   Start the `frontend` container (which uses Nginx internally), mapping its internal port 80 to the host's port 80.

5.  **Access:**
    Open `http://your-vps-ip` in your web browser. You should see the GameButler application. If you have DNS set up, you can also access it via `http://gamebutler.bdailey.com`.

## Method 2: Production with HTTPS (Nginx Proxy Manager or Certbot)

Since the docker container exposes port 80, you likely want to put it behind a secure reverse proxy on the host to handle SSL (LetsEncrypt).

### Option A: Using Nginx on Host

1.  **Update `docker-compose.yml`** to bind to a local port instead of host 80 (to avoid conflict if you run other sites):
    Change:
    ```yaml
    ports:
      - "8080:80"  # Expose container port 80 to host port 8080
    ```

2.  **Install Nginx & Certbot on Host:**
    ```bash
    sudo apt update
    sudo apt install nginx python3-certbot-nginx -y
    ```

3.  **Configure Nginx:**
    Create `/etc/nginx/sites-available/gamebutler` with the following content. Make sure to replace `gamebutler.bdailey.com` with your actual domain if different.
    ```nginx
    server {
        server_name gamebutler.bdailey.com;

        location / {
            proxy_pass http://localhost:8080; # Ensure this port matches your docker-compose.yml host port for frontend
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        }
    }
    ```

4.  **Enable Site:**
    ```bash
    sudo ln -s /etc/nginx/sites-available/gamebutler /etc/nginx/sites-enabled/
    sudo nginx -t # Test Nginx configuration for syntax errors
    sudo systemctl restart nginx
    ```

5.  **Enable SSL (HTTPS) with Certbot:**
    ```bash
    sudo certbot --nginx -d gamebutler.bdailey.com
    ```
    Follow the prompts. Certbot will automatically configure Nginx for HTTPS.

## CI/CD Deployment (Advanced)
To automate deployment, you can set up a GitHub Action that SSHs into your VPS and runs `git pull && docker compose up -d --build` whenever you push to main. This requires setting up SSH keys as GitHub Secrets.