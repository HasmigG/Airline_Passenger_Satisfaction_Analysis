var map = L.map('map').setView([0, 0], 2);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// get routes from flask
const init = async() => {
    reviews = await ((await fetch('/api/v1.0/airlines_reviews')).json());

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