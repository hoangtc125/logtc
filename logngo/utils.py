import os


def setup_logging(log_file_path):
    # Tạo thư mục cho file log nếu nó chưa tồn tại
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
