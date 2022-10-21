FROM node:16

WORKDIR /app

# Install system dependencies
# RUN apt update && apt install --no-install-recommends -y wget ffmpeg

COPY package.json .

RUN npm install -g npm@latest
RUN npm i

# Clean cache
# RUN apt-get clean && rm -rf /var/lib/apt/lists/*
RUN npm cache clean -force

# Copy files
COPY public public
COPY src src
COPY index.html index.html
COPY vite.config.ts vite.config.ts
COPY tsconfig.json tsconfig.json
COPY tsconfig.config.json tsconfig.config.json

# RUN server
ENTRYPOINT npm run dev
