const form = document.querySelector('#login-form');
const usernameInput = document.querySelector('#username');
const passwordInput = document.querySelector('#password');

form.addEventListener('submit', e => {
  e.preventDefault();
  const username = usernameInput.value.trim();
  const password = passwordInput.value.trim();

  if (!username || !password) {
    showError('Por favor ingrese su nombre de usuario y contraseña');
  } else if (username !== 'usuario' || password !== 'contraseña') {
    showError('Nombre de usuario o contraseña incorrectos');
  } else {
    alert('Inicio de sesión exitoso!');
  }
});

function showError(message) {
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error-message';
  errorDiv.innerText = message;
  form.insertBefore(errorDiv, form.firstChild);
  setTimeout(() => {
    errorDiv.remove();
  }, 1000);
}