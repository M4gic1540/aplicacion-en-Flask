const resetForm = document.getElementById('reset-form');
const emailInput = document.getElementById('email');
const successMessage = document.getElementById('reset-success');
const errorMessage = document.getElementById('reset-error');

resetForm.addEventListener('submit', (event) => {
  event.preventDefault();
  const email = emailInput.value.trim();
  if (!isValidEmail(email)) {
    showError('Por favor, introduce un correo electrónico válido.');
    return;
  }
  // Si se llega aquí, se envía el correo electrónico para restablecer la contraseña
  sendResetEmail(email)
    .then(() => {
      showSuccess();
    })
    .catch(() => {
      showError('Ha ocurrido un error. Por favor, inténtelo de nuevo más tarde.');
    });
});

function isValidEmail(email) {
  const emailRegex = /^\S+@\S+\.\S+$/;
  return emailRegex.test(email);
}

function showError(message) {
  errorMessage.innerText = message;
  errorMessage.style.display = 'block';
  successMessage.style.display = 'none';
}

function showSuccess() {
  successMessage.style.display = 'block';
  errorMessage.style.display = 'none';
}

function sendResetEmail(email) {
  // Aquí se llamaría a una función que enviaría el correo electrónico para restablecer la contraseña
  // Utilizando la librería Mailjet-sendemail o cualquier otra
  return Mailjet.sendEmail({
    to: email,
    subject: 'Restablecer contraseña',
    text: 'Por favor, haz clic en el siguiente enlace para restablecer tu contraseña: https://miweb.com/restablecer-contrasena'
  });
}

