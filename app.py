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

# Fungsi untuk menghitung probabilitas binomial P(X = k)
def binomial_probability(n, p, k):
    coefficient = math.comb(n, k)
    probability = coefficient * (p ** k) * ((1 - p) ** (n - k))
    return probability

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
    try:
        # Mengambil nilai dari input form
        n = int(request.form['n'])
        p = float(request.form['p'])
        k = int(request.form['k'])

        # Validasi input
        if not (0 <= p <= 1):
            return jsonify({'error': 'Nilai p harus antara 0 dan 1.'})
        if n <= 0 or k < 0:
            return jsonify({'error': 'Nilai n harus positif dan k tidak boleh negatif.'})

        # Hitung probabilitas P(X = k)
        px_k = binomial_probability(n, p, k)

        # Hitung probabilitas kumulatif P(X ≤ k)
        total_prob = cumulative_probability(n, p, k)

        # Menghitung persentase probabilitas
        total_prob_percentage = total_prob * 100
        px_k_percentage = px_k * 100

        # Langkah-langkah perhitungan untuk ditampilkan (bisa disesuaikan dengan detail)
        steps = []
        for i in range(k + 1):
            steps.append({'formula': f'P(X = {i}) = \\binom{{{n}}}{{{i}}} {p}^{{{i}}} (1-{p})^{{{n-i}}}'})

        # Daftar P(X = k) untuk setiap k dari 0 hingga k
        all_px = [f'P(X = {i}) = {binomial_probability(n, p, i):.6f}' for i in range(k + 1)]

        # Kembalikan hasil dalam format JSON
        return jsonify(
            result=f"{total_prob_percentage:.2f}%",  # Persentase kumulatif
            px_k=f"{px_k_percentage:.2f}%",  # Persentase untuk k
            steps=steps,  # Langkah-langkah perhitungan
            all_px=all_px  # Semua nilai P(X=k)
        )
    except ValueError:
        return jsonify({'error': 'Input tidak valid. Pastikan nilai yang dimasukkan adalah angka yang tepat.'})

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
