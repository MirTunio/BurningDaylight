# Wikipedia by SMS
This project is an applet meant to be run in conjunction with the EnvayaSMS app on Anrdoid, and a local

Part 1:
https://medium.com/burningdaylight/making-wikipedia-available-by-text-message-5b8a7913ec23?source=friends_link&sk=134c21f43030c4fa63b8e8eb5ce6168c

Part 2:
https://medium.com/burningdaylight/making-wikipedia-available-by-text-message-part-2-36be87cd0f0f?source=friends_link&sk=53cb15a1abad221ab5674b16f8f609ae

Part 3:
coming soon


## Getting Started

Install EnvayaSMS and Termux on your phone. Install python on the Termux linux environment. Install virtualenv and then install the other dependancies (flask, wikipedia etc) using "pip install < dependancy>" on the environment.
Clone the code to the android phone, and run the 'envaya_test_4.py' from the virtual environment. Open the EnvayaSMS app and point it to the flask server running at "http://localhost:5000/sms".


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

