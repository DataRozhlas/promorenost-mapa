const map = L.map('promorenost-mapa');
map.scrollWheelZoom.disable()

map.on('click', function() {
    map.scrollWheelZoom.enable()
})

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; přispěvatelé <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>, data Ministerstvo zdravotnictví'
}).addTo(map);

let vals = ok.map(v => v[1]);
vals = vals.concat(ob.map(v => v[1]))

const scl = d3.scaleLinear(d3.interpolatePiYG)
    .domain([Math.min(...vals), Math.max(...vals)])
    .range([0, 1]) 

    const mista = L.featureGroup();

ok.forEach((okres) => {
    L.polygon(okres[2], {
        color: 'white',
        weight: .5,
        fillColor: d3.interpolateOrRd(scl(okres[1])),
        fillOpacity: 0.9,
    }).addTo(mista).bindPopup(`<b>Okres ${okres[0]}</b><br>V posledních 3 měsících nakažených ${(okres[1] * 1000)/10} % obyvatel`)
})

ob.forEach((obec) => {
    L.circleMarker(obec[2], {
        radius: 6,
        color: 'white',
        weight: .5,
        fillColor: d3.interpolateOrRd(scl(obec[1])),
        fillOpacity: 1,
    }).addTo(mista).bindPopup(`<b>Obec ${obec[0]}</b><br>V posledních 3 měsících nakažených ${(obec[1] * 1000)/10} % obyvatel`)
})

mista.addTo(map)
map.fitBounds(mista.getBounds());