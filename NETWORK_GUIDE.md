# Hướng dẫn chơi Othello qua mạng

## Cách sử dụng

### Người chơi 1 (Server - Black):

```bash
python othello.py network_server network_receiver --port 12345 -v
```

### Người chơi 2 (Client - White):

```bash
python othello.py network_receiver network_client --host <IP_SERVER> --port 12345 -v
```

Thay `<IP_SERVER>` bằng địa chỉ IP của máy server (ví dụ: `192.168.1.100` hoặc `localhost` nếu chơi trên cùng máy).

## Giải thích

- **network_server**: Engine cho người chơi server (chơi màu Đen/Black)
- **network_client**: Engine cho người chơi client (chơi màu Trắng/White)
- **network_receiver**: Engine nhận nước đi từ đối thủ qua mạng

## Các tham số

- `--host <IP>`: Địa chỉ IP của server (chỉ dùng cho client)
- `--port <PORT>`: Cổng kết nối (mặc định: 12345)
- `-v`: Hiển thị bàn cờ sau mỗi nước đi (khuyến nghị)

## Ví dụ

### Trên cùng một máy (localhost):

**Terminal 1 (Server):**

```bash
python othello.py network_server network_receiver --port 12345 -v
```

**Terminal 2 (Client):**

```bash
python othello.py network_receiver network_client --host localhost --port 12345 -v
```

### Qua mạng LAN:

**Máy Server (IP: 192.168.1.100):**

```bash
python othello.py network_server network_receiver --port 12345 -v
```

**Máy Client:**

```bash
python othello.py network_receiver network_client --host 192.168.1.100 --port 12345 -v
```

## Lưu ý

1. Server phải chạy trước và chờ client kết nối
2. Đảm bảo firewall cho phép kết nối trên port đã chọn
3. Cả hai người chơi cần nhập nước đi theo format: `a1`, `b2`, `c3`, etc. (chữ cái + số)
4. Game sẽ tự động đồng bộ nước đi giữa hai người chơi
