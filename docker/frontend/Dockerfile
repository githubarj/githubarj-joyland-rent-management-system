# STAGE 1: Dependencies
FROM node:20-alpine AS dependencies
WORKDIR /app
COPY frontend/package.json frontend/yarn.lock ./
RUN yarn install --frozen-lockfile

# STAGE 2: Development
FROM dependencies AS development
COPY frontend/ .
EXPOSE 5174
CMD ["yarn", "dev"]

# STAGE 3: Builder
FROM dependencies AS builder
COPY frontend/ .
ARG REACT_APP_API_URL
ARG REACT_APP_ENV
ENV REACT_APP_API_URL=$REACT_APP_API_URL
ENV REACT_APP_ENV=$REACT_APP_ENV
RUN yarn build

# STAGE 4: Production
FROM nginx:stable-alpine AS production
COPY --from=builder /app/dist /usr/share/nginx/html
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
