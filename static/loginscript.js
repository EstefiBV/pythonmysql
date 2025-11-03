document.addEventListener("DOMContentLoaded", () => {

    const formulario = document.getElementById("formLogin");
    const usuarioInput = document.getElementById("usuario");
    const claveInput = document.getElementById("clave");
    const terminal = document.getElementById("terminal");
    const tituloh2 = document.getElementById("titulo");
    const mensajeDiv = document.getElementById("mensaje");

    tituloh2.addEventListener("mouseover", () => {
        tituloh2.style.color = "green";
    });
    tituloh2.addEventListener("mouseout", () => {
        tituloh2.style.color = "";
    });

    formulario.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append("usuario", usuarioInput.value.trim());
        formData.append("clave", claveInput.value.trim());

        try {
            const respuesta = await fetch("/login", {
                method: "POST",
                body: formData
            });
            const data = await respuesta.json();

            mensajeDiv.style.display = "block"; // mostrar el div
            if (data.status === "ok") {
                mensajeDiv.className = "mensaje exito";
                mensajeDiv.textContent = `✅ Sesión iniciada.`;
                // Espera 1 segundo antes de redirigir
                setTimeout(() => {
                    window.location.href = "/usuarios"; // tu ruta de Flask
                }, 1000);
            } else {
                mensajeDiv.className = "mensaje error";
                mensajeDiv.textContent = `❌ ${data.mensaje}`;
            }
        } catch (error) {
            terminal.textContent = `Error en el servidor`;
        }

    });

});