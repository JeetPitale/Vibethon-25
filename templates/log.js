
import { auth, signInWithEmailAndPassword, signOut, onAuthStateChanged } from './firebase.js';

const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');
const emailInput = document.getElementById('login-email');
const passwordInput = document.getElementById('login-password');

loginBtn?.addEventListener('click', () => {
  const email = emailInput.value;
  const password = passwordInput.value;

  signInWithEmailAndPassword(auth, email, password)
    .then((userCredential) => {
      console.log("Logged in:", userCredential.user);
      showMessage('✅ Logged in successfully!', 'success');
    })
    .catch((error) => {
      console.error(error);
      showMessage(`❌ ${error.message}`, 'error');
    });
});

logoutBtn?.addEventListener('click', () => {
  signOut(auth)
    .then(() => {
      showMessage('✅ Logged out!', 'success');
    })
    .catch((error) => {
      console.error(error);
      showMessage(`❌ ${error.message}`, 'error');
    });
});

onAuthStateChanged(auth, (user) => {
  if (user) {
    loginBtn?.classList.add('hidden');
    logoutBtn?.classList.remove('hidden');
  } else {
    loginBtn?.classList.remove('hidden');
    logoutBtn?.classList.add('hidden');
  }
});

