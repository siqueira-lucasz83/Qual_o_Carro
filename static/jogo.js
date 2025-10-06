document.addEventListener('DOMContentLoaded', () => {
  const jogoForm = document.getElementById('jogo-form');
  const feedback = document.getElementById('feedback');
  const dicasDiv = document.getElementById('dicas');
  const voltarMenu = document.getElementById('voltar-menu');

  let tentativas = 0;

  jogoForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const palpite = document.getElementById('palpite').value;

    const resposta = await fetch('/palpite', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ palpite })
    });

    const data = await resposta.json();

    if (data.acertou) {
      feedback.innerHTML = `🎉 Parabéns! Você acertou: era o ${data.carro} 🚗. Você ganhou ${data.pontos} pontos!`;
      feedback.style.color = '#28a745';
      jogoForm.style.display = 'none';
      voltarMenu.style.display = 'block';
      return;
    }

    feedback.innerHTML = '❌ Errou!';
    feedback.style.color = '#dc3545';
    tentativas++;

    if (tentativas < 4) {
      const carroAtual = await fetch('/carro-dica');
      const carroData = await carroAtual.json();

      if (tentativas === 1) {
        dicasDiv.innerHTML += `<p><strong>Dica 2:</strong> Ano de fabricação -> ${carroData.ano}</p>`;
      } else if (tentativas === 2) {
        dicasDiv.innerHTML += `<p><strong>Dica 3:</strong> Potência -> ${carroData.potencia} CV</p>`;
      } else if (tentativas === 3) {
        dicasDiv.innerHTML += `<p><strong>Dica 4:</strong> Tipo de carroceria -> ${carroData.carroceria}</p>`;
      }
    } else {
      const carroAtual = await fetch('/carro-dica');
      const carroData = await carroAtual.json();

      feedback.innerHTML += `<br>😢 Suas tentativas acabaram. O carro era ${carroData.modelo}.`;
      jogoForm.style.display = 'none';
      voltarMenu.style.display = 'block';
    }
  });
});
