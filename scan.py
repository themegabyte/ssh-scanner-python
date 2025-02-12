import requests
import paramiko
import base64
import hashlib
import logging
import sys


def raw_key_to_sha256(key):
    # Get the raw key in bytes
    key_bytes = key.asbytes()

    # Compute the SHA-256 hash of the key
    sha256_hash = hashlib.sha256(key_bytes).digest()

    # Encode the hash in Base64
    base64_encoded_hash = base64.b64encode(
        sha256_hash).decode('utf-8').rstrip('=')

    # Format the output as SHA256:<base64_encoded_hash>
    formatted_output = f"SHA256:{base64_encoded_hash}"

    return formatted_output


def setup_logger(log_file='app.log', log_level=logging.INFO):
    """
    Set up logging to both console and a log file.

    :param log_file: The file to which logs will be written.
    :param log_level: The logging level (e.g., logging.INFO, logging.DEBUG).
    :return: The configured logger.
    """
    # Create a logger
    logger = logging.getLogger(__name__)
    logger.setLevel(log_level)

    # Create a formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Create a file handler and set the formatter
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    # Create a console handler and set the formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def fetch_webpage(url):
    try:
        response = requests.get(url, timeout=1)
        response.raise_for_status()  # Raise an error for bad responses

        # Get the web server version if available
        server_version = response.headers.get('Server', 'Not available')

        # Return the formatted string
        return f"Webserver: {server_version} response: {response.text}"

    except requests.RequestException as e:
        return f"Error fetching the webpage: {e}"

# Example usage:
# result = fetch_webpage('http://example.com')


def main():

    logger = setup_logger(log_level=logging.DEBUG)

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-H", "--host", help="The host to connect to.", required=True)
    parser.add_argument(
        "-P", "--port", help="The port to connect to.", type=int, required=True)
    args = parser.parse_args()
    url = f"http://{args.host}/"

    ssh = paramiko.Transport((args.host, args.port))
    ssh.start_client()
    key = ssh.get_remote_server_key()
    ssh.close()
    logger.debug(
        f"SSH: {args.host}:{str(args.port)} {key.get_name()} -> {raw_key_to_sha256(key)} SSH Version: {ssh.remote_version}")
    logger.debug(f"HTTP GET:{url} {fetch_webpage(url)}")


if __name__ == '__main__':
    main()
