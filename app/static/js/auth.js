import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.1/firebase-app.js";
import {
  getAuth,
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
} from "https://www.gstatic.com/firebasejs/10.8.1/firebase-auth.js";

// Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyA2Q_FXrpQfcJfdzxN6IX5R0wmxB9TxAwg",
  authDomain: "learning-hub-6ef7d.firebaseapp.com",
  projectId: "learning-hub-6ef7d",
  storageBucket: "learning-hub-6ef7d.appspot.com",
  messagingSenderId: "983490369054",
  appId: "1:983490369054:web:539506b7fbc269c163400f"
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Signup
const signup = () => {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  createUserWithEmailAndPassword(auth, email, password)
    .then(async (userCredential) => {
      document.getElementById("auth-message").innerText = "Signup successful!";
      const token = await userCredential.user.getIdToken();
      await sendTokenToBackend(token);
      window.location.href = "/";
    })
    .catch((error) => {
      document.getElementById("auth-message").innerText = error.message;
    });
};

// Login
const login = () => {
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  signInWithEmailAndPassword(auth, email, password)
    .then(async (userCredential) => {
      document.getElementById("auth-message").innerText = "Login successful!";
      const token = await userCredential.user.getIdToken();
      await sendTokenToBackend(token);
      window.location.href = "/";
    })
    .catch((error) => {
      document.getElementById("auth-message").innerText = error.message;
    });
};

// Logout
const logout = () => {
  signOut(auth)
    .then(() => {
      document.getElementById("auth-message").innerText = "Logged out!";
      localStorage.removeItem("firebase_token");
    })
    .catch((error) => {
      document.getElementById("auth-message").innerText = error.message;
    });
};

// Send token to Flask backend
const sendTokenToBackend = async (token) => {
  try {
    const res = await fetch("/verify-token", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ token })
    });

    const data = await res.json();

    if (res.ok) {
      console.log("✅ Token verified on server:", data);
    } else {
      console.error("❌ Server rejected token:", data);
      alert("Failed to verify login.");
    }
  } catch (err) {
    console.error("❌ Error verifying token:", err);
  }
};

// Attach to buttons
document.getElementById("loginBtn").addEventListener("click", login);
document.getElementById("signupBtn").addEventListener("click", signup);
document.getElementById("logoutBtn")?.addEventListener("click", logout);
fetch('/logout', { method: 'POST' });