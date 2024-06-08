let reviews;
let origins;
let destinations;
var map = L.map('map').setView([40, -95], 2);
let routeLayer = L.layerGroup().addTo(map);

  // Add airplane markers for origin and destination
  const airplaneIcon1 = L.icon({
    iconUrl: 'static/images/plane.png',
   backgroundColor:'green',
    iconSize: [100, 50]
  });
 
   const airplaneIcon2 = L.icon({
    iconUrl: 'static/images/landing.png',
   backgroundColor:'green',
    iconSize: [50, 50]
  });

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

const getDest = city => {
  console.log('City: ',city);
  document.getElementById('destination').innerHTML = '';
  destinations = reviews[0].filter(arr => arr[17].includes(city));
 
  destinations
    .map(arr=>arr[18]).sort()
    .forEach(dest => document.getElementById('destination').innerHTML += `<option>${dest}</option>`);

  org = reviews[0].find(arr=>arr[17]==city)
  org_lat = org[32].toFixed(6)
  org_lon = org[33].toFixed(6)

  des = destinations.find(obj=>obj[18]==document.getElementById('destination').value)
  des_lat = des[34].toFixed(6)
  des_lon = des[35].toFixed(6)

 routeLayer.clearLayers();

  const orgMarker = L.marker([org_lat, org_lon],{ icon: airplaneIcon1 })
    .bindPopup(`<h5>Origin:<br>${city} <br>Lat.: ${org_lat} <br>Long.: ${org_lon}</h5>`).addTo(routeLayer);
  const desMarker = L.marker([des_lat, des_lon],{ icon: airplaneIcon2 }).bindPopup('Destination: ' + des[18]).addTo(routeLayer);

  const polyline = L.polyline([[org_lat, org_lon], [des_lat, des_lon]]).addTo(routeLayer);

  runGauge();
};

const calculateFlightDuration = () => {
  const source = document.getElementById('source').value;
  const destination = document.getElementById('destination').value;

  const flight = reviews[0].find(arr => arr[17] === source && arr[18] === destination);

  if (flight) {
    const duration = flight[36];
    document.getElementById('flight-duration').innerHTML = `Flight Duration: ${duration} hours`;
  } else {
    document.getElementById('flight-duration').innerHTML = 'Flight Duration: N/A';
  }
};

const newDest = () => {

  org = reviews[0].find(obj=>obj[17]==document.getElementById('source').value)
  org_lat = org[32].toFixed(6)
  org_lon = org[33].toFixed(6)

  des = reviews[0].find(obj=>obj[18]==document.getElementById('destination').value)
  des_lat = des[34].toFixed(6)
  des_lon = des[35].toFixed(6)

 routeLayer.clearLayers();

  const orgMarker = L.marker([org_lat, org_lon],{ icon: airplaneIcon1 })
    .bindPopup(`<h5>Origin:<br>${document.getElementById('source').value} <br>Lat.: ${org_lat} <br>Long.: ${org_lon}</h5>`).addTo(routeLayer);
  const desMarker = L.marker([des_lat, des_lon],{ icon: airplaneIcon2 }).bindPopup('Destination: ' + des[18]).addTo(routeLayer);

  const polyline = L.polyline([[org_lat, org_lon], [des_lat, des_lon]]).addTo(routeLayer);

  runGauge();
};

// get routes from flask
const init = async() => {
    reviews = await ((await fetch('/api/v1.0/airline_reviews_for_flask')).json());
    origins = [ ... new Set(reviews[0].map(col => col[17]))].sort();

    getDest(origins[0])
    
    origins.forEach(city => document.getElementById('source'). innerHTML += `<option>${city}</option>`)
     console.log(reviews);
};

init();

const runGauge = async () => {
  reviews = await ((await fetch('/api/v1.0/airline_reviews_for_flask')).json());

  rating = reviews[0].find(arr => (arr[17]==document.getElementById('source').value)&&(arr[18]==document.getElementById('destination').value))[9];
  var data = [
    {
      domain: { x: [0, 1], y: [0, 1] },
      value: rating,
      title: { text: "<span style='font-size: 30px;'><b>Overall Rating</b>" },
      type: "indicator",
      mode: "gauge+number",
      delta: { reference: 100 },
      gauge: { 
        axis: { range: [null, 10] }, bar:{color:'red'},
        bgcolor: "white",
        borderwidth: 0,
        bordercolor: "gray"
      }
    }
  ];
  
  var layout = { width: '20%', height: 300, paper_bgcolor: 'white'};
  Plotly.newPlot('gauge', data, layout);
};