# STAGE 1: Dependencies

FROM node:jod-trixie-slim AS dependencies

WORKDIR /app

COPY package.json package-lock.json ./

RUN nmp ci 

# STAGE 2:Development 

FROM dependencies AS development

COPY . .

EXPOSE 5174

CMD ["npm", "start"]



# STAGE 3: Builder

FROM dependencies AS builder 

COPY . . 

ARG REACT_APP_API_URL
ARG REACT_APP_ENV

ENV REACT_APP_API_URL=$REACT_APP_API_URL
ENV REACT_APP_ENV=$REACT_APP_ENV


RUN npm run build


# STAGE 4: Production
# We don't need Node.js to SERVE static files
# Nginx is much better at this job

FROM nginx:stable-trixie-perl AS production

# Copy our built React files into nginx's serve directory
COPY --from=builder /app/build /usr/share/nginx/html

# Copy our nginx config
COPY docker/nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]