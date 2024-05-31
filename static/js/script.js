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

const url = `http://api.openweathermap.org/geo/1.0/direct?limit=5&appid=${api_key}&q=`;