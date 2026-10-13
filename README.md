# Cloud-Secure Predictive Maintenance & Machinery Health Monitoring System

Stack: Streamlit frontend, FastAPI backend, Docker Compose, AWS EC2.

## Important dataset note
This starter project uses simulated data to make the app runnable immediately. Your report specifies the AI4I 2020 Predictive Maintenance Dataset, so for a faithful final implementation you should train and evaluate on that real dataset and report measured results. AI4I has process temperature, air temperature, rotational speed, torque, tool wear and failure labels; it does not provide a direct vibration measurement. Do not describe simulated vibration as measured AI4I data. This demo is not validated for industrial safety.

## Local run
Install Docker Desktop, then:
```bash
docker compose up --build
```
Open http://localhost:8501. The FastAPI backend stays private on the Compose network. For local debugging only, temporarily publish backend port 8000 to localhost.

## AWS EC2
Use Ubuntu 24.04 LTS in EC2. Security Group: SSH port 22 from My IP only; Streamlit port 8501 from your IP for a temporary classroom demo. Do not publish backend port 8000. For public evaluator access, use HTTPS through a reverse proxy/domain and expose 443 rather than opening 8501 to everyone.

Install Docker Engine and the Compose plugin following current official Docker instructions for Ubuntu. Then:
```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Cloud-Secure-Predictive-Maintenance-Machinery-Health-Monitoring-System
sudo docker compose up --build -d
sudo docker compose ps
sudo docker compose logs --tail=100
```
Open `http://EC2_PUBLIC_IP:8501` only if the security group allows your IP.

Security implemented: backend private on Docker bridge network, non-root container users, Pydantic input validation, no AWS credentials in source. For production add HTTPS, monitoring, access controls, rate limiting and log management. Stop/delete cloud resources after evaluation to avoid charges.

API: `GET /health`, `POST /predict`, `GET /docs` on the internal backend service.
