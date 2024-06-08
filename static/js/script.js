let reviews;
let origins;
let destinations;
var map = L.map('map').setView([0, 0], 2);


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
  org_lat = org[32]
  org_lon = org[33]

  des = reviews[0].find(arr=>arr[18]==city)
  des_lat = des[34]
  des_lon = des[35]

  const orgMarker = L.marker([org_lat, org_lon]).addTo(map).bindPopup('Origin: ' + city + ' / Lat.: ' + org_lat + ' / Long.: ' + org_lon);
  const desMarker = L.marker([des_lat, des_lon]).addTo(map).bindPopup('Destination: ' + city);

  //  // Add airplane markers for origin and destination
  //  const airplaneIcon = L.icon({
  //   iconUrl: 'path/to/airplane-icon.png',
  //   iconSize: [30, 30]
  // });

  // const airplaneMarkerOrg = L.marker([org_lat, org_lon], { icon: airplaneIcon }).addTo(map).bindPopup('Airplane: Origin - ' + city);
  // const airplaneMarkerDes = L.marker([des_lat, des_lon], { icon: airplaneIcon }).addTo(map).bindPopup('Airplane: Destination - ' + city);

       // Draw a polyline from origin to destination
  const polyline = L.polyline([[org_lat, org_lon], [des_lat, des_lon]]).addTo(map);
};

// get routes from flask
const init = async() => {
    reviews = await ((await fetch('/api/v1.0/airline_reviews_for_flask')).json());
    reviews[0].map(col => col[17])
    // new Set(reviews[0].map(col => col[11])) # included in [ ... new...]
    // [ ... new Set(reviews[0].map(col => col[11]))] # included in [ ... new...]
    
    origins = [ ... new Set(reviews[0].map(col => col[17]))].sort();

    getDest(origins[0])
    
    origins.forEach(city => document.getElementById('source'). innerHTML += `<option>${city}</option>`)
     console.log(reviews);
};

init();

var data = [
    {
      domain: { x: [0, 1], y: [0, 1] },
      value: 450,
      title: { text: "<b>Satisfaction Gauge</b>" },
      type: "indicator",
      mode: "gauge+number",
      delta: { reference: 400 },
      gauge: { axis: { range: [null, 500] } }
    }
  ];
  
  var layout = { width: '40%', height: 400, paper_bgcolor: 'white'};
  Plotly.newPlot('gauge', data, layout);
