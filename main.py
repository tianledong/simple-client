import socket
import sys
import ssl


# analyze the message from the server
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
        return "SYN"
    return f_ans


# return if message is full (end \n). if message is empty will raise Systemexit
def is_full_message(message):
    if len(message) > 0:
        return message[-1] == '\n'
    else:
        print("Invalid message")
        raise SystemExit


# Read arguments from user's input. This will return port, server, nuid,
def read_args(args):
    if len(args) < 3:
        print("Invalid Inputs")
        raise SystemExit

    # default port and server
    port = 27997
    is_sll = False
    # server = "simple-service.ccs.neu.edu"
    server = args[-2]
    nuid = args[-1]

    # args have -s means it is sll
    if '-s' in args:
        is_sll = True
        port = 27998
    # args have -s means it contains port info
    if '-p' in args:
        port_index = args.index('-p') + 1
        port = int(args[port_index])
    return port, is_sll, server, nuid


def receive_message(sock_t):
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
                print(split_message[2])
                still_working = False
            elif ans == "SYN":
                still_working = False
            else:
                sock_t.send(('cs5700spring2021 STATUS ' + str(ans) + '\n').encode())


def main(args):
    # Get information from args
    port, is_ssl, server, nuid = read_args(args)

    # Create socket normally
    sock_t = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if is_ssl:
        # warp socket for SSL
        sock_t = ssl.wrap_socket(sock_t, cert_reqs=ssl.CERT_NONE)

    # Connect to server
    try:
        sock_t.connect((server, port))
    except Exception as e:
        print(e)
        raise SystemExit
    # Send HELLO message
    hello = f"cs5700spring2021 HELLO {nuid}\n"
    sent = sock_t.send(hello.encode())
    if sent == 0:
        print("Connection has broken")
        raise SystemExit
    # receive message from server
    receive_message(sock_t)
    # close socket
    sock_t.close()


if __name__ == '__main__':
    main(sys.argv)
