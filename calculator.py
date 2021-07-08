"""
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""

import traceback


def add(*args):
    """ Returns a STRING with the sum of the arguments """
    try:
      return str(sum([int(x) for x in args]))
    except ValueError:
      raise ValueError('Error: can only operate on integer arguments.')

def subtract(*args):
    """ Returns a STRING with the result of subtraction of the arguments """
    try:
      args = [int(x) for x in args]
    except ValueError:
      raise ValueError('Error: can only operate on integer arguments.')

    result = args.pop(0)
    for arg in args:
      result -= arg

    return str(result)

def multiply(*args):
    """ Returns a STRING with the product of the arguments. """
    try:
      args = [int(x) for x in args]
    except ValueError:
      raise ValueError('Error: can only operate on integer arguments.')

    result = args.pop(0)
    for arg in args:
      result *= arg

    return str(result)

def divide(*args):
    """ Returns a STRING with the result of division of the arguments. """
    try:
      args = [int(x) for x in args]
    except ValueError:
      raise ValueError('Error: can only operate on integer arguments.')

    result = args.pop(0)
    try:
      for arg in args:
        result //= arg
    except ZeroDivisionError:
      raise ValueError('Error: cannot divide by zero.')

    return str(result)

def home():
    """ Homepage with guidelines for how to use app. """
    return """
Welcome to the calculator app.

Perform a calculation using a url path that includes the operation and operands, as in the
following example:

/add/2/2 --> 4
/subtract/4/2 --> 2
/multiply/2/2 --> 4
/divide/4/2 --> 2
"""

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """

    funcs = {
             '': home,
             'add': add,
             'subtract': subtract,
             'multiply': multiply,
             'divide': divide
             }

    args = path.strip('/').split('/')
    func_name = args.pop(0)

    try:
      func = funcs[func_name]
    except KeyError:
      raise NameError

    return func, args

def application(environ, start_response):
    headers = headers = [('Content-type', 'text/plain')]
    try:
      path = environ.get("PATH_INFO", None)
      if path is None:
        raise NameError

      func, args = resolve_path(path)
      body = func(*args)
      status = "200 OK"
    except NameError:
      status = "404 Not Found"
      body = "Not Found."
    except ValueError as error:
      status = "500 Internal Server Error"
      body = str(error)
    except Exception:
      status = "500 Internal Server Error"
      body = "Internal server error."
      print(traceback.format_exc())
    finally:
      headers.append(('Content-length', str(len(body))))
      start_response(status, headers)
      return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
