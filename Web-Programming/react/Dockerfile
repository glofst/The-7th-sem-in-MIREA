FROM node as builder
RUN mkdir -p /project
WORKDIR /project
COPY . .
RUN npm install
RUN npm run build

FROM nginx
EXPOSE 80
COPY --from=builder /project/build /usr/share/nginx/html