from flask import Flask, render_template, request
import math
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Fungsi untuk menghitung distribusi binomial (PMF)
def binomial_distribution(p, n, k):
    return math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

# Fungsi untuk menghitung distribusi kumulatif binomial (CDF)
def cumulative_binomial_distribution(p, n, k):
    cdf = 0
    for i in range(k + 1):
        cdf += binomial_distribution(p, n, i)
    return cdf

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        p = float(request.form["probabilitas"])  # Probabilitas sukses
        n = int(request.form["percobaan"])  # Jumlah percobaan
        k = int(request.form["keberhasilan"])  # Jumlah keberhasilan yang diinginkan

        # Hitung PMF
        comb = math.comb(n, k)
        pk = p ** k
        qn_k = (1 - p) ** (n - k)
        pmf_value = comb * pk * qn_k

        # Detail langkah-langkah perhitungan dengan LaTeX
        pmf_steps = {
            "kombinasi": f"C({n}, {k}) = \\frac{{{n}!}}{{{k}!({n}-{k})!}} = \\frac{{{math.factorial(n)}}}{{{math.factorial(k)} \\cdot {math.factorial(n-k)}}} = {comb}",
            "prob_sukses": f"p^k = {p}^{{{k}}} = {pk}",
            "prob_gagal": f"(1-p)^{{n-k}} = (1-{p})^{{{n-k}}} = {qn_k}",
            "hasil_pmf": (
                f"P(X = {k}) = \\binom{{{n}}}{{{k}}} \\cdot {p}^{{{k}}} \\cdot (1-{p})^{{{n-k}}} "
                f"= {comb} \\cdot {pk} \\cdot {qn_k} = {pmf_value}"
            )
        }

        # Hitung CDF
        cdf_value = cumulative_binomial_distribution(p, n, k)

        probabilities = []
        for i in range(n + 1):
            probabilities.append(binomial_distribution(p, n, i))

        # Grafik PMF
        fig, ax = plt.subplots()
        ax.bar(range(n + 1), probabilities, label="PMF")
        ax.set_xlabel('Jumlah Sukses (k)')
        ax.set_ylabel('Probabilitas P(X = k)')
        ax.set_title('Distribusi Probabilitas Binomial - PMF')
        plt.legend()

        # Menyimpan grafik ke dalam format gambar
        img_buf = BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)
        img_str = base64.b64encode(img_buf.read()).decode('utf-8')
        img_buf.close()

        return render_template(
            "index.html",
            probabilities=probabilities,
            pmf_steps=pmf_steps,
            img_str=img_str,
            p=p,
            n=n,
            k=k,
            pmf_value=pmf_value,
            cdf_value=cdf_value
        )

        # Tangkap parameter dari URL seperti ?input=...
    url_input = request.args.get("input")
    if url_input:
        return f"Input dari URL: {url_input}"


    return render_template("index.html", probabilities=None, img_str=None)




if __name__ == "__main__":
    app.run(debug=True)
