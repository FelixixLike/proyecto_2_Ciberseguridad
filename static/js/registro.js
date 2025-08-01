document.addEventListener('DOMContentLoaded', function () {
  const passwordInput = document.getElementById('password');
  const form = document.getElementById('formulario');

  function validarPassword(password) {
    const tieneLongitud = password.length >= 8;
    const tieneNumeros = (password.match(/\d/g) || []).length >= 2;
    const tieneSimbolos = /[!@#$%^&*(),.?":{}|<>_\-+=/\\[\]]/.test(password);
    const tieneMayusculas = /[A-Z]/.test(password);
    const tieneMinusculas = /[a-z]/.test(password);

    return tieneLongitud && tieneNumeros && tieneSimbolos && tieneMayusculas && tieneMinusculas;
  }

  passwordInput.addEventListener('input', function () {
    const password = passwordInput.value;

    const tieneLongitud = password.length >= 8;
    const tieneNumeros = (password.match(/\d/g) || []).length >= 2;
    const tieneSimbolos = /[!@#$%^&*(),.?":{}|<>_\-+=/\\[\]]/.test(password);
    const tieneMayusculas = /[A-Z]/.test(password);
    const tieneMinusculas = /[a-z]/.test(password);

    function actualizarEstado(id, valido) {
      const elemento = document.getElementById(id);
      if (valido) {
        elemento.textContent = '✅ ' + elemento.textContent.slice(2);
        elemento.style.color = 'green';
      } else {
        elemento.textContent = '❌ ' + elemento.textContent.slice(2);
        elemento.style.color = 'red';
      }
    }

    actualizarEstado('longitud', tieneLongitud);
    actualizarEstado('numeros', tieneNumeros);
    actualizarEstado('simbolos', tieneSimbolos);
    actualizarEstado('mayusculas', tieneMayusculas);
    actualizarEstado('minusculas', tieneMinusculas);
  });

  form.addEventListener('submit', function (event) {
    const password = passwordInput.value;

    if (!validarPassword(password)) {
      event.preventDefault(); // ❌ Evita el envío
      alert('La contraseña no cumple con los requisitos.');
    }
  });
});
