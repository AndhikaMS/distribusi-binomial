from flask import Flask, render_template, request, jsonify, send_file
import math
from math import comb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Fungsi untuk menghitung kombinasi (nCk)
def combination(n, k):
    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))

# Fungsi untuk menghitung probabilitas binomial
def binomial_probability(n, p, k):
    nCk = combination(n, k)
    return nCk * (p ** k) * ((1 - p) ** (n - k))

# Fungsi untuk menghitung probabilitas kumulatif P(X ≤ k)
def cumulative_binomial_probability(n, p, k):
    total_prob = 0
    steps = []

    for i in range(k + 1):
        prob = binomial_probability(n, p, i)
        steps.append({
            'k': i,
            'combination': comb(n, i),
            'probability': round(prob, 5),
            'formula': f'P(X={i})=\\binom{{{n}}}{{{i}}}({p})^{i}(1-{p})^{{{n-i}}}'
        })
        total_prob += prob

    return round(total_prob, 5), steps

# Fungsi untuk menghitung PMF dan CDF
def calculate_pmf_cdf(n, p):
    pmf = [binomial_probability(n, p, k) for k in range(n + 1)]
    cdf = [sum(pmf[:k + 1]) for k in range(n + 1)]
    return pmf, cdf

# Fungsi untuk membuat plot dengan garis vertikal k
def plot_distribution(n, p, k):
    pmf, cdf = calculate_pmf_cdf(n, p)

    # Plot PMF
    plt.figure(figsize=(10, 10))

    plt.subplot(2, 1, 1)
    plt.bar(range(n + 1), pmf, color='blue', alpha=0.7)
    plt.axvline(x=k, color='red', linestyle='--', label=f'k = {k}')
    plt.title('Fungsi Massa Probabilitas (PMF)')
    plt.xlabel('k (Jumlah Keberhasilan)')
    plt.ylabel('Probabilitas')
    plt.legend()

    # Plot CDF
    plt.subplot(2, 1, 2)
    plt.plot(range(n + 1), cdf, marker='o', color='green')
    plt.axvline(x=k, color='red', linestyle='--', label=f'k = {k}')
    plt.title('Fungsi Distribusi Kumulatif (CDF)')
    plt.xlabel('k (Jumlah Keberhasilan)')
    plt.ylabel('Probabilitas Kumulatif')
    plt.legend()

    # Simpan gambar ke buffer
    buffer = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()
    return buffer

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk kalkulasi probabilitas
@app.route('/calculate', methods=['POST'])
def calculate():
    n = int(request.form['n'])
    p = float(request.form['p'])
    k = int(request.form['k'])

    # Hitung probabilitas kumulatif P(X ≤ k)
    total_prob = sum(binomial_probability(n, p, i) for i in range(k + 1))

    # Hitung P(X = k)
    px_k = binomial_probability(n, p, k)

    # Perhitungan lengkap untuk P(X = k)
    nCk = combination(n, k)
    initial_formula = f"P(X = {k}) = \\binom{{{n}}}{{{k}}} \\times {p}^{k} \\times (1 - {p})^{{{n - k}}}"
    step1 = f"\\binom{{{n}}}{{{k}}} = \\frac{{{n}!}}{{{k}!({n}-{k})!}} = {nCk}"
    step2 = f"P(X = {k}) = {nCk} \\times ({p})^{k} \\times (1 - {p})^{{{n - k}}}"
    step3 = f"{nCk} \\times ({p}^{k}) \\times ({1 - p})^{n - k}"
    step4 = f"{nCk} \\times {p ** k:.5f} \\times {(1 - p) ** (n - k):.5f}"
    final_result = f"{px_k:.4f}"

    # Menghitung P(X=k) untuk semua nilai k dari 0 sampai k
    all_px = []
    for i in range(k + 1):
        all_px.append(f"P(X = {i}) = {binomial_probability(n, p, i):.4f}")

    steps = [
        {"formula": initial_formula},
        {"formula": step1},
        {"formula": step2},
        {"formula": step3},
        {"formula": step4},
        {"formula": f"P(X = {k}) = {final_result}"},
    ]

    return jsonify(result=f"{total_prob:.4f}", px_k=f"{final_result}", steps=steps, all_px=all_px)


# Route untuk menampilkan plot
@app.route('/plot', methods=['POST'])
def plot():
    n = int(request.form['n'])
    p = float(request.form['p'])
    k = int(request.form['k'])

    # Hitung nilai PMF dan CDF
    pmf = [binomial_probability(n, p, i) for i in range(n + 1)]
    cdf = [sum(pmf[:i + 1]) for i in range(n + 1)]

    # Buat plot
    fig, ax = plt.subplots(2, 1, figsize=(8, 12))

    # Plot PMF
    ax[0].bar(range(n + 1), pmf, color='skyblue')
    ax[0].axvline(x=k, color='red', linestyle='--', label=f'k = {k}')
    ax[0].set_title('Probability Mass Function (PMF)')
    ax[0].set_xlabel('k')
    ax[0].set_ylabel('P(X = k)')
    ax[0].legend()

    # Plot CDF
    ax[1].plot(range(n + 1), cdf, marker='o', color='green')
    ax[1].axvline(x=k, color='red', linestyle='--', label=f'k = {k}')
    ax[1].set_title('Cumulative Distribution Function (CDF)')
    ax[1].set_xlabel('k')
    ax[1].set_ylabel('P(X ≤ k)')
    ax[1].legend()

    # Simpan plot ke dalam buffer
    buf = io.BytesIO()
    plt.tight_layout()
    plt.savefig(buf, format='png')
    buf.seek(0)
    image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return io.BytesIO(base64.b64decode(image_base64))

# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
