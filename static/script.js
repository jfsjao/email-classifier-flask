document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("modal").style.display = "none";
    carregarHistorico();

    document.getElementById("emailForm").addEventListener("submit", function(event) {
        event.preventDefault();
        let formData = new FormData(this);
        
        fetch("/email/process", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.erro) {
                document.getElementById("resultado").innerHTML = `<p style='color:red'>${data.erro}</p>`;
            } else {
                document.getElementById("resultado").innerHTML = `
                    <h3>Classificação: ${data.categoria}</h3>
                    <p><strong>Assunto:</strong> ${data.assunto}</p>
                    <p><strong>Resposta:</strong> ${data.resposta}</p>
                `;

                adicionarAoHistorico(data.assunto, data.categoria, data.email, data.resposta);

                document.getElementById("email").value = "";
                document.getElementById("file").value = "";
            }
        });
    });

    function carregarHistorico() {
        let historicoSalvo = JSON.parse(localStorage.getItem("historicoEmails")) || [];
        let historico = document.getElementById("historico");
        historico.innerHTML = "";

        historicoSalvo.forEach(item => {
            let newItem = criarItemHistorico(item.assunto, item.categoria, item.email, item.resposta);
            historico.appendChild(newItem);
        });
    }

    function adicionarAoHistorico(assunto, categoria, email, resposta) {
        let historicoSalvo = JSON.parse(localStorage.getItem("historicoEmails")) || [];
        if (historicoSalvo.length >= 5) historicoSalvo.shift();
        let novoItem = { assunto, categoria, email, resposta };
        historicoSalvo.push(novoItem);
        localStorage.setItem("historicoEmails", JSON.stringify(historicoSalvo));
        let historico = document.getElementById("historico");
        let newItem = criarItemHistorico(assunto, categoria, email, resposta);
        historico.appendChild(newItem);
    }

    function criarItemHistorico(assunto, categoria, email, resposta) {
        let newItem = document.createElement("li");
        newItem.setAttribute("data-email", email);
        newItem.setAttribute("data-resposta", resposta);
        newItem.innerHTML = `<strong>${assunto}</strong> - ${categoria}`;
        newItem.addEventListener("click", function() {
            mostrarDetalhes(email, resposta);
        });
        return newItem;
    }

    function mostrarDetalhes(email, resposta) {
        document.getElementById("emailDetalhes").innerText = email;
        document.getElementById("respostaDetalhes").innerHTML = resposta;
        document.getElementById("modal").style.display = "flex";
    }

    document.querySelector(".close").addEventListener("click", function() {
        document.getElementById("modal").style.display = "none";
    });

    window.onclick = function(event) {
        let modal = document.getElementById("modal");
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };

    document.getElementById("clearHistory").addEventListener("click", function() {
        localStorage.removeItem("historicoEmails");
        document.getElementById("historico").innerHTML = "";
        document.getElementById("resultado").innerHTML = "";
    });
});
