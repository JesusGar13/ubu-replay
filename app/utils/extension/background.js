console.log("Background script running");

let sesiones = {};
const TIMEOUT_DURATION = 30 * 60 * 1000; // 30 minutos en milisegundos

// Función para mostrar el registro de navegación
function showSesiones() {
  console.log("Registro de navegación web (solo sesiones cerradas):");
  
  Object.entries(sesiones).forEach(([id, sesion], index) => {
    if (!sesion.abierta) {  // Solo mostrar sesiones cerradas
      console.log(`${index + 1}. Sesión ${id}:`);
      sesion.recorrido.forEach((url, recorridoIndex) => {
        console.log(`  ${recorridoIndex + 1}: ${url}`);
      });
    }
  });
}

// Cierra la sesión automáticamente si está inactiva por más de 30 minutos
function scheduleAutoClose(tabId) {
  if (sesiones[tabId]) {
    // Cancela cualquier temporizador existente
    clearTimeout(sesiones[tabId].timeout);

    // Programa un nuevo temporizador
    sesiones[tabId].timeout = setTimeout(() => {
      closeSession(tabId);
      console.log(`Sesión de la pestaña con ID ${tabId} cerrada automáticamente por inactividad`);
      showSesiones();
    }, TIMEOUT_DURATION);
  }
}

// Crea una nueva sesión
function newSesion(tabId) {
  if (sesiones[tabId] === undefined) {
    sesiones[tabId] = {
      recorrido: [],
      abierta: true,
      timeout: null,  // Para almacenar el temporizador
      timeStart: new Date().toISOString()  // Para almacenar el temporizador
    };
    scheduleAutoClose(tabId); // Programa el cierre automático de la sesión
  }
}

// Gestiona la sesión de una pestaña
function managerSession(tabId, url) {
  if (sesiones[tabId] !== undefined && sesiones[tabId].abierta) {
    sesiones[tabId].recorrido.push(url);
    scheduleAutoClose(tabId); // Extiende el tiempo de cierre automático
  }
}

// Cierra la sesión de una pestaña
function closeSession(tabId) {
  if (sesiones[tabId] !== undefined) {
    sesiones[tabId].abierta = false;

    // Limpiar el temporizador para evitar fugas de memoria
    clearTimeout(sesiones[tabId].timeout);

    // Aquí puedes enviar los datos al servidor Flask
    sendDataToFlask(tabId, sesiones[tabId]);
    clearSession(tabId);
  }
}

function clearSession(tabId) {
  if (sesiones[tabId] !== undefined) {
    console.log(`Sesión de la pestaña con ID ${tabId} limpiada`);
    delete sesiones[tabId];
  }
}

// Envía los datos de la sesión cerrada al servidor Flask
function sendDataToFlask(tabId, sesion) {
  fetch('http://127.0.0.1:5000/api/track', { // Cambia la URL según tu servidor Flask
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      tabId: tabId,
      recorrido: sesion.recorrido,
      timeStart: sesion.timeStart,
      timeEnd: new Date().toISOString()
    }),
  })
    .then(response => response.json())
    .then(data => {
      console.log('Datos enviados al servidor Flask:', data);
    })
    .catch((error) => {
      console.error('Error enviando los datos al servidor Flask:', error);
    });
}

// Detectar cuando se crea una nueva pestaña
chrome.tabs.onCreated.addListener(function(tab) {
  newSesion(tab.id);
  console.log(`Se ha creado una nueva pestaña con ID: ${tab.id}`);
});

// Detectar cuando una pestaña cambia de estado o URL
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  if (changeInfo.url && changeInfo.url !== "chrome://newtab/") {
    console.log(`La pestaña con ID ${tabId} ha cambiado de URL a: ${changeInfo.url}`);
    managerSession(tabId, changeInfo.url);
  }
});

// Detectar cuando se cierra una pestaña
chrome.tabs.onRemoved.addListener(function(tabId) {
  closeSession(tabId);
  console.log(`La pestaña con ID ${tabId} ha sido cerrada`);
  showSesiones();
});
