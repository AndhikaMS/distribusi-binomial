document.getElementById('rubik-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const n = document.getElementById('n').value;
    const p = document.getElementById('p').value;
    const k = document.getElementById('k').value;

    // Kirim permintaan ke server untuk menghitung probabilitas
    fetch('/calculate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `n=${n}&p=${p}&k=${k}`,
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('result');
        const stepsDiv = document.getElementById('steps');

        if (data.error) {
            resultDiv.innerHTML = `<p style="color: red;">${data.error}</p>`;
            stepsDiv.innerHTML = '';
        } else {
            // Tampilkan rumus distribusi binomial
            const binomialFormula = `P(X = k) = \\binom{n}{k} p^k (1-p)^{n-k}`;
            resultDiv.innerHTML = `
                <h3>Rumus Distribusi Binomial:</h3>
                <p>\\(${binomialFormula}\\)</p>
                <h3>Hasil:</h3>
                <p><strong>Probabilitas Kumulatif (P(X ≤ ${k})): ${data.result}</strong></p>
            `;

            // Tampilkan P(X=k) untuk setiap k dari 0 sampai k
            let allPxHtml = '<h3>Hasil P(X=k) untuk setiap k:</h3><ul>';
            data.all_px.forEach(px => {
                allPxHtml += `<li>${px}</li>`;
            });
            allPxHtml += '</ul>';
            resultDiv.innerHTML += allPxHtml;

            // Tampilkan Perhitungan Lengkap P(X=k)
            resultDiv.innerHTML += `
                <h3>Perhitungan Lengkap P(X = ${k}):</h3>
            `;

            // Tambahkan langkah-langkah perhitungan
            let stepsHtml = '<ul>';
            data.steps.forEach(step => {
                stepsHtml += `<li>\\(${step.formula}\\)</li>`;
            });
            stepsHtml += '</ul>';
            stepsDiv.innerHTML = stepsHtml;

            // Render MathJax untuk notasi matematika
            MathJax.typeset();

            // Kirim permintaan ke server untuk mendapatkan plot
            fetch('/plot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `n=${n}&p=${p}&k=${k}`,
            })
            .then(response => response.blob())
            .then(imageBlob => {
                const imageObjectURL = URL.createObjectURL(imageBlob);
                document.getElementById('distribution-plot').src = imageObjectURL;
            });
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
