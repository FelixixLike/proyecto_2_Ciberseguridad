function mostrarFormulario(rol) {
  document.getElementById('selector').style.display = 'none';
  document.getElementById('login-box').style.display = 'block';
  document.getElementById('rolInput').value = rol;

  const titulo = document.getElementById('titulo-formulario');
  titulo.textContent = rol === 'admin' ? 'Ingreso Administrador' : 'Ingreso Usuario';

  const registro = document.getElementById('registro-link');
  registro.style.display = rol === 'usuario' ? 'block' : 'none';
}

function volverSelector() {
  document.getElementById('selector').style.display = 'block';
  document.getElementById('login-box').style.display = 'none';
  document.getElementById('rolInput').value = '';
}
