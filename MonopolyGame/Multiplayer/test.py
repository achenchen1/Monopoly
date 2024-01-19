from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

import string
import random
import names


# RSA is probably overkill for this
def generate_key_pair():
    key_size = 2048

    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=key_size, backend=default_backend()
    )

    # Generate public key from private key
    public_key = private_key.public_key()

    return private_key, public_key


def generate_game_link():
    valid_chars = string.ascii_letters + string.digits
    game_link = "".join(random.sample(valid_chars, 8))
    return game_link


def generate_player_key(game_link):
    player_name = names.get_first_name()
    return player_name + "," + game_link


def send_move(player_key, move):
    encrypted = public_key.encrypt(
        (player_key + "," + move).encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return encrypted


def receive_move(encrypted):
    decrypted = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return decrypted.decode().split(",")


private_key, public_key = generate_key_pair()
print(game_link := generate_game_link())
print(player_name := generate_player_key(game_link))
print(encrypted := send_move(player_name, "e4"))
print(decrypted := receive_move(encrypted))
