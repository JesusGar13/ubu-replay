console.log("Background script running");

let sesiones = {};

// Función para mostrar el registro de navegación
function showSesiones() {
  console.log("Registro de navegación web (solo sesiones cerradas):");
  
  Object.entries(sesiones).forEach(([id, sesion], index) => {
    if (!sesion.abierta) {  // Solo mostrar sesiones cerradas
      console.log(`${index+1}. Sesión ${id}:`);
      sesion.recorrido.forEach((url, recorridoIndex) => {
        console.log(`  ${recorridoIndex + 1}: ${url}`);
      });
    }
  });
}

// Crea una nueva sesion. Si ya existe, no hace nada
function newSesion(tabId) {
  if (sesiones[tabId] === undefined) {
    sesiones[tabId] = {
      recorrido: [],
      abierta: true
    };
  }
}

// Gestiona la sesion de una pestaña, definimos la url si no esta definida,
// si ya esta definida, agregamos la url al recorrido
function managerSession(tabId, url) {
  if (sesiones[tabId] !== undefined && sesiones[tabId].abierta) {
    sesiones[tabId].recorrido.push(url);
  }
}

// Cierra la sesión de una pestaña
function closeSession(tabId) {
  if (sesiones[tabId] !== undefined) {
    sesiones[tabId].abierta = false;
  }
}

// ################################################################################################################

// Detectar cuando se crea una nueva pestaña
chrome.tabs.onCreated.addListener(function(tab) {
  newSesion(tab.id);
  console.log(`Se ha creado una nueva pestaña con ID: ${tab.id}`);
});

// Detectar cuando una pestaña cambia de estado o URL
chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
  // Verificamos que la URL esté definida y no sea la URL de nueva pestaña
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
