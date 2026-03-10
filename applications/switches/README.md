### Build image
`docker build -t switch_image .`

### Run Container
```
docker run \
    -e KASA_USERNAME=some_username@gmail.com \
    -e KASA_PASSWORD=some_password \
    -d --name switch_container \
    -p 80:80 \
    switch_image
```
