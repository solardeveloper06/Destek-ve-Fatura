from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.form
        installation_type = data.get('installation_type')
        installed_power = float(data.get('installed_power_kwe', 0))
        transformer_status = data.get('transformer_loss_status')
        transformer_pct = float(data.get('transformer_loss_pct', 0)) if transformer_status == 'var' else 0.0
        tariff = data.get('tariff')
        son_kaynak = data.get('son_kaynak')
        
        has_remote = data.get('has_remote')
        remote_tariff = data.get('remote_tariff') if has_remote == 'evet' else None
        remote_sktt = data.get('remote_sktt') if has_remote == 'evet' else None

        effective_power = installed_power * (1 - (transformer_pct / 100)) if transformer_status == 'var' else installed_power

        result = {
            "status": "success",
            "message": "Hesaplama başarıyla tamamlandı.",
            "effective_power_kwe": effective_power,
            "tariff": tariff,
            "son_kaynak": son_kaynak
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
