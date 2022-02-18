const body = document.querySelector("body"),
    sidebar = body.querySelector(".sidebar"),
    toggle = body.querySelector(".toggle"),
    searchBtn = body.querySelector(".search-box"),
    modeSwitch = body.querySelector(".toggle-switch"),
    modeText = body.querySelector(".mode-text");

if (!localStorage.theme) localStorage.theme = "dark"
document.body.className = localStorage.theme
modeText.innerText = document.body.classList.contains("dark") ? "Light Mode" : "Dark Mode"

    toggle.addEventListener("click", () =>{
        sidebar.classList.toggle("close");
    });
    searchBtn.addEventListener("click", () =>{
        sidebar.classList.remove("close");
    });

    modeSwitch.addEventListener("click", () =>{
        body.classList.toggle("dark");
        localStorage.theme = document.body.className || "light"

        if(body.classList.contains("dark")){
            modeText.innerText = "Light Mode"
        }else{
            modeText.innerText = "Dark Mode"
        }
    });
