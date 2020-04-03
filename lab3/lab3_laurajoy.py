__author__ = "Jane Doe"
__email__ = "jdoe@bu.edu"
__lab__ = "lab3"

import socket
import sys
import math

""" # Lab 3 - The Calc Text Transfer Protocol

## Problem
In this lab, you will implement a server for the Calc Text Transfer Protocol (CTTP). Your task 
is to implement a CTTP Server which is 100% compatible with the CTTP 1.0 Protocol Specification 
given below.

The job of this Server is to send an Announcement any time a Client connects to inform about the 
supported operations. Then, the Server listens for Requests and returns appropriate Responses
back to the Client until the Client terminates the Connection.

## Hints
* You may use the code skeleton below, modify it however you like, or even start from scratch!
* We will test the CTTP Server for compliance with the CTTP Specification by sending it valid
  queries a CTTP Client.
* A functioning CTTP Client is provided (lab3_cttpclient.py), which has two operating modes:
    * Shell mode, in which the user can interact with the connected server
    * File replay mode, in which the client automatically sends a series of commands
      found in a text file to the server. This is useful for testing your server against many
      different queries at once!
    * Note: Modifying the client is not part of the lab.
* Your server should respond as defined for any valid CTTP Request
* Your server should not crash if arbitrary unexpected request are made, but return an appropriate
  error instead (see CTTP Specifcation).

"""


def is_valid_number(num):
    try:
        float(num)
        return True
    except ValueError:
        pass

    return False

def valid_args(args, operation):
    error = "none"

    #  verifies that there are enough operands to perform calculation
    if len(args) == 5:
        # checks that format of message is correct
        if (args[0] == "CTTP/1.0") & (args[1] == "CALC") & (args[2] == operation):
            # verifies that arguments passed are numeric
            if is_valid_number(args[3]) & is_valid_number(args[4]):
                return error
                
            error = "not numbers"
        else:
            error = "format"
    else:
        error = "number of args"

    return error

class CalcTextServer(object):
    """ A CTTP Server implementation.

    """

    def __init__(self, host='', port=12345):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.addr = None
        self.transcript = []

    def run_server(self, terminate_on_close=False):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)

        stay_alive = True
        while stay_alive:
            # accept a new connection
            self.conn, self.addr = self.socket.accept()
            # Send the Announcement
            self.conn.sendall(b"CTTP/1.0 HELP\nADD SUB MUL DIV ABS SQRT")

            # Accept a Request until this condition is set to False
            accept_query = True
            while accept_query:
                # Receive and decode some data
                request = self.conn.recv(1024).decode('utf-8')
                if not request:  # ignore empty requests
                    break
                if "ADD" in request:
                    result = self.add(request)

                    if result == "format":
                        message = "CTTP/1.0 ERROR\nError: Wrong format for ADD"
                    elif result == "number of args":
                        message = "CTTP/1.0 ERROR\nError: Wrong number of arguments for ADD"
                    elif result == "not numbers":
                        message = "CTTP/1.0 ERROR\nError: Wrong arguments for ADD"
                    else:
                        message = "CTTP/1.0 CALC\n" + str(result)

                    self.conn.sendall(message.encode())

                elif "SUB" in request:
                    result = self.sub(request)

                    if result == "format":
                        message = "CTTP/1.0 ERROR\nError: Wrong format for SUB"
                    elif result == "number of args":
                        message = "CTTP/1.0 ERROR\nError: Wrong number of arguments for SUB"
                    elif result == "not numbers":
                        message = "CTTP/1.0 ERROR\nError: Wrong arguments for SUB"
                    else:
                        message = "CTTP/1.0 CALC\n" + str(result)

                    self.conn.sendall(message.encode())

                elif "MUL" in request:
                    result = self.mul(request)

                    if result == "format":
                        message = "CTTP/1.0 ERROR\nError: Wrong format for MUL"
                    elif result == "number of args":
                        message = "CTTP/1.0 ERROR\nError: Wrong number of arguments for MUL"
                    elif result == "not numbers":
                        message = "CTTP/1.0 ERROR\nError: Wrong arguments for MUL"
                    else:
                        message = "CTTP/1.0 CALC\n" + str(result)

                    self.conn.sendall(message.encode())

                elif "DIV" in request:
                    result = self.div(request)

                    if result == "format":
                        message = "CTTP/1.0 ERROR\nError: Wrong format for DIV"
                    elif result == "number of args":
                        message = "CTTP/1.0 ERROR\nError: Wrong number of arguments for DIV"
                    elif result == "not numbers":
                        message = "CTTP/1.0 ERROR\nError: Wrong arguments for DIV"
                    elif result == "zero":
                        message = "CTTP/1.0 ERROR\nError: Cannot divide by zero"
                    else:
                        message = "CTTP/1.0 CALC\n" + str(result)

                    self.conn.sendall(message.encode())

                elif "ABS" in request:
                    result = self.abs(request)

                    message = "CTTP/1.0 CALC\n" + str(result)
                    self.conn.sendall(message.encode())

                elif "SQRT" in request:
                    result = self.sqrt(request)

                    message = "CTTP/1.0 CALC\n" + str(result)
                    self.conn.sendall(message.encode())

                elif "BYE" in request:
                    self.conn.sendall(b"CTTP/1.0 KTHXBYE\n")
                    stay_alive = False if terminate_on_close else True
                    accept_query = False  # jump out of accept_query loop
                else:
                    self.conn.sendall(b"CTTP/1.0 ERROR\nUnkown request")
            # This client is done, close the connection
            self.conn.close()
        # close socket at the end
        self.socket.close()

    def add(self, request):
        args = request.split(' ')
        error = valid_args(args, "ADD")

        if error == "none":
            return float(args[3]) + float(args[4])

        return error

    def sub(self, request):
        args = request.split(' ')
        error = valid_args(args, "SUB")

        if error == "none":
            return float(args[3]) - float(args[4])

        return error

    def mul(self, request):
        args = request.split(' ')
        error = valid_args(args, "MUL")

        if error == "none":
            return float(args[3]) * float(args[4])

        return error

    def div(self, request):
        args = request.split(' ')
        error = valid_args(args, "DIV")

        if error == "none":
            if float(args[4]) != 0:
                return float(args[3]) / float(args[4])
            error = "zero"

        return error

    def abs(self, request):
        return 1

    def sqrt(self, request):
        return 1


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 24680
    c = CalcTextServer('', port)
    c.run_server(terminate_on_close=True)

""" # Calc Text Transfer Protocol Specification v.1.0

The Calc Text Transfer Protocol (CTTP) is a simple protocol that can be used to implement a 
calculator over TCP.

Notes:

* Any capitalized noun refers to that term as defined elsewhere in the specifcation, i.e., Server refers to a CTTP Server or a Message refers to a CTTP Message as defined in the respective sections.
* In the term definitions below, terms enclosed in `<Angle Brackets>` are variables. Any term that is not enclosed in angle brackets should be taken literally. The following terms indicate special symbols:

```
<SP>  = ' ' 
<NL>  = '\n' 
|     = <logical OR> 
[<x>] = <<x> is optional> 
```

## CTTP Server-Client Interaction

When a **CTTP Client** connects to the listening port of a **CTTP Server**, the Server immediately sends Usage Instructions listing the available capabilities (See CTTP Usage Instructions). It then listens for Requests from the Client.

Upon receipt of the Usage Instructions, a Client may send Requests to the Server (see CTTP Requests).

Upon receipt of a Request, a Server responds to the Client with an appropriate Response (see CTTP Response).

## CTTP Messages

A **CTTP Message** is a TCP packet that is transferred between a Client and a Server, (or vice versa). In CTTP 1.0, every message uses the following structure:

```
<Message>        = <Message-Header>[<NL><Message-Body>]

<Message-Header> = <CTTP-Version><SP><Message-Code>
<CTTP-Version>   = CTTP/1.0
<Message-Code>   = OHAI|CALC|ERROR|HELP|BYE|KTHBYE
```

The meaning of these Message Codes is:

* **CALC**: This is about a calculation
* **ERROR**: An error occurred an the requested response cannot be produced
* **HELP**: This is a help text / usage documentation
* **BYE**: The Client wants to terminate the session
* **KTHXBYE**: The Server confirms termination of the session

The `<Message-Body>` varies depending on the type of the message, as follows:

### CTTP Request

A **CTTP Request** is a Message sent from the Client to the Server to request a calculation.

The Message Body of a Request is:

```
<Message-Body-Request> = [<SP><Command>]
```

Only the Message Codes `CALC`, `HELP`, or `BYE` are allowed in a Request -- any other Message Code in a Request results in an `ERROR` Response. The `HELP` and `BYE` Requests do not have a `<Command>` (anything after the Message Code is ignored). For Messages of type `CALC`, the `<Command>` is

```
<Command>  = <Operator><SP><Operand1>[<SP><Operand2>]
<Operator> = ADD|SUB|MUL|DIV|ABS|SQRT
<Operand*> = <int>|<float>
```

The Operators listed above perform mathematical operations as expected:

* `ADD`:  `<Operand1> + <Operand2>`
* `SUB`:  `<Operand1> - <Operand2>`
* `MUL`:  `<Operand1> * <Operand2>`
* `DIV`:  `<Operand1> / <Operand2>` if `<Operand2>!=0` else return an `ERROR` Response
* `ABS`:  absolute value of `<Operand1>`
* `SQRT`: square root of `<Operand1>` if `<Operand1>>=0`, else return an `ERROR` Response

Note that all Operators expect two Operators, except `ABS`, and `SQRT` expecting a single Operand. An incorrect number of Operands should result in an `ERROR` Response by the Server.

### CTTP Response

A **CTTP Response** is a Message sent from the Server to the Client containing the response to a Request. It has the following structure:

```
<Response> = <CTTP-Version><SP><Message-Code><NL><Content>
```

The `<Content>` may be any UTF-8-encoded text that responds to the Request.

Generally, the Message Code corresponds to the Message Code in the Request. Exceptions:

* If an error occurred during a calculation, Message Code `ERROR` is sent in response to a `CALC` Request.
* When a client sends a `BYE` request, the server always responds with `KTHXBYE`.

### CTTP Usage Instructions
A **CTTP Usage Instructions** are a special Message that the Server sends in two cases:

* Immediately after a Client connects, Usage Instructions are sent without any Request
* If a `HELP` Request is received, the Server responds with Usage Instructions.

The structure of Usage Instructions are a special case of a Response, where the `<Content>` is a space-separated list of all the `<Operator>` functions the Server implements.

## Example

This is an example of the message exchange between a Client and a Server.

> Client connects to Server.

> Server --> Client:

```
CTTP/1.0 HELP
ADD SUB MUL DIV ABS SQRT
```

> Client --> Server:
```
CTTP/1.0 CALC ADD 1 1
```

> Server --> Client:
```
CTTP/1.0 CALC
2
```

> Client --> Server:
```
CTTP/1.0 CALC ABS 1 x
```

> Server --> Client:
```
CTTP/1.0 ERROR
Wrong number of arguments for ABS.
```

> Client --> Server:
```
CTTP/1.0 CALC SIN 0.5
```

> Server --> Client:
```
CTTP/1.0 ERROR
Unknown command.
```

> Client --> Server:
```
CTTP/1.0 BYE
```

> Server --> Client:
```
CTTP/1.0 KTHXBYE
```

> Disconnection.
"""
