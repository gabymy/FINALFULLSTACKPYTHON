document.addEventListener('DOMContentLoaded', () => {
    const turnosForm = document.getElementById('turnos-form');
    const registroForm = document.getElementById('registro-form');
    const turnosLista = document.getElementById('turnos-lista');

    // Manejar el envío del formulario de turnos
    if (turnosForm) {
        turnosForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(turnosForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch(turnosForm.action, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (response.ok) {
                    alert(result.message);
                    turnosForm.reset();
                    cargarTurnos(); // Recargar la lista de turnos
                } else {
                    alert(result.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Hubo un error al registrar el turno.');
            }
        });
    }

    // Manejar el envío del formulario de registro
    if (registroForm) {
        registroForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const formData = new FormData(registroForm);
            const data = Object.fromEntries(formData.entries());

            try {
                const response = await fetch(registroForm.action, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();

                if (response.ok) {
                    alert(result.message);
                    registroForm.reset();
                } else {
                    alert(result.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Hubo un error al registrarse.');
            }
        });
    }

    // Función para cargar los turnos
    async function cargarTurnos() {
        try {
            const response = await fetch('/turnos');
            const turnos = await response.json();

            turnosLista.innerHTML = turnos.map(turno => `
                <li>
                    ${turno.nombre_dueno} - ${turno.nombre_mascota} - ${turno.fecha_turno}
                </li>
            `).join('');
        } catch (error) {
            console.error('Error:', error);
            alert('Hubo un error al cargar los turnos.');
        }
    }

    // Cargar los turnos al iniciar la página
    cargarTurnos();
});
