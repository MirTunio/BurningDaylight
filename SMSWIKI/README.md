# Wikipedia by SMS
This project is an applet meant to be run in conjunction with the EnvayaSMS app on Anrdoid, and a Flask server running on locally using Termux. The goal is to provide access to Wikipedia through a simple SMS based interface. This applet would help those without the means or ability to use the internet to access this vast body of information for the cost of a few sms messages. The Server side would bear the cost burden of outgoing messages and internet access, which would be a small price to pay for the service it provides to potentially hundreds of thousands of people. 

I have written a series of articles describing my efforts in achieving this aim:

Part 1:
https://medium.com/burningdaylight/making-wikipedia-available-by-text-message-5b8a7913ec23?source=friends_link&sk=134c21f43030c4fa63b8e8eb5ce6168c

Part 2:
https://medium.com/burningdaylight/making-wikipedia-available-by-text-message-part-2-36be87cd0f0f?source=friends_link&sk=53cb15a1abad221ab5674b16f8f609ae

Part 3:
https://medium.com/burningdaylight/making-wikipedia-available-by-text-message-part-3-64115e1945bf?source=friends_link&sk=ddccff0613b6d1ee1869182b75a584ce

## Getting Started
(The files to use are "envaya_test_4.py" and "WikiHelper2.py")

Install EnvayaSMS and Termux on your phone. Install python on the Termux linux environment. Install virtualenv and then install the other dependancies (flask, wikipedia etc) using "pip install < dependancy>" in this virtual environment.
Clone the code to the android phone, and run the 'envaya_test_4.py' from the virtual environment. Open the EnvayaSMS app and point it to the flask server running at "http://localhost:5000/sms" by default.

## Future Goals

- Avail more services to users: Geo-location, weather forecast, news, short educational courses, english to urdu dictionaries.

- Create a more robust server setup which can handle a larger number of queries

- Make the sms-interface even simpler, clearer, and intuitive.


## License

This project is licensed under the MIT License
