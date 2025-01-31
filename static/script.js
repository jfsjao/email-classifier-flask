document.addEventListener("DOMContentLoaded", function() {
    // Garante que o modal comece oculto
    document.getElementById("modal").style.display = "none";

    // Carrega histórico salvo no localStorage ao iniciar
    carregarHistorico();

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

                // Adiciona novo item ao histórico no navegador
                adicionarAoHistorico(data.assunto, data.categoria, data.email, data.resposta);

                // Limpar campos após classificação
                document.getElementById("email").value = "";
                document.getElementById("file").value = "";
            }
        });
    });

    // Função para carregar histórico salvo no navegador
    function carregarHistorico() {
        let historicoSalvo = JSON.parse(localStorage.getItem("historicoEmails")) || [];
        let historico = document.getElementById("historico");

        // Limpa o HTML antes de adicionar novos itens
        historico.innerHTML = "";

        historicoSalvo.forEach(item => {
            let newItem = criarItemHistorico(item.assunto, item.categoria, item.email, item.resposta);
            historico.appendChild(newItem);
        });
    }

    // Função para adicionar itens ao histórico (mantendo até 5 registros)
    function adicionarAoHistorico(assunto, categoria, email, resposta) {
        let historicoSalvo = JSON.parse(localStorage.getItem("historicoEmails")) || [];

        // Mantém no máximo 5 registros no histórico
        if (historicoSalvo.length >= 5) {
            historicoSalvo.shift(); // Remove o mais antigo
        }

        let novoItem = { assunto, categoria, email, resposta };
        historicoSalvo.push(novoItem);
        localStorage.setItem("historicoEmails", JSON.stringify(historicoSalvo));

        // Atualiza a lista de histórico
        let historico = document.getElementById("historico");
        let newItem = criarItemHistorico(assunto, categoria, email, resposta);
        historico.appendChild(newItem);
    }

    // Função auxiliar para criar um item de histórico com evento de clique
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

    // Função para exibir detalhes no modal
    function mostrarDetalhes(email, resposta) {
        document.getElementById("emailDetalhes").innerText = email;
        document.getElementById("respostaDetalhes").innerText = resposta;
        document.getElementById("modal").style.display = "flex";
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

    // Botão para limpar histórico temporário (somente do usuário)
    document.getElementById("clearHistory").addEventListener("click", function() {
        localStorage.removeItem("historicoEmails");
        document.getElementById("historico").innerHTML = "";
        document.getElementById("resultado").innerHTML = "";
    });
});
