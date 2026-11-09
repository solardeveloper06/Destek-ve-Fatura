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
        
        generation_kwh = float(data.get('generation_kwh', 0))
        consumption_kwh = float(data.get('consumption_kwh', 0))
        
        # Ayrı Yer Tüketimi Kontrolü
        has_remote = data.get('has_remote')
        remote_consumption_kwh = float(data.get('remote_consumption_kwh', 0)) if has_remote == 'evet' else 0.0
        remote_tariff = data.get('remote_tariff') if has_remote == 'evet' else None

        # Toplam Tüketim Hesaplama (Ana Tesis + Ayrı Yer Tüketimi)
        total_consumption_kwh = consumption_kwh + remote_consumption_kwh
        
        transformer_status = data.get('transformer_loss_status')
        transformer_pct = float(data.get('transformer_loss_pct', 0)) if transformer_status == 'var' else 0.0
        tariff = data.get('tariff')
        
        # Trafo kayıp etkisi hesaplaması
        effective_power = installed_power * (1 - (transformer_pct / 100)) if transformer_status == 'var' else installed_power

        # Net mahsuplaşma (Üretim - Toplam Tüketim)
        net_kwh = generation_kwh - total_consumption_kwh
        net_status = "Veriş Fazlası (Şebekeye Satış/Veriş)" if net_kwh >= 0 else "Çekiş Fazlası (Şebekeden Tüketim)"

        result = {
            "status": "success",
            "message": "Hesaplama başarıyla tamamlandı.",
            "effective_power_kwe": round(effective_power, 2),
            "generation_kwh": generation_kwh,
            "consumption_kwh": consumption_kwh,
            "has_remote": has_remote,
            "remote_consumption_kwh": remote_consumption_kwh,
            "remote_tariff": remote_tariff,
            "total_consumption_kwh": total_consumption_kwh,
            "net_kwh": round(net_kwh, 2),
            "net_status": net_status,
            "tariff": tariff
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
