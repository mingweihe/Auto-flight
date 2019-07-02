<h1>Auto Flight using Multiple Logistic Linear Regression</h1>
The purpose of this project is to teach Tello drone automatically flying. In other words, it's basically a project about image classification.<br>
What is the functionality of my code?<br>
1.Teach tello drone how to fly automatically.
2.Calling tello python API.
3.Connect encapsulated API with trained image classification model, which is also meant -- Auto-flight.
<br>
<h2>Run it with Terminal command:</h2>
sudo python start.py checkpoints/gesture/ checkpoints/operation/<br>
parameters description:<br>
<h4>1."checkpoints/gesture/": </h4>
gesture recognition trained model directory. (DeepLearning Model Hybrid-7 refer to <a href='https://github.com/mingweihe/HandGestureRecognition'>HandGestureRecognition</a>)<br>
<h4>2."checkpoints/operation/": </h4>
autoflight trained model directory<br>
<img src = "https://github.com/mingweihe/AutoFlight/blob/master/screenshot/IMG_8626%202.JPG?raw=true" width='25%'><br>
Test screenshot<br>
<img src = "https://github.com/mingweihe/AutoFlight/blob/master/screenshot/screenshot2018-0703_14-03-47-235110.png?raw=true" width='25%'><br>
Training in jupyter<br>
<img src = "https://github.com/mingweihe/AutoFlight/blob/master/screenshot/screenshot2018-0703_18-31-34-560725.png?raw=true" width='25%'><br>
