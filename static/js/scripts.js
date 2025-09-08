// ------------------- Auth / Navbar -------------------
let loggedIn = false;
const navLinks = document.getElementById('navLinks');
const loginModal = document.getElementById('loginModal');
const signupModal = document.getElementById('signupModal');

function openModal(modal) { modal.classList.add('active'); }
function closeModal(modal) { modal.classList.remove('active'); }

function renderAuthLinks() {
    [...navLinks.querySelectorAll('li[data-auth]')].forEach(li => li.remove());

    if (loggedIn) {
        const logoutLi = document.createElement('li');
        logoutLi.setAttribute('data-auth', 'true');
        const logoutLink = document.createElement('a');
        logoutLink.href = "#";
        logoutLink.textContent = "Logout";
        logoutLink.addEventListener('click', e => { e.preventDefault(); logout(); });
        logoutLi.appendChild(logoutLink);
        navLinks.appendChild(logoutLi);
    } else {
        const loginLi = document.createElement('li');
        loginLi.setAttribute('data-auth', 'true');
        const loginLink = document.createElement('a');
        loginLink.href = "#";
        loginLink.textContent = "Login";
        loginLink.addEventListener('click', e => { e.preventDefault(); openModal(loginModal); });
        loginLi.appendChild(loginLink);

        const signupLi = document.createElement('li');
        signupLi.setAttribute('data-auth', 'true');
        const signupLink = document.createElement('a');
        signupLink.href = "#";
        signupLink.textContent = "Sign Up";
        signupLink.addEventListener('click', e => { e.preventDefault(); openModal(signupModal); });
        signupLi.appendChild(signupLink);

        navLinks.appendChild(loginLi);
        navLinks.appendChild(signupLi);
    }
}

function logout() {
    loggedIn = false;
    renderAuthLinks();
    alert('Logged out successfully!');
}

// Close modal buttons
document.getElementById('closeLogin').addEventListener('click', () => closeModal(loginModal));
document.getElementById('closeSignup').addEventListener('click', () => closeModal(signupModal));
window.addEventListener('click', e => {
    if (e.target === loginModal) closeModal(loginModal);
    if (e.target === signupModal) closeModal(signupModal);
});

document.getElementById('loginForm').addEventListener('submit', e => {
    e.preventDefault();
    loggedIn = true;
    closeModal(loginModal);
    renderAuthLinks();
    alert('Logged in successfully!');
});

document.getElementById('signupForm').addEventListener('submit', e => {
    e.preventDefault();
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('signupConfirmPassword').value;
    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }
    loggedIn = true;
    closeModal(signupModal);
    renderAuthLinks();
    alert('Signed up and logged in successfully!');
});

// Initial auth render
renderAuthLinks();

// ------------------- Upload Confirmation -------------------
// document.addEventListener("DOMContentLoaded", () => {
//     const fileInput = document.getElementById("fileInput");
//     const urlInput = document.querySelector("input[name='image_url']");
//     const uploadMessage = document.getElementById("uploadMessage");
//     const scanBtn = document.querySelector(".scan-btn");

//     // Initially disable scan button
//     scanBtn.disabled = true;

//     function updateScanButton() {
//         if ((fileInput.files && fileInput.files.length > 0) || urlInput.value.trim() !== "") {
//             scanBtn.disabled = false;
//         } else {
//             scanBtn.disabled = true;
//         }
//     }

//     // When file is selected
//     fileInput.addEventListener("change", () => {
//         if (fileInput.files && fileInput.files.length > 0) {
//             const fileName = fileInput.files[0].name;
//             uploadMessage.textContent = `✅ Photo uploaded: ${fileName}`;
//             uploadMessage.style.color = "green";
//         } else {
//             uploadMessage.textContent = "";
//         }
//         updateScanButton();
//     });

//     // When URL is typed
//     urlInput.addEventListener("input", () => {
//         if (urlInput.value.trim() !== "") {
//             uploadMessage.textContent = "✅ Image URL entered!";
//             uploadMessage.style.color = "green";
//         } else if (!(fileInput.files && fileInput.files.length > 0)) {
//             uploadMessage.textContent = "";
//         }
//         updateScanButton();
//     });

//     // Prevent submission if nothing selected
//     const uploadForm = document.getElementById("uploadForm");
//     uploadForm.addEventListener("submit", (e) => {
//         if (!(fileInput.files && fileInput.files.length > 0) && urlInput.value.trim() === "") {
//             e.preventDefault();
//             uploadMessage.textContent = "⚠️ Please select an image or enter a URL before scanning!";
//             uploadMessage.style.color = "red";
//             scanBtn.focus();
//         }
//         // Otherwise, allow normal form submission and keep message visible
//     });
// });
