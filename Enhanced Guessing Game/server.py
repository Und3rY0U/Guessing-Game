import socket
import random

PASSWORD = "Lucero"

def get_rating(guesses):
    if guesses <= 5:
        return "Excellent"
    elif guesses <= 20:
        return "Very Good"
    else:
        return "Good/Fair"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 12345))
server.listen(5)

print("Server is running on port 12345...")

while True:
    client, address = server.accept()
    print(f"Connected to {address[0]}:{address[1]}")

    client.send("Welcome, Client!".encode())

    received_password = client.recv(1024).decode()
    if received_password != PASSWORD:
        client.send("Incorrect password. Connection closed.".encode())
        client.close()
        continue

    client.send("Access granted. Guess a number between 1 and 100.".encode())

    secret_number = random.randint(1, 100)
    guess_count = 0

    while True:
        data = client.recv(1024).decode()
        if not data:
            break

        guess = int(data)
        guess_count += 1

        if guess < secret_number:
            client.send("Too low".encode())
        elif guess > secret_number:
            client.send("Too high".encode())
        else:
            rating = get_rating(guess_count)
            result = f"Correct! You guessed it in {guess_count} tries. Rating: {rating}"
            client.send(result.encode())
            break

    client.close()
