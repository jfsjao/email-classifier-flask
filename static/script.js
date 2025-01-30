document.addEventListener("DOMContentLoaded", function() {
    // Garante que o modal comece oculto
    document.getElementById("modal").style.display = "none";

    // Adiciona evento ao formulário de envio
    document.getElementById("emailForm").addEventListener("submit", function(event) {
        event.preventDefault();
        
        let formData = new FormData(this);
        
        fetch("/process", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.erro) {
                document.getElementById("resultado").innerHTML = "<p style='color:red'>" + data.erro + "</p>";
            } else {
                document.getElementById("resultado").innerHTML = `
                    <h3>Classificação: ${data.categoria}</h3>
                    <p><strong>Resposta:</strong> ${data.resposta}</p>
                `;

                // Adiciona novo item ao histórico
                adicionarAoHistorico(data.assunto, data.categoria, data.email, data.resposta);

                // Limpar campos após classificação
                document.getElementById("email").value = "";
                document.getElementById("file").value = "";
            }
        });
    });

    // Função para adicionar itens ao histórico com evento de clique
    function adicionarAoHistorico(assunto, categoria, email, resposta) {
        let historico = document.getElementById("historico");
        let newItem = document.createElement("li");
        newItem.setAttribute("data-email", email);
        newItem.setAttribute("data-resposta", resposta);
        newItem.innerHTML = `<strong>${assunto}</strong> - ${categoria}`;
        
        newItem.onclick = function() {
            mostrarDetalhes(email, resposta);
        };
        
        historico.appendChild(newItem);
    }

    // Adiciona eventos de clique nos itens do histórico carregado
    document.querySelectorAll("#historico li").forEach(item => {
        item.addEventListener("click", function() {
            let email = this.getAttribute("data-email");
            let resposta = this.getAttribute("data-resposta");
            mostrarDetalhes(email, resposta);
        });
    });

    // Botão de limpar histórico
    document.getElementById("clearHistory").addEventListener("click", function() {
        fetch("/clear_history", { method: "POST" })
        .then(response => response.json())
        .then(data => {
            alert(data.mensagem);
            document.getElementById("historico").innerHTML = "";
            document.getElementById("resultado").innerHTML = "";
        });
    });

    // Função para exibir detalhes no modal
    function mostrarDetalhes(email, resposta) {
        document.getElementById("emailDetalhes").innerText = email;
        document.getElementById("respostaDetalhes").innerText = resposta;
        document.getElementById("modal").style.display = "flex"; // Garante que o modal aparece corretamente
    }

    // Fechar modal ao clicar no botão de fechar
    document.querySelector(".close").addEventListener("click", function() {
        document.getElementById("modal").style.display = "none";
    });

    // Fecha o modal se o usuário clicar fora dele
    window.onclick = function(event) {
        let modal = document.getElementById("modal");
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
});
