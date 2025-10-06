document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('carForm');
  const resultsSection = document.getElementById('resposta-box');
  const resultsWrapper = document.getElementById('results');
  const modoValidacao = document.getElementById('modoValidacao');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    resultsWrapper.style.display = 'block';
    resultsSection.innerHTML = '<p class="loading">🔄 Verificando dados...</p>';

    const formData = {
      modelo: document.getElementById('modelo').value.trim().toLowerCase(),
      marca: document.getElementById('marca').value.trim().toLowerCase(),
      ano: document.getElementById('ano').value.trim(),
      potencia: document.getElementById('potencia').value.trim(),
      carroceria: document.getElementById('carroceria').value.trim().toLowerCase()
    };

    try {
      const response = await fetch('/validar-carro', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      const contentType = response.headers.get('content-type');

      if (contentType.includes('application/json')) {
        const json = await response.json();

        if (json.resultado?.includes('✅')) {
          resultsSection.innerHTML = `<p class="valid">✅ ${json.resultado}</p>`;
        } else if (json.resultado?.includes('❌')) {
          const erros = json.erros?.map(e => 
            `<li><strong>${e.campo}</strong>: jogo=${e.jogo}, real=${e.real}</li>`
          ).join('');
          resultsSection.innerHTML = `<p class="invalid">❌ ${json.resultado}</p><ul>${erros}</ul>`;
        } else {
          resultsSection.innerHTML = `<p>${JSON.stringify(json)}</p>`;
        }

      } else {
        const texto = await response.text();

        if (texto.includes('✅')) {
          resultsSection.innerHTML = `<p class="valid">✅ ${texto}</p>`;
        } else if (texto.includes('❌')) {
          resultsSection.innerHTML = `<p class="invalid">❌ ${texto}</p>`;
        } else {
          resultsSection.innerHTML = `<p>${texto}</p>`;
        }
      }

    } catch (error) {
      resultsSection.innerHTML = `<p class="invalid">❌ Ocorreu um erro: ${error.message}</p>`;
      console.error('Erro na requisição:', error);
    }
  });
});
