function mostrarFormulario(rol) {
  document.getElementById('selector').style.display = 'none';
  document.getElementById('login-box').style.display = 'block';
  document.getElementById('rolInput').value = rol;

  // Mostrar título según rol
  const titulo = document.getElementById('titulo-formulario');
  titulo.textContent = rol === 'admin' ? 'Ingreso Administrador' : 'Ingreso Usuario';

  // Mostrar o no el enlace de registro
  const registro = document.getElementById('registro-link');
  if (rol === 'usuario') {
    registro.style.display = 'block';
  } else {
    registro.style.display = 'none';
  }
}

function volverSelector() {
  document.getElementById('selector').style.display = 'block';
  document.getElementById('login-box').style.display = 'none';
}
