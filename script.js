document.getElementById('travelForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const question = document.getElementById('question').value;

    const responseContainer = document.getElementById('responseContainer');
    const responseElement = document.getElementById('response');
    responseElement.innerHTML = 'Carregando...';

    try {
        const response = await fetch('http://localhost:8080/http://api-travelagent-232686593.us-east-2.elb.amazonaws.com', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });

        if (!response.ok) {
            throw new Error('Erro na requisição: ' + response.statusText);
        }

        const data = await response.json();
        responseElement.innerHTML = formatResponse(data.details);
    } catch (error) {
        responseElement.textContent = 'Ocorreu um erro: ' + error.message;
    }
});

function formatResponse(details) {
    // Substitui caracteres especiais
    details = details.replace(/\\u00e3/g, 'ã').replace(/\\u00e7/g, 'ç').replace(/\\u00e9/g, 'é').replace(/\\u00f5/g, 'õ').replace(/\\u00ed/g, 'í');

    // Divide o texto em linhas e coloca dentro de parágrafos
    const formattedDetails = details.split('\n\n').map(paragraph => `<p>${paragraph}</p>`).join('');

    return formattedDetails;
}
