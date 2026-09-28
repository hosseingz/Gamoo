FROM node:22

WORKDIR /app

COPY package*.json ./


RUN npm config set registry https://registry.npmjs.org/ \
    && npm config set fetch-retry-maxtimeout 600000 \
    && npm config set fetch-retries 10 \
    && npm config set fetch-timeout 1200000 \
    && npm config set progress false \
    && npm config set maxsockets 3 \
    && npm install --verbose

COPY . .

ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV

RUN npm run build

# Next.js development server port
EXPOSE 3000


CMD ["sh", "-c", "if [ \"$NODE_ENV\" = \"production\" ]; then npm run start; else npm run dev; fi"]