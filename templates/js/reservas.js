document.addEventListener("DOMContentLoaded", function () {
  const boton = document.getElementById("generar-btn");
  const container = document.getElementById("habitaciones-container");
  const totalHabitaciones = 10;

  boton.addEventListener("click", function () {
    boton.style.display = "none"; // Ocultar boton

    let habitacion = 101;

    while (habitacion < 101 + totalHabitaciones) {
      const div = document.createElement("div");
      div.classList.add("habitacion");
      div.textContent = `Habitacion #${habitacion}`;
      div.dataset.numero = habitacion;

      if (habitacion % 2 === 0) {
        div.classList.add("ocupada");
        div.textContent += " (Ocupada)";
      } else {
        div.classList.add("libre");
        div.addEventListener("click", reservarHabitacion);
      }

      container.appendChild(div);
      habitacion++;
    }
  });

  function reservarHabitacion(e) {
    const habitacion = e.target;
    habitacion.classList.remove("libre");
    habitacion.classList.add("ocupada");
    habitacion.textContent = `Habitacion #${habitacion.dataset.numero} (Reservada)`;
    habitacion.removeEventListener("click", reservarHabitacion);
    alert("Reserva exitosa! Gracias por elegirnos.");
  }
});

