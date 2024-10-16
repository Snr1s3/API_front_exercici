document.addEventListener("DOMContentLoaded", function() {
    // Cridem a l'endpoint de l'API fent un fetch
    fetch('http://127.0.0.1:8000/alumne/list')
        .then(response => {
            if (!response.ok) {
                throw new Error("Error a la resposta del servidor");
            }
            return response.json();
        })
        .then(data => {
            const alumnesTableBody = document.querySelector("#tablaAlumne tbody");
            alumnesTableBody.innerHTML = ""; 
            
            data.forEach(alumne => {
                const row = document.createElement("tr");

                const nomAluCell = document.createElement("td");
                nomAluCell.textContent = alumne.NomAlumne;
                row.appendChild(nomAluCell);

                const cicle= document.createElement("td");
                cicle.textContent = alumne.Cicle;
                row.appendChild(cicle);
                const curs = document.createElement("td");
                curs.textContent = alumne.Curs;
                row.appendChild(curs);
                const grup = document.createElement("td");
                grup.textContent = alumne.Grup;
                row.appendChild(grup);
                const aula = document.createElement("td");
                aula.textContent = alumne.DescAula;
                row.appendChild(aula);
                alumnesTableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error("Error capturat:", error);
            alert("Error al carregar la llista d'alumnes");
        });
});