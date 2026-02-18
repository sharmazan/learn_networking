# Toy HTTP server using Python sockets

Запуск + тести (curl)

Terminal A
```
python toy_http_server.py
```

Terminal B
```
curl -v http://127.0.0.1:8000/
curl -v http://127.0.0.1:8000/health
curl -v -X POST http://127.0.0.1:8000/echo -H "Content-Type: application/json" -d '{"msg":"hi"}'
```

