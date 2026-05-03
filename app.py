import os
from flask import Flask, render_template, request, redirect, url_for, flash
from services import (
    list_meters,
    create_meter,
    update_meter,
    delete_meter,
    trigger_simulation,
    get_readings,
    get_averages,
    get_peaks,
    get_categories,
)

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "smartgrid-client-secret")

@app.route("/", methods=["GET"])
def index():
    meters = []
    readings = []
    averages = []
    peaks = None
    categories = None

    selected_meter_id = request.args.get("meter_id", "").strip()
    start_date = request.args.get("start_date", "").strip()
    end_date = request.args.get("end_date", "").strip()
    analysis_type = request.args.get("analysis_type", "").strip()

    try:
        meters = list_meters()
    except Exception as e:
        flash(f"Failed to load meters: {e}", "error")

    if selected_meter_id or start_date or end_date:
        try:
            meter_id = int(selected_meter_id) if selected_meter_id else None
            readings = get_readings(
                meter_id=meter_id,
                start_date=start_date or None,
                end_date=end_date or None
            )
        except Exception as e:
            flash(f"Failed to load readings: {e}", "error")

    if analysis_type:
        try:
            if not selected_meter_id or not start_date or not end_date:
                flash("Meter ID, start date, and end date are required for analysis.", "error")
            else:
                meter_id = int(selected_meter_id)

                if analysis_type == "averages":
                    averages = get_averages(meter_id, start_date, end_date)
                elif analysis_type == "peaks":
                    peaks = get_peaks(meter_id, start_date, end_date)
                elif analysis_type == "categories":
                    categories = get_categories(meter_id, start_date, end_date)
        except Exception as e:
            flash(f"Failed to load analysis: {e}", "error")

    return render_template(
        "index.html",
        meters=meters,
        readings=readings,
        averages=averages,
        peaks=peaks,
        categories=categories,
        selected_meter_id=selected_meter_id,
        start_date=start_date,
        end_date=end_date,
        analysis_type=analysis_type,
    )

@app.route("/meters/create", methods=["POST"])
def meters_create():
    name = request.form.get("name", "").strip()
    if not name:
        flash("Meter name is required.", "error")
        return redirect(url_for("index"))

    try:
        create_meter(name)
        flash("Meter created successfully.", "success")
    except Exception as e:
        flash(f"Failed to create meter: {e}", "error")

    return redirect(url_for("index"))

@app.route("/meters/update", methods=["POST"])
def meters_update():
    meter_id = request.form.get("meter_id", "").strip()
    name = request.form.get("name", "").strip()

    if not meter_id or not name:
        flash("Meter ID and new name are required.", "error")
        return redirect(url_for("index"))

    try:
        update_meter(int(meter_id), name)
        flash("Meter updated successfully.", "success")
    except Exception as e:
        flash(f"Failed to update meter: {e}", "error")

    return redirect(url_for("index"))

@app.route("/meters/delete", methods=["POST"])
def meters_delete():
    meter_id = request.form.get("meter_id", "").strip()

    if not meter_id:
        flash("Meter ID is required.", "error")
        return redirect(url_for("index"))

    try:
        delete_meter(int(meter_id))
        flash("Meter deleted successfully.", "success")
    except Exception as e:
        flash(f"Failed to delete meter: {e}", "error")

    return redirect(url_for("index"))

@app.route("/simulate", methods=["POST"])
def simulate():
    meter_id = request.form.get("meter_id", "").strip()
    start_date = request.form.get("start_date", "").strip()
    end_date = request.form.get("end_date", "").strip()

    if not meter_id:
        flash("Meter ID is required for simulation.", "error")
        return redirect(url_for("index"))

    try:
        trigger_simulation(
            int(meter_id),
            start_date=start_date or None,
            end_date=end_date or None
        )
        flash("Simulation started successfully.", "success")
    except Exception as e:
        flash(f"Failed to start simulation: {e}", "error")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8004, debug=True)