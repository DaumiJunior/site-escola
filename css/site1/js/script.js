
const loginLink = document.getElementById("login-link");
        const loginForm = document.getElementById("login-form");
    
        const cursosLink = document.getElementById("cursos-link");
        const cursosContent = document.getElementById("cursos-content");
    
        loginLink.addEventListener("click", () => {
            loginForm.classList.toggle("hidden");
        });
    
        cursosLink.addEventListener("click", () => {
            cursosContent.classList.toggle("hidden");
        });
    const bibliotecaLink = document.getElementById("biblioteca-link");
            
    bibliotecaLink.addEventListener("click", function(event) {
        event.preventDefault();
        
        // Redirecionar para o link da Biblioteca Virtual
        window.location.href = "https://www.biblion.org.br/";
    });
    document.addEventListener("DOMContentLoaded", function () {
        const commentForm = document.getElementById("new-comment-form");
        const commentList = document.getElementById("comments-ul");

        commentForm.addEventListener("submit", function (event) {
            event.preventDefault();
            
            const nameInput = document.getElementById("comment-name");
            const textInput = document.getElementById("comment-text");

            const name = nameInput.value;
            const text = textInput.value;

            if (name && text) {
                const commentItem = document.createElement("li");
                commentItem.innerHTML = `<strong>${name}:</strong> ${text}`;
                commentList.appendChild(commentItem);

                nameInput.value = "";
                textInput.value = "";
            }
        });
    });const menuButton = document.getElementById('menu-button');
    const menu = document.getElementById('menu');
    const profileLink = document.getElementById('profile-link');
    const profile = document.getElementById('profile');
    
    menuButton.addEventListener('click', () => {
        menu.classList.toggle('hidden');
    });
    
    profileLink.addEventListener('click', () => {
        profile.classList.toggle('hidden');
    });
    