# function to calculate the dew point from the sensor reading of temperature and humidity
def dew_find(t , h):
  H_1 = math.log(h/100)+ (17.62 * t) / (243.12 + t) 
  D_1 = 243.12 * H_1 / (17.62 - H_1)
  return D_1
# function to read the temperature and humidity and make an object dew that calculates dew point
def read_sensor():
  global temp, hum, dew
  temp = hum = dew = 0
  
  try:
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    dew = dew_find(temp, hum)
    dew = round(dew , 2)
    msg = (b'{0:3.1f},{1:3.1f}, {2:3.1f}'.format(temp, hum, dew))
    
    return(msg)
      
   
  except OSError as e:
    return('Failed to read sensor.')
   
  
# web html function to build a display on the internet using html codes
def web_page():
  
  html = """<!DOCTYPE HTML><html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
  <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h2 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.2rem; }
    .dht-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
  </style>
</head>
<body>
  <h2>ESP32 Weather Server</h2>
  <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="dht-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;C</sup>
  </p>
  <p>
    <i class="fas fa-tint" style="color:#00add6;"></i> 
    <span class="dht-labels">Humidity</span>
    <span>"""+str(hum)+"""</span>
    <sup class="units">%</sup>
  </p>
  
  <p>
    <i class="fas fa-hand-point-right" style="color:#778899;"></i>
    <span class="dht-labels">DewPoint</span>
    <span>"""+str(dew)+"""</span>
    <sup class="units">&deg;C</sup>
  </p>
</body>
</html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
# requesting to run each function and give appropriate replies
while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  print('Content = %s' % str(request))
  sensor_readings = read_sensor()
  print(sensor_readings)
  sensor_dew = dew_find(temp, hum)
  print(sensor_dew)
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()




