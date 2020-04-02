#!flask/bin/python
import frames as f
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)

app.frames = {"adjustments_df": f.adjustments_dataframe(),
              "mental_health_df": f.mental_health_dataframe(),
              "organisational_culture_df": f.organisational_culture_dataframe(),
              "work_self_confidence_df": f.work_self_confidence_dataframe()}

app.organisational_culture_df_quantitative = list(map(lambda row: list(map(
    lambda data: f.AnswerMappings.organisational_culture[data] if data in f.AnswerMappings.organisational_culture else data, row)), app.frames["organisational_culture_df"]))

app.mental_health_df_quantitative = list(map(lambda row: list(map(
    lambda data: f.AnswerMappings.mental_health[data] if data in f.AnswerMappings.mental_health else data,row)), app.frames["mental_health_df"]))

app.work_self_confidence_df_quantitative = list(map(lambda row: list(map(
    lambda data: f.AnswerMappings.work_self_confidence[data] if data in f.AnswerMappings.work_self_confidence else data, row)), app.frames["work_self_confidence_df"]))

CORS(app)

@app.route('/adjustments/count', methods=['GET'])
def get_adjustments_count():
    return jsonify(len(app.frames["adjustments_df"]))

@app.route('/adjustments/overview', methods=['GET'])
def get_adjustments_sentiment_overview():
    username = request.args.get('username')
    summary = f.get_adjustments_sentiments_summary(
        app.frames["adjustments_df"], username)
    return jsonify(summary)

@app.route('/mental-health/count', methods=['GET'])
def get_mental_health_count():
    return jsonify(len(app.frames["mental_health_df"]))


@app.route('/mental-health/overview', methods=['GET'])
def get_mental_health_overview():
    username = request.args.get('username')
    summary = f.get_mental_health_summary(
        app.mental_health_df_quantitative, username)
    return jsonify(summary)


@app.route('/work-self-confidence/overview', methods=['GET'])
def get_work_self_confidence_overview():
    username = request.args.get('username')
    summary = f.get_work_self_confidence_summary(
        app.work_self_confidence_df_quantitative, username)
    return jsonify(summary)


@app.route('/organisational-culture/count', methods=['GET'])
def get_organizational_culture_count():
    return jsonify(len(app.frames["organisational_culture_df"]))


@app.route('/work-self-confidence/count', methods=['GET'])
def get_work_self_confidence_count():
    return jsonify(len(app.frames["work_self_confidence_df"]))


## ADMIN ENTRIES:
@app.route('/admin/mental-health/overview', methods=['GET'])
def get_admin_mental_health_overview():
    summary = f.get_admin_mental_health_summary(app.mental_health_df_quantitative)
    return jsonify(summary)


if __name__ == '__main__':
    with app.app_context():
        app.run(debug=True)
