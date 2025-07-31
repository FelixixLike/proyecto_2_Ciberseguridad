document.getElementById("reservaForm").addEventListener("submit", async function(e) {
  e.preventDefault(); // Evita que la página se recargue

  const form = e.target;

  const ingreso = new Date(form.fechaIngreso.value);
  const salida = new Date(form.fechaSalida.value);
  const precio = parseInt(form.habitacion.value);

  if (isNaN(ingreso) || isNaN(salida) || salida <= ingreso) {
    document.getElementById("mensaje").innerText = "Fechas inválidas. Verifica que la salida sea después del ingreso.";
    return;
  }

  const noches = Math.ceil((salida - ingreso) / (1000 * 60 * 60 * 24));
  const total = noches * precio;

  const data = {
    nombre: form.nombre.value,
    correo: form.correo.value,
    fecha: form.fechaIngreso.value,
    fecha_salida: form.fechaSalida.value,
    noches,
    habitacion: form.habitacion.options[form.habitacion.selectedIndex].text,
    precio,
    total
  };

  try {
    const res = await fetch('/guardar_reserva', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    if (res.ok) {
      alert("✅ Reserva exitosa");
      document.getElementById("mensaje").innerText = "Reserva guardada correctamente.";
      form.reset();
    } else {
      document.getElementById("mensaje").innerText = "Error al guardar la reserva.";
    }
  } catch (error) {
    document.getElementById("mensaje").innerText = "Error de conexión con el servidor.";
  }
});
