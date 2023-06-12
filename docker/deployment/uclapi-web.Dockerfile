FROM node:18-alpine AS builder
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED 1

COPY ./uclapi-frontend/package.json ./
RUN npm install

COPY ./uclapi-frontend .
RUN npm run build && npm install --production

FROM node:18-alpine AS runner
WORKDIR /app
ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

ARG ENVIRONMENT
ENV ENVIRONMENT ${ENVIRONMENT}

COPY --from=builder /app/next.config.js ./
COPY --from=builder /app/middleware.ts ./
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

COPY ./docker/deployment/non-public/${ENVIRONMENT}/uclapi/uclapi-web.env /app/.env

EXPOSE 3000

CMD ["npm", "run", "start"]
