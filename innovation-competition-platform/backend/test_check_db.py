import sys, os
sys.path.insert(0, '.')
from app import create_app
app = create_app()
with app.app_context():
    from models.material_evaluation import MaterialEvaluation
    import json
    ev = MaterialEvaluation.query.get(8)
    print(f'pdf_path: {ev.pdf_path}')
    print(f'Exists: {os.path.exists(ev.pdf_path) if ev.pdf_path else False}')
    if ev.dimension_scores_json:
        dims = json.loads(ev.dimension_scores_json)
        print(f'Dimensions: {len(dims)} items')