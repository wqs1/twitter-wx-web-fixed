FROM python:3.10-slim

WORKDIR /app

COPY . .

# 安装 supervisor 和 pip 清华源加速
RUN apt update && apt install -y supervisor && \
    pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD ["sh", "-c", "supervisord -c supervisord.conf & python app/web.py"]
