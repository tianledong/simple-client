import socket
import sys
import ssl


def analyze_message(message):
    split_message = message.split(' ')
    if split_message[1] == "BYE":
        return "BYE"
    split_message = split_message[2::]
    final_message = ""
    final_message = final_message.join(split_message)
    try:
        f_ans = eval(final_message)
    except ZeroDivisionError:
        return "ERR"
    except SyntaxError as s:
        print(f"ERR: {s}\n")
        print(f"Terminating...")
        return "SYN"
    return f_ans


def is_full_message(message):
    return message[-1] == '\n'


def main():
    # default port and server
    port = 27997
    server = "simple-service.ccs.neu.edu"
    # Create socket
    sock_t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to server
    try:
        sock_t.connect((server, port))
        print(f'Has connected to {server}. Port at {port}')
    except Exception as e:
        print(e)
        print('Connection failed')
        exit()
    # Send HELLO message
    hello = "cs5700spring2021 HELLO 001211949\n"
    sent = sock_t.send(hello.encode())
    if sent == 0:
        print("Connection has broken")
    else:
        print("Message has sent")

    # While still_working is True, keep receiving message
    still_working = True
    while still_working:
        is_full = False
        full_message = ""
        # when the message not full, keep receiving from the server
        while not is_full:
            received_message = sock_t.recv(16384).decode()
            full_message += received_message
            is_full = is_full_message(received_message)

        if full_message:
            ans = analyze_message(full_message)
            if ans == "ERR":
                sock_t.send('cs5700spring2021 ERR #DIV/0\n'.encode())
            elif ans == "BYE":
                split_message = full_message.split(' ')
                print(f"The secrete flag is {split_message[2]}\n")
                sock_t.send(('cs5700spring2021 BYE ' + str(ans) + '\n').encode())
                still_working = False
            elif ans == "SYN":
                still_working = False
            else:
                sock_t.send(('cs5700spring2021 STATUS ' + str(ans) + '\n').encode())
    sock_t.close()


if __name__ == '__main__':
    main()
    print(sys.argv[1])
