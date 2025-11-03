document.addEventListener("DOMContentLoaded", () => {
    const tabla = document.getElementById("tablaUsuarios").querySelector("tbody");
    const mensajeDiv = document.getElementById("mensaje");
    const inputUsuario = document.getElementById("usuario");
    const inputClave = document.getElementById("clave");
    const btnCrear = document.getElementById("crear");

    // Función para mostrar mensaje
    function mostrarMensaje(texto, tipo) {
        mensajeDiv.style.display = "block";
        mensajeDiv.className = "mensaje " + tipo;
        mensajeDiv.textContent = texto;
        setTimeout(() => mensajeDiv.style.display = "none", 3000);
    }

    // Cargar todos los usuarios
    async function cargarUsuarios() {
        tabla.innerHTML = "";
        const resp = await fetch("/api/usuarios");
        const usuarios = await resp.json();

        usuarios.forEach(u => {
            const fila = document.createElement("tr");
            fila.innerHTML = `
                <td>${u.id}</td>
                <td><input type="text" value="${u.usuario}" /></td>
                <td><input type="text" value="${u.clave}" /></td>
                <td>
                    <button class="actualizar" data-id="${u.id}">Actualizar</button>
                    <button class="eliminar" data-id="${u.id}">Eliminar</button>
                </td>
            `;
            tabla.appendChild(fila);
        });
    }

    // Crear usuario
    btnCrear.addEventListener("click", async () => {
        const usuario = inputUsuario.value.trim();
        const clave = inputClave.value.trim();
        if (!usuario || !clave) {
            mostrarMensaje("Usuario y clave son obligatorios", "error");
            return;
        }

        const resp = await fetch("/api/usuarios", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ usuario, clave })
        });
        const data = await resp.json();
        mostrarMensaje(data.mensaje, data.status === "ok" ? "exito" : "error");
        cargarUsuarios();
    });

    // Delegación de eventos para actualizar y eliminar
    tabla.addEventListener("click", async (e) => {
        const id = e.target.dataset.id;
        const fila = e.target.closest("tr");
        if (e.target.classList.contains("actualizar")) {
            const usuario = fila.querySelectorAll("input")[0].value;
            const clave = fila.querySelectorAll("input")[1].value;
            const resp = await fetch(`/api/usuarios/${id}`, {
                method: "PUT",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ usuario, clave })
            });
            const data = await resp.json();
            mostrarMensaje(data.mensaje, data.status === "ok" ? "exito" : "error");
            cargarUsuarios();
        } else if (e.target.classList.contains("eliminar")) {
            const resp = await fetch(`/api/usuarios/${id}`, { method: "DELETE" });
            const data = await resp.json();
            mostrarMensaje(data.mensaje, data.status === "ok" ? "exito" : "error");
            cargarUsuarios();
        }
    });

    // Cargar usuarios al inicio
    cargarUsuarios();
});
