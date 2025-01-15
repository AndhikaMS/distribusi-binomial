document.addEventListener("DOMContentLoaded", function() {
    MathJax.typeset();
    {% if pmf_data %}
    // Grafik PMF
    var ctxPmf = document.getElementById('pmfChart').getContext('2d');
    var pmfChart = new Chart(ctxPmf, {
        type: 'bar',
        data: {
            labels: [{% for k in range(trials + 1) %} 'Keberhasilan {{k}}', {% endfor %}],
            datasets: [{
                label: 'PMF (Probability Mass Function)',
                data: {{ pmf_data | tojson }},
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    {% endif %}

    {% if cdf_data %}
    // Grafik CDF
    var ctxCdf = document.getElementById('cdfChart').getContext('2d');
    var cdfChart = new Chart(ctxCdf, {
        type: 'line',
        data: {
            labels: [{% for k in range(trials + 1) %} 'Keberhasilan {{k}}', {% endfor %}],
            datasets: [{
                label: 'CDF (Cumulative Distribution Function)',
                data: {{ cdf_data | tojson }},
                fill: false,
                borderColor: 'rgba(75, 192, 192, 1)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    {% endif %}
});
