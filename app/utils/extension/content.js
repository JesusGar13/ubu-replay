// Función para enviar datos a Flask
function sendDataToFlask(data) {
    fetch('http://127.0.0.1:5000/api/track', {  // URL de tu servidor Flask
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Data sent successfully:', data);
    })
    .catch((error) => {
        console.error('Error sending data:', error);
    });
}

// Llamar a sendDataToFlask en managerSession
function managerSession(tabId, url) {
  if (sesiones[tabId] !== undefined && sesiones[tabId].abierta) {
    sesiones[tabId].recorrido.push(url);
    let data = {
      url: url,
      action: 'update',
      timestamp: new Date().toISOString()
    };
    sendDataToFlask(data);  // Enviar datos al servidor Flask
  }
}
