# auth_checker.py: Web Authorization Testing

This Python framework simplifies complex authorization tests in web apps.
It is recommended to combine it with Burp Suite and the extension [Copy As Python-Requests](https://portswigger.net/bappstore/b324647b6efa4b6a8f346389730df160). Copy relevant requests and define them as a function in `custom_requests.py`. The flow and logic of executing test cases is defined in `auth_checker.py`.

Compared to Burp extensions such as AuthMatrix and similar, this framework features a much higher control and flexibility in creating test cases. For example, it is trivial to pass a retrieved id of a created object to next test through other accounts. If the object got deleted by a test case, create it again before continuing. A more complex logic can be defined with custom conditions and orders test cases are executed.

The flexibility comes with the downside of more time to set things up. The test sequence can be easily repeated later. It features a way to first authenticate all accounts and keeping sessions active by repeating test requests. All responses can be logged for easier debugging.

## Main script arguments

`auth_checkery.py renew`  
Renew all sessions and write them to disk.

`auth_checkery.py keep`  
Run defined test requests to keep sessions alive. Run it simultaneously while testing to make sure the sessions stay alive.

