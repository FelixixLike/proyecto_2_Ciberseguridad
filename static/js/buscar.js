document.addEventListener("DOMContentLoaded", cargarReservas);

async function cargarReservas() {
  const res = await fetch('/todas_reservas');
  const data = await res.json();
  mostrarReservas(data);
}

async function buscar() {
  const inicio = document.getElementById("inicio").value;
  const fin = document.getElementById("fin").value;

  if (!inicio || !fin) {
    alert("Por favor selecciona ambas fechas.");
    return;
  }

  const res = await fetch('/buscar_reservas', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ inicio, fin })
  });

  const data = await res.json();
  mostrarReservas(data);
}

function mostrarReservas(data) {
  const tbody = document.querySelector("#tabla tbody");
  tbody.innerHTML = "";

  if (data.length === 0) {
    tbody.innerHTML = "<tr><td colspan='5' style='text-align:center; color:gray;'>No se encontraron reservas.</td></tr>";
    return;
  }

  data.forEach(r => {
    const row = `<tr>
      <td data-label='Nombre'>${r.nombre}</td>
      <td data-label='Correo'>${r.correo}</td>
      <td data-label='Fecha'>${r.fecha}</td>
      <td data-label='Noches'>${r.noches}</td>
      <td data-label='Total'>$${r.total.toLocaleString('es-CO')}</td>
    </tr>`;
    tbody.innerHTML += row;
  });
}
