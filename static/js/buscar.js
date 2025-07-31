document.addEventListener("DOMContentLoaded", () => {
  cargarReservas();

  // Asociar el evento de clic para buscar por fechas
  const btnBuscar = document.getElementById("btnBuscar");
  if (btnBuscar) {
    btnBuscar.addEventListener("click", buscar);
  }
});

// Carga todas las reservas al abrir la página
async function cargarReservas() {
  try {
    const res = await fetch('/todas_reservas');
    const data = await res.json();
    mostrarReservas(data);
  } catch (error) {
    console.error("Error al cargar reservas:", error);
  }
}

// Busca reservas por fechas
async function buscar() {
  const inicio = document.getElementById("inicio").value;
  const fin = document.getElementById("fin").value;

  if (!inicio || !fin) {
    alert("Por favor selecciona ambas fechas.");
    return;
  }

  try {
    const res = await fetch('/buscar_reservas', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ inicio, fin })
    });
    const data = await res.json();
    mostrarReservas(data);
  } catch (error) {
    console.error("Error al buscar reservas:", error);
  }
}

// Muestra las reservas en la tabla
function mostrarReservas(data) {
  const tbody = document.querySelector("#tabla tbody");
  tbody.innerHTML = "";

  if (!data || data.length === 0) {
    tbody.innerHTML = "<tr><td colspan='7' style='text-align:center; color:gray;'>No se encontraron reservas.</td></tr>";
    return;
  }

  data.forEach(r => {
    const inicio = new Date(r.fecha_ingreso);
    const salida = new Date(r.fecha_salida);
    const diffTime = Math.abs(salida - inicio);
    const noches = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    const total = r.precio * noches;

    const row = `<tr>
      <td data-label='Nombre'>${r.nombre}</td>
      <td data-label='Correo'>${r.correo}</td>
      <td data-label='Fecha Ingreso'>${r.fecha_ingreso}</td>
      <td data-label='Fecha Salida'>${r.fecha_salida}</td>
      <td data-label='Habitación'>${r.tipo_habitacion} - $${r.precio.toLocaleString('es-CO')}</td>
      <td data-label='Noches'>${noches}</td>
      <td data-label='Total'>$${total.toLocaleString('es-CO')}</td>
    </tr>`;
    tbody.innerHTML += row;
  });
}
