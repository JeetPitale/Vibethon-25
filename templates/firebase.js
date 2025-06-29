// Import Firebase modules (must use this only in a module-based environment like index.html using <script type="module">)
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.9.1/firebase-app.js";
import { getAuth, onAuthStateChanged, signInWithEmailAndPassword, createUserWithEmailAndPassword, signOut } from "https://www.gstatic.com/firebasejs/11.9.1/firebase-auth.js";

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyC0_RD1C50XZFDa8QGHR2xYGDMQ_0utRyw",
  authDomain: "exam-whispers.firebaseapp.com",
  projectId: "exam-whispers",
  storageBucket: "exam-whispers.appspot.com",
  messagingSenderId: "438582593358",
  appId: "1:438582593358:web:2688a6ded26cc275cbc01f",
  measurementId: "G-GRKQHX9DN1"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Elements
const loginBtn = document.getElementById('login-btn');
const logoutBtn = document.getElementById('logout-btn');
const sidebarLogoutBtn = document.getElementById('sidebar-logout-btn');
const emailInput = document.getElementById('login-email');
const passwordInput = document.getElementById('login-password');
const authTitle = document.getElementById('auth-title');
const authActionBtn = document.getElementById('auth-action-btn');
const toggleAuthModeBtn = document.getElementById('toggle-auth-mode');
const toggleMessage = document.getElementById('toggle-message');

let isLoginMode = true;

authActionBtn?.addEventListener('click', () => {
  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();

  if (!email || !password) {
    showMessage("Enter email and password", "error");
    return;
  }

  if (isLoginMode) {
    signInWithEmailAndPassword(auth, email, password)
      .then(() => {
        showMessage("✅ Logged in!", "success");
        activatePage("home");
        document.querySelector(".flex.justify-center.items-center.h-screen")?.remove();
      })
      .catch((error) => showMessage("❌ " + error.message, "error"));
  } else {
    createUserWithEmailAndPassword(auth, email, password)
      .then(() => {
        showMessage("✅ Account created!", "success");
        activatePage("home");
        document.querySelector(".flex.justify-center.items-center.h-screen")?.remove();
      })
      .catch((error) => showMessage("❌ " + error.message, "error"));
  }
});

toggleAuthModeBtn?.addEventListener('click', () => {
  isLoginMode = !isLoginMode;
  authTitle.textContent = isLoginMode ? "Login" : "Sign Up";
  authActionBtn.textContent = isLoginMode ? "Login" : "Sign Up";
  toggleMessage.textContent = isLoginMode ? "Don't have an account?" : "Already have an account?";
  toggleAuthModeBtn.textContent = isLoginMode ? "Sign up" : "Login";
});

// Logout
const doLogout = () => {
  signOut(auth)
    .then(() => {
      showMessage("✅ Logged out", "success");
    })
    .catch((error) => {
      console.error("Logout error:", error);
      showMessage("❌ " + error.message, "error");
    });
};

logoutBtn?.addEventListener('click', doLogout);
sidebarLogoutBtn?.addEventListener('click', doLogout);

// Auth State Listener
onAuthStateChanged(auth, (user) => {
  const loginSection = document.querySelector(".flex.justify-center.items-center.h-screen");

  if (user) {
    loginSection?.classList.add("hidden");
    activatePage("home");
  } else {
    loginSection?.classList.remove("hidden");
    pages.forEach(p => p.classList.remove("active"));
  }
});
