document.getElementById("reservaForm").addEventListener("submit", async function(e) {
  e.preventDefault();

  const form = e.target;

  const ingreso = new Date(form.fechaIngreso.value);
  const salida = new Date(form.fechaSalida.value);
  const precio = parseFloat(form.habitacion.value);

  // Validación de fechas
  if (isNaN(ingreso) || isNaN(salida) || salida <= ingreso) {
    document.getElementById("mensaje").innerText = "Fechas inválidas. La salida debe ser posterior al ingreso.";
    return;
  }

  // Datos de la reserva (el id_usuario lo agrega el backend desde la sesión)
  const data = {
    fecha_ingreso: form.fechaIngreso.value,
    fecha_salida: form.fechaSalida.value,
    tipo_habitacion: form.habitacion.options[form.habitacion.selectedIndex].text,
    precio: precio
  };

  try {
    const res = await fetch('/guardar_reserva', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const resultado = await res.json();
    if (res.ok) {
      document.getElementById("mensaje").innerText = resultado.mensaje || "Reserva guardada correctamente.";
      alert("✅ ¡Reserva realizada con éxito!");
      form.reset();
    } else {
      document.getElementById("mensaje").innerText = resultado.error || "Error al guardar la reserva.";
    }
  } catch (error) {
    document.getElementById("mensaje").innerText = "Error de conexión con el servidor.";
    console.error("Error al enviar reserva:", error);
  }
});
