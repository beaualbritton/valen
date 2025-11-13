# shoutout Stanislav
# https://khromov.se/dockerizing-your-sveltekit-applications-a-practical-guide/


FROM node:22-alpine AS builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build
RUN npm prune --production

FROM node:22-alpine
WORKDIR /frontend
COPY --from=builder /frontend/build build/
COPY --from=builder /frontend/node_modules node_modules/
EXPOSE 3000
ENV NODE_ENV=production
CMD [ "node", "build" ]

